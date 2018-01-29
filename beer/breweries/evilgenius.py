'''
Author: Kevin Panaro
Date: 1.28.15
Purpose: Grabs Evil Genius beers

TODO: Something is weird with their menu. All the beers scraped are more
      than the amount of beers on tap. Maybe it's also what they are 
      selling on the side, but I don't think I want to change it.
'''
import logging
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer

BASE_URL = "http://evilgeniusbeer.com/beers/"
BREWERY = "Evil Genius Brewery"
locations = ['Fishtown']
SAVE_FILE = "evil_genius.json"

def parse_url(url):
    '''gets beer data from url'''
    return_beers = []

    html = beautiful_url(url)
    
    beers = html.find_all("div", "beer")

    for beer in beers:
        beer_dict = {}
        beer_name = unicode_to_ascii(beer.find("h2", "beer-title").get_text())
        beer_style = unicode_to_ascii(beer.find("h4", "beer-style").get_text())
        beer_description = unicode_to_ascii(beer.find("div", "col col-1-3").get_text()).strip("\n")

        logging.info("Beer found:  {}".format(beer_name))
        logging.info("Style:       {}".format(beer_style))
        if beer_description:
            logging.info("Description: Found")

        beer_stats = beer.find("div", "col col-1-3 beer-stats")
        
        beer_stats_dict = {}

        beer_stats_last = None

        for stat in beer_stats.stripped_strings:
            if stat[-1] == ":":
                '''it's a dict key now'''
                stat = stat.strip(":")
                beer_stats_last = stat
            else:
                value = stat
                beer_stats_dict[beer_stats_last] = value

        logging.info("Stats:       Found")
        logging.debug(beer_stats_dict)

        beer_dict = {"beer": beer_name, 
                     "description": beer_description, 
                     "style": beer_style, 
                     "stats": beer_stats_dict}

        return_beers.append(beer_dict)
    return(return_beers)

def evil_genius():

    logLevel = logging.DEBUG
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
    evil_genius()