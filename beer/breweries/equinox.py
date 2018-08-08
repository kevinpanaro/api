'''
Author:  Kevin Panaro
Date:    3.21.18
Purpose: Grabs Equinox Beers on tap
Note:    Someone fix this horrible website design
'''
import logging
from helpers.url_pull import beautiful_url
from helpers.save_beer import save_beer

BASE_URL = "https://equinoxbrewing.com/"
BREWERY = "Equinox Brewing" 
SAVE_FILE = "equinox.json"

locations = ["133 Remington Street, Fort Collins, CO 80524"]

def get_beers_url(url):
    html = beautiful_url(url)
    beer_urls = [url['href'] for url in html.find_all("a", "tg-element-absolute", href=True)]
    logging.debug("{} beer urls found".format(len(beer_urls)))
    return(beer_urls)

def parse_url(url):
    beer_urls = get_beers_url(url)

    return_beers = []

    for beer_url in beer_urls:
        beer_dict = {}
        beer = beautiful_url(beer_url)

        beer_name = beer.find('h1', {'class': 'entry-title'}).get_text()

        logging.debug("Beer Found: {}".format(beer_name))

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
  
        logging.debug(beer_stats) 

        beer_dict = {"beer": beer_name,
                     "description": beer_description,
                     "stats": beer_stats}

        return_beers.append(beer_dict)
    return(return_beers)   


def equinox():

    logLevel=logging.DEBUG
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []
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
    equinox()