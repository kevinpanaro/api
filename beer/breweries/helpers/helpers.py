import os
import json
import re
import requests
import logging
import time
import pdb
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession 
from contextlib import closing

logging = logging.getLogger(__name__)

def get_id(file_name):
    """
    Opens and returns the next id number for the next beer.
     
    :param file_name: the file name for an id file
    :return: the number in the id file
    """
    logging.debug("beginning get_beer_id")
    path = os.path.dirname(os.path.realpath(__file__))

    full_id_path = os.path.join(path, 'tmp', file_name)

    if not os.path.exists(full_id_path):
        set_id(file_name)

    with open(full_id_path, 'r') as f:
        last_id = f.read()

    last_id = int(last_id)
    logging.debug(f"{file_name} found: {last_id}")
    return(last_id)

def reset_id():
    """
    Resets the id of all id files in /tmp/ to one, using set_id()
    """
    logging.info(f"Resetting all files")
    path = os.path.dirname(os.path.realpath(__file__))
    for _, _, all_files in os.walk(os.path.join(path, 'tmp')):
        pass
    for file in all_files:
        logging.debug(f"Resetting {file}")
        set_id(file_name = file)


def set_id(file_name: str, starting_id = 1):
    """
    Sets the id to the arg value.

    :param file_name: the file name for an id file
    :param starting_id: the number to set the id file to (optional)
    """
    logging.debug("starting set_id")
    path = os.path.dirname(os.path.realpath(__file__))

    full_id_path = os.path.join(path, 'tmp', file_name)
    logging.debug(f"{full_id_path}")

    with open(full_id_path, 'w+') as f:
        f.write(str(starting_id))
        logging.debug(f"wrote {starting_id} to {file_name}")



def b_id():
    """ 
    Theres a better way to do this, but for now it's hard coded, shoot me.

    :return: List of breweries, with cooresponding id values. Manually updated.
    """
    brewery_id = {"Tired Hands Brewery": 1,
                "Equinox Brewing": 2,
                "Dock Street": 3,
                "Evil Genius Brewery": 4,
                "The Mayor of Old Town": 5,
                "Monk's Cafe": 6,
                "Odell Brewing": 7}

    return(brewery_id)


def beautiful_url(url: str, cookies: list = False, 
                  javascript: bool = False) -> "BeautifulSoup Object":
    """
    simple url grab but also closes 
    nicely and beautiful soups it

    :param url: the string url to scrape
    :param cookies: a list of cookies (optional)
    :param javascript: a bool to indicate if javascript is present on the url page. (optional)
    :return: a BeautifulSoup Object
    """

    def is_good_response(resp):
        content_type = resp.headers["Content-Type"].lower()
        if resp.status_code != 200:
            logging.warn(f"Status Code: {resp.status_code}")
        else:
            logging.debug(f"Status Code: {resp.status_code}")
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find("html") > -1)


    cookiejar = requests.cookies.RequestsCookieJar()

    if cookies:
        logging.info("Prepping cookies...")
        for cookie in cookies:
            cookiejar.set(name=cookie['name'],
                          value=cookie['value'],
                          domain=cookie['domain'],
                          path=cookie['path'],
                          )

    if javascript:
        session = HTMLSession()
        resp = session.get(url, cookies=cookiejar)

        resp.html.render()
        if is_good_response(resp):
            souped_url = bs(resp.html.html, "html.parser")
            logging.debug("Successfull parse of url")
            return souped_url
        else:
            return None
        
    with closing(requests.get(url, cookies=cookiejar)) as resp:
        if is_good_response(resp):
            souped_url = bs(resp.text, "html.parser")
            logging.debug("Successfull parse of url")
            return souped_url
        else:
            return None



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

    :param _id: the beer id value 
    :param _type: the beer type value
    :param beer_name: the name of the beer
    :param beer_description: the description of the beer
    :param beer_brewery: the brewery of the beer
    :param beer_abv: the abv of the beer (optional)
    :param beer_ibu: the ibu of the beer (optional)
    :param beer_hops: the hops of the beer (optional)
    :param beer_malts: malts of the beer (optional)
    :param beer_avail: the availability of the beer (optional)
    :param beer_style: the style of the beer (optional)
    :return: a correctly formatted dict
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
             "beer_style": re.compile("[\w]+[\w\s]?[\w]+"),
             "beer_ibu": re.compile("[\d]+"),
             }

    def search_description(search_term, search_bank: list,
                           beer_description: str) -> list:
        """
        This is a function to return a list of items in the beer description.

        Args:
                 search_term: the variable we're searching for
                 search_bank: the bank of variables we are 
                              iteration through
            beer_description: the description provided
                              by the beer

        Returns:
            A list of terms found in the beer_description
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

        Args:
            beer_style: a list of styles

        Returns:
            non duplicate styles (list or str)
        """
        if isinstance(beer_style, str):
            try:
                return(REGEX["beer_style"].search(beer_style).group(0).strip())
            except:
                return(None)

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
    
    def ibu_cleaner(beer_ibu) -> int:
        try:
            beer_ibu = int(REGEX["beer_ibu"].search(beer_ibu).group(0).strip())
        except:
            pass
        return(beer_ibu)

    beer_abv = abv_cleaner(beer_abv)

    # I have no way to implement this right now
    if beer_ibu:
        beer_ibu = ibu_cleaner(beer_ibu)

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
