try:
    from helpers.breweries import Brewery
except ModuleNotFoundError:
    from .helpers.breweries import Brewery
import logging

base_url = "http://www.tiredhands.com/{}/beers/"
brewery_name = "Tired Hands Brewery"
cookies = None
javascript = False
save_file = "tired_hands_class.json"
locations = {"Fermentaria": 'fermentaria',"Brew Cafe": "cafe"}
single_page = True
beers_html_tags = ('div', 'menu-item')
beer_name_tags = ('div', 'menu-item-title')
beer_description_tags = ('div', 'menu-item-description')
kill = ["***Other Beverages***", "***Sunday Brunch Beverages***"]


TH = Brewery(brewery_name=brewery_name,
                     base_url=base_url,
                     cookies=cookies,
                     javascript=javascript,
                     save_file=save_file,
                     locations=locations,
                     single_page=single_page,
                     beers_html_tags=beers_html_tags,
                     beer_name_tags=beer_name_tags,
                     beer_description_tags=beer_description_tags,
                     kill=kill)



def TiredHands():
    TH.run()

if __name__ == '__main__':
    import logging
    logLevel=logging.DEBUG
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)
    TiredHands()