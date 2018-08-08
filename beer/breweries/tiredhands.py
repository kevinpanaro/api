import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.save_beer import save_beer
from helpers.breweries import Brewery


BASE_URL = "http://www.tiredhands.com/{}/beers/"
BREWERY = "Tired Hands Brewery"
SAVE_FILE = "tired_hands.json"

locations = ['fermentaria', 'cafe']


def parse_url(url):
    '''gets beer data from url'''
    kill = ["***Other Beverages***", "***Sunday Brunch Beverages***"]
    return_beers = []

    update_time_regex = re.compile('\d+/\d+/\d+')

    data = beautiful_url(url)
    

    try:
        update_time = data.find('div', 'sqs-block html-block sqs-block-html')

    except AttributeError:
        logging.info("AttributeError, but trying again")
        parse_url(url)


    try:
        update_time = update_time
    except UnboundLocalError:
        logging.warning("UnboundLocalError, but skipping")

    update_time = update_time_regex.search(update_time.text).group(0)

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
            beer_name = beer.find('div', 'menu-item-title').get_text().strip().strip(":")
            if beer_name in kill:
                logging.info("All beer found")
                break
            logging.info("Beer found: {}".format(beer_name))

            beer_description = beer.find('div', 'menu-item-description').get_text().strip()
            logging.info("Description found")

            abv = abv_regex.search(beer_description).group(0)
            style = style_regex.search(beer_description).group(0)

            if abv:
                beer_stats['abv'] = abv
            if style:
                beer_stats['style'] = style.strip()

            try:
                beer_notes = beer.find('div', 'menu-item-price-bottom').get_text().strip()[1::]
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

    return(return_beers, update_time)
    


def tired_hands():

    logLevel=logging.DEBUG
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
        for location in locations:
            logging.info("Location: {}".format(location))
            location_url = BASE_URL.format(location)
            beers, update_time = parse_url(location_url)
            output.append({"location": location, "beers": beers, "update_time": update_time})
        output = {"locations": output, "brewery": BREWERY}
        save_beer(output, SAVE_FILE)
        
        print("{} completed".format(BREWERY))
    except Exception as e:
        logging.warning(f"{e} failed.")

    

if __name__ == '__main__':
    tired_hands()