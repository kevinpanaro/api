from helpers.breweries import Brewery

base_url = "http://www.tiredhands.com/{}/beers/"
brewery = "Tired Hands Brewery"
cookies = None
javascript = False
save_file = "tired_hands_class.json"
locations = {"Fermentaria": 'fermentaria',"Brew Cafe": "cafe"}
single_page = True
beers_html_tags = ('div', 'menu-item')
beer_name_tags = ('div', 'menu-item-title')
beer_description_tags = ('div', 'menu-item-description')
kill = ["***Other Beverages***", "***Sunday Brunch Beverages***"]


TiredHands = Brewery(brewery = brewery, 
                     base_url = base_url, 
                     cookies = cookies,
                     javascript = javascript,
                     save_file = save_file, 
                     locations = locations, 
                     single_page = single_page, 
                     beers_html_tags = beers_html_tags,
                     beer_name_tags = beer_name_tags,
                     beer_description_tags = beer_description_tags,
                     kill = kill)

TiredHands()