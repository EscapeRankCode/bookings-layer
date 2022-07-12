import json
from json import JSONEncoder

class Event:
    def __init__(self, time, event_id: int, availability: int):
        self.time = time
        self.event_id = event_id
        self.availability = availability


class Day:
    def __init__(self, year: int, month: int, day: int, day_availability: int, events):
        self.year = year
        self.month = month
        self.day = day
        self.day_availability = day_availability
        self.events = events


class Calendar:
    def __init__(self, timezone, days):
        self.timezone = timezone
        self.days = days


class CalendarAvailabilityResponse:
    def __init__(self, booking_system_id, bs_config_id, calendar: Calendar) -> None:
        self.booking_system_id = booking_system_id
        self.bs_config_id = bs_config_id
        self.calendar = calendar


class CalendarAvailabilityResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
