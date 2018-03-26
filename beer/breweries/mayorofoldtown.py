import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer


BASE_URL = "http://themayorofoldtown.com/beer/"
BREWERY = "The Mayor of Old Town"
SAVE_FILE = "mayor_of_old_town.json"

locations = ['632 S. Mason St. Fort Collins, CO 80524']

def get_beers_urls(url):

    html = beautiful_url(url)

    possible_urls = html.find('ul', {'class': 'currently_available clearfix'})

    all_beers_urls = [urls.find_all('a')[1]['href'] for urls in possible_urls.find_all('li')]

    logging.debug("Found all beers. {} total".format(len(all_beers_urls)))

    return(all_beers_urls)


def parse_url(url):

    all_beers_urls = get_beers_urls(url)

    return_beers = []

    for beer in all_beers_urls:
        beer_dict = {}
        html = beautiful_url(beer)

        beer_container = html.find('div', {'class': 'container'})

        beer_name = unicode_to_ascii(beer_container.find('h1').get_text())

        beer_desc_cont = beer_container.find('div', {'id': 'content-inner'})

        try:
            beer_description = unicode_to_ascii(beer_desc_cont.find('p').get_text())
        except AttributeError:
            logging.info("{} description hard to find. Trying again.".format(beer))
            beer_description = unicode_to_ascii(beer_desc_cont.find('div').get_text())

        logging.debug("Beer Description FOUND")

        beer_details = beer_container.find('div', {'id': 'sidebar-inner'})

        beer_details = ([detail.get_text().strip() for detail in beer_details.find_all('dd')])

        style, abv, container_type = beer_details

        beer_stats = {'style': style,
                      'abv': abv.strip('%') + '%',
                      'container_type': container_type}

        beer_dict = {"beer": beer_name,
                     "description": beer_description,
                     "stats": beer_stats}   

        return_beers.append(beer_dict)
    return(return_beers)  

def mayor_of_old_town():

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
    mayor_of_old_town()