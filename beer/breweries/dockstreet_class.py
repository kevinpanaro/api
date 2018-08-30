from helpers.breweries import Brewery

base_url = "http://www.dockstreetbeer.com/whats-on-tap/{}"
brewery_name = "Dock Street"
cookies = None
javascript = False
save_file = "dock_street_class.json"
locations = {"701 South 50th Street, Philadelphia, PA 19143": ""}
single_page = True
beers_html_tags = ("div", "menu-item")
beer_name_tags = ("div", "menu-item-title")
beer_description_tags = ("div", "menu-item-description")


DockStreet = Brewery(brewery_name=brewery_name,
                     base_url=base_url,
                     cookies=cookies,
                     javascript=javascript,
                     save_file=save_file,
                     locations=locations,
                     single_page=single_page,
                     beers_html_tags=beers_html_tags,
                     beer_name_tags=beer_name_tags,
                     beer_description_tags=beer_description_tags,
                     )

DockStreet.run()
