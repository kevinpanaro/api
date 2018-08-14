import logging
import re
from datetime import date

try:
    from helpers import *
except:
    from .helpers import *


BASE_URL = "http://themayorofoldtown.com/beer/"
BREWERY = "The Mayor of Old Town"
SAVE_FILE = "mayor_of_old_town.json"

locations = ['632 S. Mason St. Fort Collins, CO 80524']

def get_beers_urls(url):

    html = beautiful_url(url)

    all_beers_urls = re.findall("https://themayorofoldtown\.com/beers/.+?(?=\")", str(html))

   
    # all_beers_urls = [urls.find_all('a')[1]['href'] for urls in possible_urls.find_all('li')]

    logging.debug("Found all beers. {} total".format(len(all_beers_urls)))

    return(all_beers_urls)


def parse_url(url):

    all_beers_urls = get_beers_urls(url)

    return_beers = []

    _id = get_id("beer_id")
    for _id, beer in enumerate(all_beers_urls, start = 1):
        beer_dict = {}

        beer_name = None
        beer_description = None
        beer_notes = None
        beer_stats = {}

        beer_brewery = None 
        beer_abv = None
        beer_ibu = None
        beer_hops = []
        beer_malts = []
        beer_avail = []
        beer_style = None


        html = beautiful_url(beer)

        beer_name = html.find('h1', {'class':'beertitle'}).get_text()

        logging.debug("Beer Found: {}".format(beer_name))

        beer_brewery = html.find('h2', {'class': 'brewerytitle'}).get_text().strip()

        logging.debug("Brewery Found: {}".format(beer_brewery))

        beer_style_abv = html.find('span', {'class': 'beerstyle'}).get_text()

        beer_style, beer_abv = tuple(beer.strip() for beer in beer_style_abv.split("|"))

        logging.debug("Style Found: {}".format(beer_style))

        logging.debug("ABV Found: {}".format(beer_abv))

        beer_description = html.find('div', {'class': 'beer-description'}).get_text().strip()

        if beer_description: logging.debug("Description Found")

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

def mayorofoldtown():

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
    except:
        logging.warning("{} failed.")


if __name__ == '__main__':
    mayorofoldtown()
