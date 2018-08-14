import helpers

class Brewery():

    def __init__(self, brewery: str, base_url: str, cookies: list, javascript: bool, save_file: str,
                 locations: dict, single_page: bool, beers_html_tags,
                 beer_name_tags, beer_description_tags, beer_abv_tags = None,
                 beer_ibu_tags = None, beer_hops_tags = [], beer_malts_tags = [],
                 beer_avail_tags = [], beer_style_tags = None, beer_multi_page_tags = None, kill = []):
        self.brewery = brewery
        self.base_url = base_url
        self.cookies = cookies
        self.javascript = javascript
        self.save_file = save_file
        self.locations = locations
        self.single_page = single_page
        self.beers_html_tags = beers_html_tags
        self.beer_name_tags = beer_name_tags
        self.beer_description_tags = beer_description_tags
        self.beer_abv_tags = beer_abv_tags
        self.beer_ibu_tags = beer_ibu_tags
        self.beer_hops_tags = beer_hops_tags
        self.beer_malts_tags = beer_malts_tags
        self.beer_avail_tags = beer_avail_tags
        self.beer_style_tags = beer_style_tags
        self.beer_multi_page_tags = beer_multi_page_tags
        self.kill = kill

        self.beer_name = None
        self.beer_description = None
        self.beer_brewery = self.brewery
        self.beer_abv = None
        self.beer_ibu = None
        self.beer_hops = []
        self.beer_malts = []
        self.beer_avail = []
        self.beer_style = None


    def __call__(self):
        self.main()

    def main(self):
        output = []

        _id = helpers.get_id("location_id")

        for location, url in self.locations.items():
            self.return_beers = []

            location_url = self.base_url.format(url)
            self.get_beers(location_url)
            output.append({"location": location, 
                           "beers": self.return_beers, 
                           "id": _id,
                           "type": "location"})
            _id += 1

        helpers.set_id(file_name = "location_id", starting_id = _id)

        output = {"locations": output, 
                  "establishment": self.brewery, 
                  "id": helpers.b_id()[self.brewery], 
                  "type": "establishment"}

        helpers.save_beer(output, self.save_file)

    def get_beers(self, location_url):
        self.get_beers_list(location_url)

        _id = helpers.get_id("beer_id")
        for beer in self.beers:
            if self.single_page:
                try:
                    self.beer_name = self.get_beer_info(beer, self.beer_name_tags)
                    self.beer_description = self.get_beer_info(beer, self.beer_description_tags)

                    beer_dict = helpers.format_beer_dict(_id              = _id,
                                                         _type            = "beer",
                                                         beer_name        = self.beer_name,
                                                         beer_description = self.beer_description,
                                                         beer_brewery     = self.beer_brewery,
                                                         beer_abv         = self.beer_abv,
                                                         beer_ibu         = self.beer_ibu,
                                                         beer_hops        = self.beer_hops,
                                                         beer_malts       = self.beer_malts,
                                                         beer_avail       = self.beer_avail,
                                                         beer_style       = self.beer_style,)
                    self.return_beers.append(beer_dict)
                except:
                    pass
            else: # multipage, list of urls here
                beer_page = helpers.beautiful_url(url=beer, 
                                                  cookies=self.cookies, 
                                                  javascript=self.javascript)
            _id += 1

            
        helpers.set_id(file_name = "beer_id", starting_id = _id)


    def get_beers_list(self, location_url: str):
        """
        Returns a Beautiful Soup List or a list of urls

        """

        if self.single_page:
            data = helpers.beautiful_url(url=location_url, 
                                         cookies=self.cookies, 
                                         javascript=self.javascript)            
            tag, attribute = self.beers_html_tags
            self.beers = data.find_all(tag, attribute)
        else: # get a list of all the beer urls
            pass

    def get_beer_info(self, beer, tags):
        tag, attribute = tags
        return(beer.find(tag, attribute).get_text().strip())
