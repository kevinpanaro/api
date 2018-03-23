'''
Author:  Kevin Panaro
Date:    3.21.18
Purpose: Grabs Odell Beers on tap
'''
import logging
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer
from bs4 import BeautifulSoup as bs
from requests import get, Request, Session, cookies
from contextlib import closing

BASE_URL = "https://www.odellbrewing.com/tap-room/"
BREWERY = "Odell Brewing" 
SAVE_FILE = "odell.json"

locations = ["800 East Lincoln Ave, Fort Collins, CO 80524"]

def beautiful_url(url):
    '''because a wall'''
    jar = cookies.RequestsCookieJar()
    jar.set('odAccess', 'true', domain='www.odellbrewing.com', path='/')
    req = Request('GET', url, cookies=jar)
    req = req.prepare()
    s = Session()
    r = s.send(req)
    souped_url = bs(r.text, "html.parser")
    return(souped_url)

def get_beers_url(url):
    html = beautiful_url(url)
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
        beer = beautiful_url(beer_url)

        beer_name = beer.find('div', {'class':'columns small-12 beer-title'}).get_text().strip()

        logging.debug("Beer Found: {}".format(beer_name))

        beer_description = unicode_to_ascii(beer.find('div', {'class':'beer-content'}).get_text().strip())

        if beer_description:
            logging.debug("Description: Found")
        else:
            logging.warn("No Description Found")

        beer_details = beer.find_all('div', {'class':'columns small-12 medium-12'})

        beer_stats = {}
        # i'll figure out a nicer way for this later
        for num, stat in enumerate(beer_details):
            if num == 0:
                ibu = stat.get_text().strip().split(":")
                beer_stats['ibu'] = ibu[-1].strip().title()
            elif num == 1:
                style = stat.get_text().strip()
                beer_stats['style'] = style
            elif num == 2:
                abv = stat.get_text().strip().split(":")
                beer_stats['abv'] = abv[-1].strip().title()
            elif num == 3:
                availability = stat.get_text().strip()
                beer_stats['availability'] = availability

        beer_dict = {"beer": beer_name,
                     "description": beer_description,
                     "stats": beer_stats}   

        return_beers.append(beer_dict)
    return(return_beers)   

def odell():

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
    odell()