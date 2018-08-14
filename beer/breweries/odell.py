'''
Author:  Kevin Panaro
Date:    3.21.18
Purpose: Grabs Odell Beers on tap

What happened?

My cookie's were working but the actual beers were 
rendere by a javascript script. So now i'm using
requests-html, to render the website, before 
collecting the raw_html
'''
import logging

try:
    from helpers import *
except:
    from .helpers import *

BASE_URL = "https://www.odellbrewing.com/taproom{}/"
BREWERY = "Odell Brewing" 
SAVE_FILE = "odell.json"
COOKIES = [{'name': 'odAccess', 'value': 'true', 'domain': 'www.odellbrewing.com', 'path': '/'}]
 
locations = {"Fort Collins": "", "Denver": "-denver"}

# def get_beers_url(url):
#     html = beautiful_url(url=url, cookies=COOKIES, javascript=True)
#     all_beers = html.find_all('div', {"class": "item-bg-color menu-item"})
    
#     beer_urls = []
#     for url in html.find_all('p', {'class':'tap-beer'}):
#         beer_urls.append(url.find('a')['href'])
#     logging.debug("{} beer urls found".format(len(beer_urls)))
#     return(beer_urls)

def parse_url(url):
    beers = beautiful_url(url=url, cookies=COOKIES, javascript=True)
    beers = beers.find_all('div', {'class': 'item-bg-color menu-item'})
    logging.info(f"Found {len(beers)} beers")
    return_beers = []

    _id = get_id("beer_id")

    for beer in beers:
        print(beer)
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
        beer_style = None
        beer_dict = {}

        beer_name = beer.find('span', {'class':'item'}).get_text().strip()
        logging.info(f"Beer Found: {beer_name}")

        beer_brewery = beer.find('span', {"class": "brewery-name-hideable brewery hide"}).get_text()
        logging.info(f"Brewery Found: {beer_brewery}")

        beer_style = beer.find('span', {'class':'beer-style-hideable beer-style'}).get_text()
        logging.info(f"Style Found: {beer_style}")

        beer_abv = beer.find('span', {'class': 'abv-hideable abv'}).get_text()
        logging.info(f"ABV Found: {beer_abv}")

        try:
            beer_ibu = beer.find('span', {"class": "ibu-hideable ibu hide"}).get_text()
            logging.info(f"IBU Found: {beer_ibu}")
        except:
            pass

        beer_description = beer.find('p', {'class': 'show-less item-title-color'}).get_text()
        
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

def odell():

    logLevel=logging.INFO
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

    try:
        output = []

        for location, url in locations.items():
            logging.info("Location: {}".format(location))
            beers = parse_url(BASE_URL.format(url))
            output.append({"location": location, "beers": beers})

        output = {"locations": output, "establishment": BREWERY, "id": b_id()[BREWERY], "type": "establishment"}
        save_beer(output, SAVE_FILE)
        
        logging.info(f"Complete: {BREWERY}")
    except Exception as e:
        logging.warning(f"{e} failed.")

if __name__ == '__main__':
    odell()
