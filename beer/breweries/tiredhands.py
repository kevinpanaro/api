import logging
import re
from datetime import date

try:
    from helpers import *
except:
    from .helpers import *


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

    except AttributeError: # this has a potentional to loop forever... TODO
        logging.info("AttributeError, but trying again")
        parse_url(url)

    try:
        update_time = update_time
    except UnboundLocalError:
        update_time = None
        logging.warning("UnboundLocalError, but skipping")

    update_time = update_time_regex.search(update_time.text).group(0)

    logging.debug("Update date: {}".format(update_time))

    beers = data.find_all('div', 'menu-item')

    for _id, beer in enumerate(beers, start = 1):
        abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)%')
        style_regex = re.compile('[\D]+')

        beer_dict = {}
        beer_name = None
        beer_description = None
        beer_notes = None
        beer_stats = {}

        beer_brewery = BREWERY # everything served here is by Tired Hands
        beer_abv = None
        beer_ibu = None
        beer_hops = []
        beer_malts = []
        beer_avail = []
        beer_style = None

        try:
            beer_name = beer.find('div', 'menu-item-title').get_text().strip().strip(":")
            if beer_name in kill:
                logging.info("All beer found")
                break
            logging.debug("Beer found: {}".format(beer_name))

            beer_description = beer.find('div', 'menu-item-description').get_text().strip()
            logging.debug("Description found")

            abv = abv_regex.search(beer_description).group(0)
            style = style_regex.search(beer_description).group(0)
            
            if abv:
                beer_abv = abv

            if style:
                beer_style = style.strip()

            try:
                beer_notes = beer.find('div', 'menu-item-price-bottom').get_text().strip()[1::]
                logging.debug("Notes found")
            except:
                beer_notes = ""
                logging.info("Notes not found")

            beer_description = beer_description + " " + beer_notes

            beer_dict = format_beer_dict(_id              = _id,
                                         _type            = "beer",
                                         beer_name        = beer_name,
                                         beer_description = beer_description,
                                         beer_brewery     = beer_brewery,
                                         beer_abv         = beer_abv,
                                         beer_ibu         = beer_ibu,
                                         beer_hops        = beer_hops,
                                         beer_malts       = beer_malts,
                                         beer_avail       = beer_avail,
                                         beer_style       = beer_style,)

            return_beers.append(beer_dict)

        except AttributeError:
            logging.info("bad beer")

    return(return_beers, update_time)


def tired_hands():

    logLevel=logging.INFO
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
        logging.info(f"Establishment: {BREWERY}")
        for _id, location in enumerate(locations, start = 1):
            logging.info("Location: {}".format(location))
            location_url = BASE_URL.format(location)
            beers, update_time = parse_url(location_url)
            output.append({"location": location, 
                           "beers": beers, 
                           "update_time": update_time,
                           "id": _id,
                           "type": "location"})
            
        output = {"locations": output, "establishment": BREWERY, "id": b_id()[BREWERY], "type": "establishment"}
        save_beer(output, SAVE_FILE)
        
        logging.info(f"Complete: {BREWERY}")
    except Exception as e:
        logging.warning(f"{type(e)} {e} failed.")


if __name__ == '__main__':
    tired_hands()
