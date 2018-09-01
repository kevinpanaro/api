from helpers.breweries import Brewery

base_url = "https://equinoxbrewing.com/"
brewery_name = "Equinox Brewing"
cookies = None
javascript = False
save_file = "equinox_class.json"
locations = {"133 Remington Street, Fort Collins, CO 80524": ""}
single_page = False
beer_multi_page_tags = ("a", "tg-element-absolute")
beer_name_tags = ('h1', {'class': 'entry-title'})
beer_description_tags = ('div', {'class': 'entry-content content'})


Equinox = Brewery(brewery_name = brewery_name, 
                     base_url = base_url, 
                     cookies = cookies,
                     javascript = javascript,
                     save_file = save_file, 
                     locations = locations, 
                     single_page = single_page, 
                     beer_multi_page_tags = beer_multi_page_tags,
                     beer_name_tags = beer_name_tags,
                     beer_description_tags = beer_description_tags)

Equinox.run()