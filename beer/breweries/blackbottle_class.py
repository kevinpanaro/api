# -*- coding: utf-8 -*-
try:
    from helpers.breweries import Brewery
except ModuleNotFoundError:
    from .helpers.breweries import Brewery
import logging

base_url = "https://blackbottlebrewery.com/bbb-beers/on-tap/"
brewery_name = "Black Bottle Brewery"
cookies = [{'name': 'popupcookie', 'value': 'yes', 'domain': 'blackbottlebrewery.com', 'path': '/'}]
javascript = True
save_file = "black_bottle_class.json"
locations = {"1611 S College Ave, Suite 1609, Fort Collins, CO 80525": ""}
single_page = True
beers_html_tags = ('div', {"class": "beer"})
beer_parent_tags = ('div', {"id": "menu-17035"})
beer_name_tags = ('a', {"class": "item-title-color"})
beer_abv_tags = ('div', {"class": "abv-hideable"})
beer_ibu_tags = ("div", {"class": "ibu-hideable"})
beer_brewery_tags = ('div', {"class": "brewery-name-hideable"})
beer_style_tags = ('span', {"class": "beer-style beer-style-hideable item-title-color"})
beer_description_tags = ('p', {'class': "link-font-color show-less item-title-color"})


BB = Brewery(brewery_name=brewery_name,
             base_url=base_url,
             cookies=cookies,
             javascript=javascript,
             save_file=save_file,
             locations=locations,
             single_page=single_page,
             beers_html_tags=beers_html_tags,
             beer_parent_tags=beer_parent_tags,
             beer_name_tags=beer_name_tags,
             beer_abv_tags=beer_abv_tags,
             beer_ibu_tags=beer_ibu_tags,
             beer_brewery_tags=beer_brewery_tags,
             beer_style_tags=beer_style_tags,
             beer_description_tags=beer_description_tags,
             )



def BlackBottle():
    BB.run()

if __name__ == '__main__':
    import logging
    logLevel=logging.INFO
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)
    BlackBottle()