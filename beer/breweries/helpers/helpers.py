import os
import json
import re
import logging
from bs4 import BeautifulSoup as bs
import requests
from contextlib import closing

logging = logging.getLogger(__name__)

def b_id():
    """ 
    Theres a better way to do this, but
    for now it's hard coded, shoot me.
    """
    brewery_id = {"Tired Hands Brewery": 1,
                "Equinox Brewing": 2,
                "Dock Street": 3,
                "Evil Genius Brewery": 4,
                "The Mayor of Old Town": 5,
                "Monk's Cafe": 6,
                "Odell Brewing": 7}

    return(brewery_id)


def beautiful_url(url: str, cookie: bool = False) -> "BeautifulSoup Object":
    """
    simple url grab but also closes 
    nicely and beautiful soups it
    """

    def is_good_response(resp):
        content_type = resp.headers["Content-Type"].lower()
        if resp.status_code != 200:
            logging.warn(f"Status Code: {resp.status_code}")
        else:
            logging.info(f"Status Code: {resp.status_code}")
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find("html") > -1)
        
    try:
        if cookie:
            logging.critical("Cookies don't work right now.")
            # name, content, domain, path = cookie
            # jar = cookies.RequestsCookieJar()
            # jar.set(name=name, value=content, domain=domain, path=path)
            cookiejar = requests.cookies.RequestsCookieJar()
            cookiejar.set(name="odAccess", value="true", domain="www.odellbrewing.com", path="/")
            req = requests.Request(method="GET", url=url, cookies=cookiejar)

            prepared_req = req.prepare()
            
            s = requests.Session()
            resp = s.send(prepared_req)
            # print(resp)
            if is_good_response(resp):
                souped_url = bs(resp.text, "html.parser")

                return souped_url
            else:
                return None

        with closing(requests.get(url)) as resp:
            if is_good_response(resp):
                souped_url = bs(resp.text, "html.parser")
                logging.info("Successfull parse of url")
                return souped_url
            else:
                return None

    except Exception as err:
        logging.warn(f"{type(err)}: {err}")


def save_beer(data: dict, file_name: str) -> None:
    """
    This function saves the formatted beer json
    to the defined path. In this case ../../taps
    """
    path = os.path.dirname(os.path.realpath(__file__))

    save_path = os.path.join(path, "../../taps", file_name)

    if os.path.exists(save_path):
        os.remove(save_path)


    with open(save_path, "w+") as f:
        f.write(json.dumps(data))

    logging.info(f"Saved: {file_name}")


def format_beer_dict(_id: int, _type: str, 
                     beer_name: str, 
                     beer_description: str,
                     beer_brewery: str, 
                     beer_abv: float = None,
                     beer_ibu: int = None, 
                     beer_hops: list = [],
                     beer_malts: list = [], 
                     beer_avail: list = [],
                     beer_style: list = []) -> dict:
    """
    This takes all information collected and formats 
    the data so that it is the same format for all 
    scraped beer data

    The name of the beer, description and brewery are required. 
    All other aspects are optional, and if not provided will try
    to be determined from the beer description.

    Proposed Output:
    beers =[
        { 
            "id": 1 # for api
            "type": "beer"
            "beer": "name of this beer",
            "brewery": "name of this beer"s brewery", (if it"s a bar like Monks)
            "description": "description of this beer",
            "stats": {
                "abv": "abv of this beer", # formatted as only a float
                "ibu": "ibu of this beer", 
                "hops": ["types of hops in this beer"], # as a list
                "malts": ["types of malts in this beer"], # as a list
                "availability": "when this beer is available",
                "style": "the style of this beer",
            }
        }, # and so on for other beers
    ]
    """

    ###############################################
    ## These will probably be put in a different ## 
    ## script for ease of reading.               ##
    ###############################################

    # subject to change
    AVAILABILITY =   ["january", "jan"
                      "february", "feb",
                      "march", "mar",
                      "april", "apr",
                      "may",
                      "june", "jun",
                      "july", "jul",
                      "august", "aug",
                      "september", "sep", "sept",
                      "october", "oct",
                      "november", "nov",
                      "december", "dec",
                      "winter", "spring",
                      "summer", "fall",
                      "year round",
                      ]
    # source https://www.morebeer.com/articles/homebrew_beer_hops
    HOPS = ["admiral", "agnus", "ahtanum", "alpharoma", "amarillo", 
            "amethyst", "apollo", "aramis", "atlas", "aurora", "beata", 
            "belma", "bitter gold", "boadicea", "bobek", "bouclier", 
            "bramling cross", "bravo", "brewers gold", "british kent goldings", 
            "bullion", "calicross", "california cluster", "calypso", "cascade", 
            "cashmere", "cekin", "celeia", "centennial", "challenger", 
            "chelan", "chinook", "cicero", "citra", "cluster", "cobb’s golding", 
            "columbia", "columbus", "comet", "crystal", "dana", "delta", 
            "dr. rudi", "early green", "el dorado", "ella", "endeavour", 
            "equinox", "eroica", "falconer’s flight", "first gold", "flyer", 
            "fuggle", "galaxy", "galena", "glacier", "golding", "green bullet", 
            "hallertau", "hbc 342 experimental", "helga", "herald", "herkules", 
            "hersbrucker", "horizon", "huell melon", "ivanhoe", "jester", 
            "junga", "kazbek", "kohatu", "liberty", "lubelski", "magnum", 
            "mandarina bavaria", "mathon", "marynka", "meridian", "merkur", 
            "millennium", "mittelfruh", "mosaic", "motueka", "mt. hood", 
            "mt. rainier", "nelson sauvin", "newport", "northdown", 
            "northern brewer", "nugget", "opal", "orbit", "orion", "outeniqua", 
            "pacific gem", "pacific jade", "pacific sunrise", "pacifica", 
            "palisade", "perle", "phoenix", "pilgrim", "pilot", "pioneer", 
            "polaris", "premiant", "pride of ringwood", "progress", "rakau", 
            "riwaka", "saaz", "santiam", "saphir", "satus", "select", 
            "serebrianka", "simcoe", "sladek", "smaragd", "sonnet", "sorachi ace", 
            "southern brewer", "southern cross", "southern promise", 
            "southern star", "sovereign", "spault", "spaulter select", "sterling", 
            "strickelbract", "strisselspault", "styrian gold", "styrian goldings", 
            "summer", "summit", "super galena", "super pride", "sussex", "sybilla", 
            "sylva", "tahoma", "tardif de burgogne", "target", "taurus", "warrior", 
            "whitbread goldings", "willamette", "yakima cluster", "zenith", "zythos",
            "callista", "ariana", "idaho7"]

    # source https://cotubrewing.com/homebrewing/malt-profiles/
    MALTS = ["amber", "aromatic", "belgian", "biscuit", "black barley",
             "black", "brown", "crystal", "caramel", "caramunich", "carapils",
             "chocolate", "english pale", "flaked maize", "flaked oats",
             "flaked rye", "flaked wheat", "honey", "lager", "munich",
             "pale ale malt", "pilsner", "pils", "roasted barley", "rye",
             "smoked", "special b", "wheat", "rice", "victory", "vienna",
             ]

    # source https://en.wikipedia.org/wiki/List_of_beer_styles
    STYLES = ["altbier", "amber ale", "barley wine", "berliner weisse", 
              "bière de garde", "bitter", "blonde ale", "bock", "brown ale", 
              "california common/steam beer", "cream ale", "dortmunder export", 
              "doppelbock", "double ipa", "dunkel", "dunkelweizen", "eisbock", 
              "flanders red ale", "golden ale", "summer ale", "gose", "gueuze", 
              "hefeweizen", "helles", "india pale ale", "ipa", "kölsch", "lambic", 
              "light ale", "maibock", "helles bock", "malt liquor", "mild", 
              "oatmeal stout", "oktoberfestbier", "märzenbier", "old ale", "oud bruin", "pale ale", 
              "pilsener", "pilsner", "pils", "porter", "red ale", "roggenbier", "saison", 
              "scotch ale", "scottish ale", "stout", "schwarzbier", "vienna lager", "witbier", 
              "weissbier", "weizenbock", "strong ale", ]
    
    REGEX = {"beer_abv": re.compile("([\d]+\.[\d]\s*|[\d]+\s*)(?=%)"),
             "beer_style": re.compile("[\D]+"),
             }

    def search_description(search_term, search_bank: list,
                           beer_description: str) -> list:
        """
        This is a function to return a list of items in the beer description.
        """
        # if it exists return, it
        if search_term:
            return search_term

        else:   # if it doesn't exist, try to find it.
            search_term = []
            for item in search_bank: # ([\d]+\.[\d]\s*|[\d]+\s*)(?=%)%
                regex = re.compile(item + "(?=[\W])|(?<=[\W])" + item)
                item = regex.search(beer_description.lower())
                if item:
                    search_term.append(item.group(0))

            return search_term

    def style_cleaner(beer_style: list) -> str:
        """
        most beers fall under one category.
        this will help with cleaning up a beer 
        thats ['api', 'double ipa'] when it's really just
        a ['double api']
        """
        if isinstance(beer_style, str):
            return(beer_style.strip('.'))

        dupes = []
        beer_style_copy = beer_style[:]

        for style in beer_style:
            for style_copy in beer_style_copy:
                if style != style_copy:
                    if style in style_copy:
                        dupes.append(style)

        for dupe in dupes:
            beer_style.remove(dupe)

        if len(beer_style) == 1:
            return(beer_style[0])
        else:
            return(beer_style)

    def abv_cleaner(beer_abv) -> float:
        try:    
            beer_abv = float(REGEX["beer_abv"].search(beer_abv).group(0).strip())
        except:
            try:
                beer_abv = float(REGEX["beer_abv"].search(beer_description).group(0).strip())
            except:
                pass
            pass
        return(beer_abv)
    

    beer_abv = abv_cleaner(beer_abv)

    # I have no way to implement this right now
    if beer_ibu:
        pass

    beer_hops = search_description(beer_hops, HOPS, beer_description)

    beer_malts = search_description(beer_malts, MALTS, beer_description)

    beer_avail = search_description(beer_avail, AVAILABILITY, beer_description)

    beer_style_from_name = search_description(beer_style, STYLES, beer_name)

    # the name probably has the best description for the type of beer it is.
    if beer_style_from_name:
        beer_style = beer_style_from_name
    else:
        beer_style = search_description(beer_style, STYLES, beer_description)

    beer_style = style_cleaner(beer_style)

    beer_dict = {
                    "id": _id,
                    "type": _type, 
                    "beer": beer_name,
                    "description": beer_description,
                    "brewery": beer_brewery,
                    "stats":
                        {
                            "abv": beer_abv,
                            "ibu": beer_ibu,
                            "hops": beer_hops,
                            "malts": beer_malts,
                            "availability": beer_avail,
                            "style": beer_style,
                        },
                }

    return(beer_dict)