from bs4 import BeautifulSoup as bs
from requests import get, Request, Session, cookies
from contextlib import closing

def beautiful_url(url, cookie=False):
    '''simple url grab but also closes nicely and beautiful soups it'''
    try:
        if cookie:
            name, content, domain, path = cookie
            jar = cookies.RequestsCookieJar()
            jar.set(name, content, domain=domain, path=path) 
            req = Request('GET', url, cookies=jar)
            req = req.prepare()
            s = Session()
            r = s.send(req)
            if is_good_response(r):
                souped_url = bs(r.text, "html.parser")
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

def is_good_response(resp):
    content_type = resp.headers["Content-Type"].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
