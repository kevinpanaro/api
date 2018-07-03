import logging
import re
from datetime import date
from helpers.url_pull import beautiful_url
from helpers.unicode_helper import unicode_to_ascii
from helpers.save_beer import save_beer
from bowling import Bowling

class DevonLanes(Bowling):


    def __init__(self):
        '''self initializes, for devon lanes'''
        self.base_url = "https://devonlanes.com/"
        contact = "contact-location"
        self.contact_url = "".join([self.base_url, contact])
        self._contact_info()
        self._hours()
        Bowling.__init__(self, self.name, self.address, self.phone, self.hours)

    def _contact_info(self):

        contact_html = beautiful_url(self.contact_url)

        name, address_p1, address_p2, phone = tuple(contact_html.find_all('p', {'style': 'margin-bottom: 0px ! important;'}))

        name = name.get_text()
        address_p1 = address_p1.get_text()
        address_p2 = address_p2.get_text()
        address = " ".join([address_p1, address_p2])
        phone = phone.get_text()

        self.name = name
        self.address = address
        self.phone = phone

    def _hours(self):

        devon_lanes_html = beautiful_url(self.base_url)

        hours = devon_lanes_html.find("div", {"class": "tve_cb_cnt tve_empty_dropzone"})
        list_of_hours = (str(hours).split('strong'))

        hours = {'Monday': ["11:00", "00:00"],
                 'Tuesday': ["09:00", "23:00"],
                 'Wednesday': ["09:00", "23:00"],
                 'Thursday': ["11:00", "00:00"],
                 'Friday': ["11:00", "00:00"],
                 'Saturday': ["10:00", "00:00"],
                 'Sunday': ["10:00", "22:00"],
                 }

        self.hours = hours

def devon_lanes():
    return(DevonLanes())

if __name__ == '__main__':
    devon_lanes()