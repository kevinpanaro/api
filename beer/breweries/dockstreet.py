'''
Author:  Kevin Panaro
Date:    1.30.15
Purpose: Grabs Dock Street Beers on tap
'''
import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer

BASE_URL = "http://www.dockstreetbeer.com/whats-on-tap/"
BREWERY = "Dock Street" # not a brewery just a BASE_URL
SAVE_FILE = "dock_street.json"

locations = ["701 South 50th Street, Philadelphia, PA 19143"]

def parse_url(url):
    '''parse doc street beers'''
    abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)')
    ibu_regex = re.compile('\d+(?=[\s]IBU)|(?<=IBU[\s])\d+')
    style_regex = re.compile('(?<=[\/][\s])[\w\s]+(?=[\s][\/])')
    return_beers = []

    html = beautiful_url(url)

    beers = html.find_all("div", "menu-item")

    for beer in beers:
        beer_dict = {}

        beer_name = unicode_to_ascii(beer.find("div", "menu-item-title").get_text()).title().strip()
        logging.info("Beer found:    {}".format(beer_name))

        beer_description = unicode_to_ascii(beer.find("div", "menu-item-description").get_text()).strip()
        if beer_description:
            logging.info("Beer descripton:  FOUND")

        abv = abv_regex.search(beer_description).group()
        logging.info("ABV found:     {}".format(abv))

        ibu = ibu_regex.search(beer_description).group()
        logging.info("IBU found:     {}".format(ibu))

        try:
            beer_style = style_regex.search(beer_description).group()
            logging.info("Style found:   {}".format(beer_style))
        except AttributeError:
            logging.info("Style not found")
            beer_style = None

        beer_stats = {"ibu": ibu,
                      "abv": abv}

        beer_summary = beer_description.split('/')[-1].strip()
        logging.info("Summary:       FOUND")

        beer_dict = {"beer": beer_name,
                     "description": beer_description,
                     "style": beer_style,
                     "stats": beer_stats,
                     "summary": beer_summary}

        return_beers.append(beer_dict)
    return(return_beers)



def dock_street():

    logLevel=logging.DEBUG
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    output = []
    for location in locations:
        logging.info("Location: {}".format(location))
        beers = parse_url(BASE_URL)
        output.append({"location": location, "beers": beers})

    output = {"brewery": BREWERY, "locations": output}
    save_beer(output, SAVE_FILE)


if __name__ == '__main__':
    dock_street()