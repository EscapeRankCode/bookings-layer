import json
from json import JSONEncoder


class Event:
    def __init__(self, time, event_id: str, availability: int):
        self.time = time
        self.event_id = event_id
        self.availability = availability

    def __iter__(self):
        yield from {
            "time": self.time,
            "event_id": self.event_id,
            "availability": self.availability
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class Day:
    def __init__(self, year: int, month: int, day: int, day_availability: int, events):
        self.year = year
        self.month = month
        self.day = day
        self.day_availability = day_availability
        self.events = events

    def __iter__(self):
        yield from {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "day_availability": self.day_availability,
            "events": self.events
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class Calendar:
    def __init__(self, timezone, days):
        self.timezone = timezone
        self.days = days

    def __iter__(self):
        yield from{
            "timezone": self.timezone,
            "days": self.days
        }

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class CalendarAvailabilityResponse:
    def __init__(self, booking_system_id, bs_config_id, calendar: Calendar) -> None:
        self.booking_system_id = booking_system_id
        self.bs_config_id = bs_config_id
        self.calendar = calendar

    def __iter__(self):
        yield from{
            "booking_system_id": self.booking_system_id,
            "bs_config_id": self.bs_config_id,
            "calendar": self.calendar
        }

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class CalendarAvailabilityResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
