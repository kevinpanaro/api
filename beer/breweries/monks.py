'''
Author: Kevin Panaro
Date: 1.28.15
Purpose: Grabs Monks beers on tap

Technically not a brewery, and I want to limit this api to just
craft brewery places that change their taps a lot, but Monk's
kinda falls under the category because their beer selection is 
continuous.

'''
import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.save_beer import save_beer

BASE_URL = "http://www.monkscafe.com/on-tap/"
BREWERY = "Monk's Cafe" # not a brewery just a BASE_URL
SAVE_FILE = "monks.json"

locations = ["264 S. 16th Street, Philadelphia, PA 19102"]


def parse_url(url):
    abv_regex = re.compile('([\d]+\.[\d]\s*|[\d]+\s*)(?=%)')
    summary_regex = re.compile('[\w\s]+\-(.[\w\s\S]+)')
    return_beers = []

    html = beautiful_url(url)

    beer_names = html.find_all("strong", "text-red")
    beer_name_list = []

    beer_descriptions = html.find_all("p", "text-grey")
    beer_descriptions_list = []

    for beer_name in beer_names:
        beer_name = beer_name.get_text()

        if beer_name.strip() != "":
            beer_name_list.append(beer_name)

    for beer_description in beer_descriptions:
        beer_description = beer_description.get_text()

        if beer_description.strip() != "":
            beer_descriptions_list.append(beer_description)


    beer_name_list = beer_name_list[:len(beer_descriptions_list)]

    for beer, description in zip(beer_name_list, beer_descriptions_list):
        stats = {}

        description = description.strip()
        try:
            origin = description.split("-")[0].strip().title()
        except AttributeError:
            origin = None

        try:
            abv = abv_regex.search(description).group()
        except AttributeError:
            abv = None

        stats = {"abv": abv,
                 "origin": origin}

        beer_dict = {"beer": beer.strip(),
                     "description": description,
                     "stats": stats,
                     "summary": summary_regex.search(description).group(1).strip()}
        return_beers.append(beer_dict)
    return(return_beers)


def monks():

    logLevel=logging.WARN
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
    monks()