'''
Author: Kevin Panaro
Date: 1.28.15
Purpose: Grabs Evil Genius beers

TODO: Something is weird with their menu. All the beers scraped are more
      than the amount of beers on tap. Maybe it's also what they are 
      selling on the side, but I don't think I want to change it.
'''
import logging
try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "http://evilgeniusbeer.com/beers/"
BREWERY = "Evil Genius Brewery"
locations = {'Fishtown': None}
SAVE_FILE = "evil_genius.json"

def parse_url(url):
    '''gets beer data from url'''
    return_beers = []

    html = beautiful_url(url)
    
    beers = html.find_all("div", "beer")

    _id = get_id("beer_id")

    for beer in beers:
        logging.debug(f'id: {_id}')

        beer_dict = {}
        beer_name = None
        beer_description = None
        beer_notes = None
        beer_stats = {}

        beer_brewery = BREWERY # everything served here is by Evil Genius
        beer_abv = None
        beer_ibu = None
        beer_hops = []
        beer_malts = []
        beer_avail = []
        beer_style = []

        try:
            beer_name = beer.find("h2", "beer-title").get_text()
            logging.info(f"Beer found:  {beer_name}")
        except:
            logging.warn("NO BEER FOUND")



        try:
            beer_style = beer.find("h4", "beer-style").get_text()
            logging.info(f"Style:       {beer_style}")
        except:
            pass # sometimes non-existant, skipping for now.

        

        try:
            beer_description = beer.find("div", "col col-1-3").get_text().strip("\n")
            logging.info("Description: Found")
        except:
            logging.warn("no description found")

        beer_stats = beer.find("div", "col col-1-3 beer-stats")
        
        beer_stats_dict = {}

        beer_stats_last = None

        for stat in beer_stats.stripped_strings:
            if stat[-1] == ":":
                '''it's a dict key now'''
                stat = stat.strip(":")
                beer_stats_last = stat.lower()
            else:
                value = stat
                beer_stats_dict[beer_stats_last] = value

        logging.info("Stats:       Found")
        logging.debug(beer_stats_dict)

        try:
            beer_abv = beer_stats_dict['abv']
        except:
            beer_abv = None

        try:
            beer_hops = beer_stats_dict['hops']
        except:
            beer_hops = []

        try:
            beer_ibu = beer_stats_dict['ibu']
        except:
            beer_ibu = None

        try:
            beer_malts = beer_stats_dict['malts']
        except:
            beer_malts = []

        try:
            beer_avail = beer_stats_dict['available']
        except:
            beer_avail = []

        # not used
        try:
            beer_package = beer_stats_dict['package']
        except:
            beer_package = None

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

def evil_genius():

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
        logging.warning(f"{type(e)} {e} failed.")

if __name__ == '__main__':
    evil_genius()
