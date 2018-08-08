'''
Author:  Kevin Panaro
Date:    3.21.18
Purpose: Grabs Odell Beers on tap
'''
import logging

try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "https://www.odellbrewing.com/tap-room/"
BREWERY = "Odell Brewing" 
SAVE_FILE = "odell.json"
COOKIE = ('odAccess', 'true', 'www.odellbrewing.com', '/')

locations = ["800 East Lincoln Ave, Fort Collins, CO 80524"]

def get_beers_url(url):
    html = beautiful_url(url, COOKIE)
    all_beers = html.find_all('p', {'class':'tap-beer'})
    beer_urls = []
    for url in html.find_all('p', {'class':'tap-beer'}):
        beer_urls.append(url.find('a')['href'])
    logging.debug("{} beer urls found".format(len(beer_urls)))
    return(beer_urls)

def parse_url(url):

    beer_urls = get_beers_url(url)

    return_beers = []

    for beer_url in beer_urls:
        beer_dict = {}
        beer = beautiful_url(beer_url, COOKIE)

        beer_name = beer.find('div', {'class':'columns small-12 beer-title'}).get_text().strip()

        logging.debug("Beer Found: {}".format(beer_name))

        beer_description = beer.find('div', {'class':'beer-content'}).get_text()

        if beer_description:
            logging.debug("Description: Found")
        else:
            logging.warning("No Description Found")

        beer_details = beer.find_all('div', {'class':'columns small-12 medium-12'})

        beer_details = ([detail.get_text().strip() for detail in beer_details])

        ibu, style, abv, availability = beer_details

        beer_stats = {'ibu': ibu.split(':')[-1],
                      'style': style,
                      'abv': abv.split(':')[-1],
                      'availability': availability}

        beer_dict = {"beer": beer_name,
                     "description": beer_description,
                     "stats": beer_stats}   

        return_beers.append(beer_dict)
    return(return_beers)   

def odell():

    logLevel=logging.DEBUG
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
        cookie = ('odAccess', 'true', 'www.odellbrewing.com', '/')
        for location in locations:
            logging.info("Location: {}".format(location))
            beers = parse_url(BASE_URL)
            output.append({"location": location, "beers": beers})

        output = {"brewery": BREWERY, "locations": output}
        save_beer(output, SAVE_FILE)
        
        print("{} completed".format(BREWERY))
    except:
        logging.warning("{} failed.")

if __name__ == '__main__':
    odell()
