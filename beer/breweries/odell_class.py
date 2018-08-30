from helpers.breweries import Brewery

base_url = "https://www.odellbrewing.com/taproom{}/"
brewery_name = "Odell Brewing"
cookies = [{'name': 'odAccess', 'value': 'true', 'domain': 'www.odellbrewing.com', 'path': '/'}]
javascript = True
save_file = "odell_class.json"
locations = {"Fort Collins": "", "Denver": "-denver"}
single_page = True
beers_html_tags = ('div', {'class': 'item-bg-color menu-item'})
beer_name_tags = ('span', {'class': 'item'})
beer_description_tags = ('p', {'class': 'show-less item-title-color'})
beer_brewery_tags = ('span', {"class": "brewery-name-hideable brewery hide"})
beer_abv_tags = ('span', {'class': 'abv-hideable abv'})
beer_ibu_tags = ('span', {"class": "ibu-hideable ibu hide"})
beer_style_tags = ('span', {'class': 'beer-style-hideable beer-style'})

Odell = Brewery(brewery_name=brewery_name,
                     base_url=base_url,
                     cookies=cookies,
                     javascript=javascript,
                     save_file=save_file,
                     locations=locations,
                     single_page=single_page,
                     beers_html_tags=beers_html_tags,
                     beer_name_tags=beer_name_tags,
                     beer_description_tags=beer_description_tags,
                     beer_brewery_tags=beer_brewery_tags,
                     beer_abv_tags=beer_abv_tags,
                     beer_ibu_tags=beer_ibu_tags,
                     beer_style_tags=beer_style_tags,
                     )

Odell.run()
