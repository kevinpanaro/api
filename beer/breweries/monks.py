'''
Author: Kevin Panaro
Date: 1.28.15
Purpose: Grabs Monks beers on tap

Technically not a brewery, and I want to limit this api to just
craft brewery places that change their taps a lot, but Monk's
kinda falls under the category because their beer selection is 
continuous.

'''
import logging
import re
from datetime import date

try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "http://www.monkscafe.com/on-tap/"
BREWERY = "Monk's Cafe" # not a brewery just a BASE_URL
SAVE_FILE = "monks.json"

locations = {"264 S. 16th Street, Philadelphia, PA 19102": None}


def parse_url(url):
    abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)')
    summary_regex = re.compile('[\w\s]+\-(.[\w\s\S]+)')
    return_beers = []

    html = beautiful_url(url)

    beer_names = html.find_all("strong", "text-red")
    beer_name_list = []

    beer_descriptions = html.find_all("p", "text-grey")
    beer_descriptions_list = []

    for beer_name in beer_names:
        beer_name = beer_name.get_text()

        if beer_name.strip() != "":
            beer_name_list.append(beer_name)

    for beer_description in beer_descriptions:
        beer_description = beer_description.get_text()

        if beer_description.strip() != "":
            beer_descriptions_list.append(beer_description)


    beer_name_list = beer_name_list[:len(beer_descriptions_list)]

    _id = get_id("beer_id")

    for beer_name, beer_description in zip(beer_name_list, beer_descriptions_list):
        logging.debug(f"id: {_id}, beer: {beer_name}")
        beer_dict = {}
        beer_notes = None
        beer_stats = {}

        beer_brewery = None # everything served here is by Tired Hands
        beer_abv = None
        beer_ibu = None
        beer_hops = []
        beer_malts = []
        beer_avail = []
        beer_style = []

        stats = {}

        beer_description = beer_description.strip()

        try:
            origin = beer_description.split("-")[0].strip().title()
        except AttributeError:
            origin = None

        try:
            beer_abv = abv_regex.search(beer_description).group()
        except AttributeError:
            beer_abv = None


        # stats = {"abv": abv,
        #          "origin": origin}

        # beer_dict = {"beer": beer.strip(),
        #              "description": description,
        #              "stats": stats,
        #              "summary": summary_regex.search(description).group(1).strip()}
        

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


def monks():

    logLevel=logging.DEBUG
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
        
        _id = get_id("location_id")

        for location, url in locations.items():
            logging.info("Location: {}".format(location))
            location_url = BASE_URL.format(url)
            beers = parse_url(location_url)
            output.append({"location": location, 
                           "beers": beers, 
                           "id": _id,
                           "type": "location"})
            _id += 1

        set_id(file_name = "location_id", starting_id = _id) 

        output = {"locations": output, "establishment": BREWERY, "id": b_id()[BREWERY], "type": "establishment"}
        save_beer(output, SAVE_FILE)
        
        logging.info(f"Complete: {BREWERY}")
    except Exception as e:
        logging.warning(f"{type(e)}, {e} failed.")

if __name__ == '__main__':
    monks()
