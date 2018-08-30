from helpers.breweries import Brewery

base_url = "http://evilgeniusbeer.com/beers/{}"
brewery_name = "Evil Genius Brewery"
cookies = None
javascript = False
save_file = "evil_genius_class.json"
locations = {'Fishtown': ""}
single_page = True
beers_html_tags = ("div", "beer")
beer_name_tags = ("h2", "beer-title")
beer_description_tags = ("div", "col col-1-3")
beer_style_tags = ("h4", "beer-style")


EvilGenius = Brewery(brewery_name=brewery_name,
                     base_url=base_url,
                     cookies=cookies,
                     javascript=javascript,
                     save_file=save_file,
                     locations=locations,
                     single_page=single_page,
                     beers_html_tags=beers_html_tags,
                     beer_name_tags=beer_name_tags,
                     beer_description_tags=beer_description_tags,
                     beer_style_tags=beer_style_tags,
                     )

EvilGenius.run()
