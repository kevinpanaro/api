import os
import json
import re
from bs4 import BeautifulSoup as bs
from requests import get, Request, Session, cookies
from contextlib import closing

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
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find("html") > -1)
        
    try:
        if cookie:
            name, content, domain, path = cookie
            jar = cookies.RequestsCookieJar()
            jar.set(name, content, domain=domain, path=path) 
            req = Request("GET", url, cookies=jar)
            req = req.prepare()
            s = Session()
            resp = s.send(req)

            if is_good_response(resp):
                souped_url = bs(resp.text, "html.parser")
                return souped_url
            else:
                return None

        with closing(get(url)) as resp:
            if is_good_response(resp):
                souped_url = bs(resp.text, "html.parser")
                return souped_url
            else:
                return None

    except Exception as e:
        print(e)


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


def format_beer_dict(_id: int, _type: str, 
                     beer_name: str, 
                     beer_description: str,
                     beer_brewery: str, 
                     beer_abv: float = None,
                     beer_ibu: int = None, 
                     beer_hops: list = [],
                     beer_malts: list = [], 
                     beer_avail: list = [],
                     beer_style: str = []) -> dict:
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
              "oktoberfestbier", "märzenbier", "old ale", "oud bruin", "pale ale", 
              "pilsener", "pilsner", "pils", "porter", "red ale", "roggenbier", "saison", 
              "scotch ale", "stout", "schwarzbier", "vienna lager", "witbier", 
              "weissbier", "weizenbock"]
    
    REGEX = {"beer_abv": re.compile("([\d]+\.[\d]\s*|[\d]+\s*)(?=%)"),
             "beer_style": re.compile("[\D]+"),
             }

    def search_description(search_term: list, search_bank: list,
                           beer_description: str) -> list:
        """
        This is a function to return a list of items in the beer description.
        """
        if search_term:
            return search_term
        else:
            for item in search_bank:
                regex = re.compile(item + "(?=[\W])")
                item = regex.search(beer_description.lower())
                if item:
                    search_term.append(item.group(0))
            return search_term

    try:
        beer_abv = float(beer_abv.strip().strip("%"))
    except:
        beer_abv = float(REGEX["beer_abv"].search(beer_description).group(0).strip())

    if beer_ibu == None:
        pass

    beer_hops = search_description(beer_hops, HOPS, beer_description)

    beer_malts = search_description(beer_malts, MALTS, beer_description)

    beer_avail = search_description(beer_avail, AVAILABILITY, beer_description)

    beer_style = search_description(beer_style, STYLES, beer_description)

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