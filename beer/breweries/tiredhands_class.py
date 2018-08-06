import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer
from helpers.breweries import Brewery

BASE_URL = "http://www.tiredhands.com/{}/beers/"
BREWERY = "Tired Hands Brewery"
SAVE_FILE = "tired_hands.json"

LOCATIONS = ['fermentaria', 'cafe']

class TiredHands(Brewery):

    def __init__(self):
        self.base_url = BASE_URL
        self.brewery = BREWERY
        self.save_file = SAVE_FILE
        self.locations = LOCATIONS

    def update(self):
        logLevel=logging.DEBUG
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
        logging.basicConfig(format=FORMAT,level=logLevel)

        try:
            output = []
            for location in self.locations:
                logging.info("Location: {}".format(location))
                location_url = self.base_url.format(location)
                self.parse_url(location_url)
                output.append({"location": location, "beers": self.return_beers, "update_time": self.update_time})
            output = {"locations": output, "brewery": self.brewery}
            save_beer(output, self.save_file)
            
            print("{} completed".format(self.brewery))
        except:
            logging.warn("{} failed.")



    def parse_url(self, url):
        '''gets beer data from url'''
        kill = ["***Other Beverages***", "***Sunday Brunch Beverages***"]
        return_beers = []

        year = date.today().strftime('%y')
        update_time_regex = re.compile("\d+/\d+/\d+".format(year))

        data = beautiful_url(url)
        try:
            update_time = data.find('div', 'sqs-block html-block sqs-block-html')
        except AttributeError:
            logging.info("AttributeError, but trying again")
            parse_url(url)

        try:
            update_time = unicode_to_ascii(update_time.text)
        except UnboundLocalError:
            logging.warn("UnboundLocalError, but skipping")
        update_time = update_time_regex.search(update_time).group(0)
        logging.info("Update date: {}".format(update_time))

        beers = data.find_all('div', 'menu-item')
        
        for beer in beers:
            abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)%')
            style_regex = re.compile('[\D]+')

            beer_dict = {}
            beer_name = None
            beer_description = None
            beer_notes = None
            beer_stats = {}

            try:
                beer_name = unicode_to_ascii(beer.find('div', 'menu-item-title').get_text().strip(':'))
                if beer_name in kill:
                    logging.info("All beer found")
                    break
                logging.info("Beer found: {}".format(beer_name))

                beer_description = unicode_to_ascii(beer.find('div', 'menu-item-description').get_text().strip())
                logging.info("Description found")

                abv = abv_regex.search(beer_description).group(0)
                style = style_regex.search(beer_description).group(0)

                if abv:
                    beer_stats['abv'] = abv
                if style:
                    beer_stats['style'] = style.strip()

                try:
                    beer_notes = unicode_to_ascii(beer.find('div', 'menu-item-price-bottom').get_text().strip()[1::])
                    logging.info("Notes found")
                except:
                    beer_notes = ""
                    logging.info("Notes not found")

            except AttributeError:
                logging.info("bad beer")

            if beer_name and beer_description and beer_notes and beer_stats:
                beer_dict = {"beer": beer_name, 
                             "description": beer_description, 
                             "summary": beer_description + " " + beer_notes, 
                             "notes": beer_notes, 
                             "stats": beer_stats}

                return_beers.append(beer_dict)

        self.return_beers = return_beers
        self.update_time = update_time


