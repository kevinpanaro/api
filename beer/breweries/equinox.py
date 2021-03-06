'''
Author:  Kevin Panaro
Date:    3.21.18
Purpose: Grabs Equinox Beers on tap
Note:    Someone fix this horrible website design
'''
import logging

try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "https://equinoxbrewing.com/"
BREWERY = "Equinox Brewing" 
SAVE_FILE = "equinox.json"

locations = {"133 Remington Street, Fort Collins, CO 80524": None}

def get_beers_url(url):
    html = beautiful_url(url)
    beer_urls = [url['href'] for url in html.find_all("a", "tg-element-absolute", href=True)]
    logging.debug("{} beer urls found".format(len(beer_urls)))
    return(beer_urls)

def parse_url(url):
    beer_urls = get_beers_url(url)

    return_beers = []

    _id = get_id("beer_id")
    for beer_url in beer_urls:
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
        beer_style = []
        beer_dict = {}

        beer = beautiful_url(beer_url)

        beer_name = beer.find('h1', {'class': 'entry-title'}).get_text()

        logging.debug(f"Beer Found: {beer_name}")

        beer_details = beer.find('div', {'class': 'entry-content content'})

        beer_description, beer_details = (beer_details.find_all('p'))

        beer_description = beer_description.get_text()

        logging.debug("Beer descripton:  FOUND")

        beer_details = beer_details.get_text().split("|")
        logging.debug(beer_details)

        beer_stats = {}

        for stat in beer_details:
            stat = stat.strip()
            try:
                stat, data = (stat.split(":"))
            except:
                logging.info(f"{stat} has too many :")
                continue
            stat = stat.replace(" ", "_")
            beer_stats[stat.lower()] = data.strip()

        try:
            beer_abv = beer_stats['abv']
        except:
            beer_abv = None



        try:
            beer_ibu = beer_stats['ibu']
        except:
            beer_ibu = None

  
        logging.debug(beer_stats) 
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


def equinox():

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
    except:
        logging.warning("{} failed.")

if __name__ == '__main__':
    equinox()
