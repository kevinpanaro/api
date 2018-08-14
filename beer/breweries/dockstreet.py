'''
Author:  Kevin Panaro
Date:    1.30.15
Purpose: Grabs Dock Street Beers on tap
'''

import logging
import re
from datetime import date

try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "http://www.dockstreetbeer.com/whats-on-tap/"
BREWERY = "Dock Street" # not a brewery just a BASE_URL
SAVE_FILE = "dock_street.json"

locations = ["701 South 50th Street, Philadelphia, PA 19143"]

def parse_url(url):
    '''parse doc street beers'''
    abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)')
    ibu_regex = re.compile('\d+(?=[\s]IBU)|(?<=IBU[\s])\d+')
    style_regex = re.compile('(?<=-)[\w\s]+(?=-)')
    return_beers = []

    html = beautiful_url(url)

    beers = html.find_all("div", "menu-item")

    _id = get_id("beer_id")

    for beer in beers:

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

        beer_name = beer.find("div", "menu-item-title").get_text().title().strip()
        logging.info("Beer found:    {}".format(beer_name))

        beer_description = beer.find("div", "menu-item-description").get_text().strip()
        if beer_description:
            logging.info("Beer descripton:  FOUND")

        beer_abv = abv_regex.search(beer_description).group()
        logging.info("ABV found:     {}".format(beer_abv))

        beer_ibu = ibu_regex.search(beer_description).group()
        logging.info("IBU found:     {}".format(beer_ibu))

        try:
            beer_style = style_regex.search(beer_description).group().strip()
            logging.info("Style found:   {}".format(beer_style))
        except AttributeError:
            logging.info("Style not found")
            beer_style = None

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
        _id += 1

    set_id(file_name = "beer_id", starting_id = _id)
    return(return_beers)



def dock_street():

    logLevel=logging.DEBUG
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
        for _id, location in enumerate(locations, start = 1):
            logging.info("Location: {}".format(location))
            beers = parse_url(BASE_URL)
            output.append({"location": location, 
                           "beers": beers, 
                           "id": _id,
                           "type": "location"})

        output = {"locations": output, "establishment": BREWERY, "id": b_id()[BREWERY], "type": "establishment"}
        save_beer(output, SAVE_FILE)

        logging.info(f"Complete: {BREWERY}")
    except Exception as e:
        logging.warning(f"{type(e)} {e} failed.")

if __name__ == '__main__':
    dock_street()