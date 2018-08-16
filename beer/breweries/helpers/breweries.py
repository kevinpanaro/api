import helpers

class Brewery():

    def __init__(self, brewery_name: str, base_url: str, cookies: list, javascript: bool, save_file: str,
                 locations: dict, single_page: bool, beers_html_tags,
                 beer_name_tags, beer_description_tags, beer_brewery_tags = None,beer_abv_tags = None,
                 beer_ibu_tags = None, beer_hops_tags = [], beer_malts_tags = [],
                 beer_avail_tags = [], beer_style_tags = None, beer_multi_page_tags = None, kill = []):

        self.brewery_name = brewery_name            # name of the brewery
        self.base_url = base_url                    # base url for the brewery
        self.cookies = cookies                      # list of cookies
        self.javascript = javascript                # bool determining if javascript is needed
        self.save_file = save_file                  # end save file name
        self.locations = locations                  # list of brewery locations
        self.single_page = single_page              # bool whether all beers are on the same page
        self.beers_html_tags = beers_html_tags      # parent html tag that encompasses all beers on a html site
        self.beer_name_tags = beer_name_tags        # html tags for the name of the beer
        self.beer_description_tags = beer_description_tags # html tags for the description of the beer
        self.beer_brewery_tags = beer_brewery_tags  # html tags if location has more than just their beer on tap
        self.beer_abv_tags = beer_abv_tags          # html tags for the abv of the beer
        self.beer_ibu_tags = beer_ibu_tags          # html tags for the ibu of the beer
        self.beer_hops_tags = beer_hops_tags        # html tags for the hops of the beer
        self.beer_malts_tags = beer_malts_tags      # html tags for the malts of the beer
        self.beer_avail_tags = beer_avail_tags      # html tags for the availability of the beer
        self.beer_style_tags = beer_style_tags      # html tags for the style of the beer
        self.beer_multi_page_tags = beer_multi_page_tags    # html tags for urls of the beers if not single_page
        self.kill = kill                            # kill if these are found

        self.beer_name = None
        self.beer_description = None
        self.beer_brewery = self.brewery_name
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
                  "establishment": self.brewery_name, 
                  "id": helpers.b_id()[self.brewery_name], 
                  "type": "establishment"}

        helpers.save_beer(output, self.save_file)

    def get_beers(self, location_url):
        self.get_beers_list(location_url)

        _id = helpers.get_id("beer_id")
        for beer in self.beers:
            """
            At this point it is required that beer
            either be, or become a bs4 object.
            self.beers will be a list of bs4 objects,
            or a list of urls to specific beer pages. 
            """

            #
            if helpers.valid_url(beer):
                beer = helpers.beautiful_url(url=beer, 
                                     cookies=self.cookies, 
                                     javascript=self.javascript)

            if self.single_page: # will get rid off
                try:
                    self.set_all_beer_info(beer)

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

    def set_all_beer_info(self, beer):
        """ 
        This attempts to set all the beer info from the tags provided
        
        :param beer: a specific beers bs4 object
        :returns: all beer info (by setting by reference (?))
        """
        def try_to_set(beer_value, beer_value_tags):
            """
            value is an beer part, eg. name, brewery, abv...
            """
            try:
                beer_value = self.get_beer_info(beer, beer_value_tags)
            except:
                pass
            return(beer_value)

        self.beer_name = try_to_set(self.beer_name, self.beer_name_tags)
        self.beer_description = try_to_set(self.beer_description, self.beer_description_tags)
        self.beer_brewery = try_to_set(self.beer_brewery, self.beer_brewery_tags)
        self.beer_abv = try_to_set(self.beer_abv, self.beer_abv_tags)
        self.beer_ibu = try_to_set(self.beer_ibu, self.beer_ibu_tags)
        self.beer_hops = try_to_set(self.beer_hops, self.beer_hops_tags)
        self.beer_malts = try_to_set(self.beer_malts, self.beer_malts_tags)
        self.beer_avail = try_to_set(self.beer_avail, self.beer_avail_tags)
        self.beer_style = try_to_set(self.beer_style, self.beer_style_tags)


