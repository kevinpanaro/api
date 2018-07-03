import logging
from helpers.save_lanes import save_lanes

class InvalidHoursFormat(Exception):
    pass

class InvalidDay(Exception):
    pass

class InvalidHours(Exception):
    pass

class InvalidPhoneNumber(Exception):
    pass

class Bowling():
    def __init__(self, name, address, phone, hours={}):
        self.name = name
        self.address = address
        self.phone = self.validate_phone(phone)
        self.hours = self.validate_lane_hours(hours)


    def set_hours(self, hours):
        self.hours = self.validate_lane_hours(hours)

    def get_hours(self, day=None):
        if day:
            return(self.hours[day])
        else:
            return(self.hours)

    def __repr__(self):
        return(self.name)

    def get_name(self):
        return(self.name)

    def get_address(self):
        return(self.address)

    def set_phone_number(self, phone):
        self.phone = self.validate_phone(phone)

    def get_phone_number(self):
        return(self.phone)

    def save_hours(self):
        data = {"name": self.name,
                "address": self.address,
                "phone": self.phone,
                "hours": self.hours}

        file_name = "_".join(self.name.split(" ")) + '.json'
        save_lanes(data, file_name.lower())

    def validate_phone(self, phone):
        ''' validates the phone number '''
        phone_number = ""
        for char in list(phone):
            if char.isdigit():
                phone_number += char
        if len(phone_number) in [10, 11]:
            return phone_number
        else:
            raise InvalidPhoneNumber()

    def validate_lane_hours(self, hours):
        ''' validates the hours dictionary'''

        def validate_hours(times, day):
            from datetime import datetime
            start, stop = times
            start = datetime.strptime(start, "%H:%M")
            stop = datetime.strptime(stop, "%H:%M")
            if stop == datetime(1900, 1, 1, 0, 0):
                return True
            elif start < stop:
                return True
            else:
                raise InvalidHours("Start time is before stop time for {}".format(day))

        if isinstance(hours, dict):
            pass
        else:
            raise InvalidHoursFormat("Hours are type, {}. Need dictionary.".format(type(hours)))

        weekdays = ['Sunday',    'Sun',
                    'Monday',    'Mon',
                    'Tuesday',   'Tue',
                    'Wednesday', 'Wed',
                    'Thursday',  'Thu',
                    'Friday',    'Fri',
                    'Saturday',  'Sat',
                    ]
        for day in hours.keys():
            if day.title() in weekdays and validate_hours(hours[day], day):
                continue
            else:
                raise InvalidDay("{} not a valid day.".format(day))

        return(hours)
