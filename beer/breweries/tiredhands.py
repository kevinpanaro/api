import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer


BASE_URL = "http://www.tiredhands.com/{}/beers/"
BREWERY = "Tired Hands Brewery"
SAVE_FILE = "tired_hands.json"

locations = ['fermentaria', 'cafe']


def parse_url(url):
    '''gets beer data from url'''
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
        beer_dict = {}
        try:
            beer_name = unicode_to_ascii(beer.find('div', 'menu-item-title').get_text().strip().strip(':'))
            logging.info("Beer found: {}".format(beer_name))

            beer_description = unicode_to_ascii(beer.find('div', 'menu-item-description').get_text().strip())
            logging.info("Description found")
            try:
                beer_notes = unicode_to_ascii(beer.find('div', 'menu-item-price-bottom').get_text().strip()[1::])
                logging.info("Notes found")
            except:
                beer_notes = ""
                logging.info("Notes not found")
        except AttributeError:
            logging.info("Reached ends of beer")
            break
        beer_dict = {"beer": beer_name, "description": beer_description, "summary": beer_description + "\n" + beer_notes, "notes": beer_notes}
        return_beers.append(beer_dict)
    return(return_beers, update_time)
    


def tired_hands():

    logLevel=logging.WARN
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    output = []
    for location in locations:
        logging.info("Location: {}".format(location))
        location_url = BASE_URL.format(location)
        beers, update_time = parse_url(location_url)
        output.append({"location": location, "beers": beers, "update_time": update_time})
    output = {"locations": output, "brewery": BREWERY}
    save_beer(output, SAVE_FILE)

    

if __name__ == '__main__':
    tired_hands()