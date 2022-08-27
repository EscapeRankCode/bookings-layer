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
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "time": self.time,
            "event_id": self.event_id,
            "availability": self.availability
        }



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
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        events_json = []
        for event in self.events:
            events_json.append(event.to_json())
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "day_availability": self.day_availability,
            "events": events_json
        }


class Calendar:
    def __init__(self, timezone, days):
        self.timezone = timezone
        self.days = days

    def __iter__(self):
        yield from{
            "timezone": self.timezone,
            "days": self.days
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        days_json = []
        for day in self.days:
            days_json.append(day.to_json())

        return {
            "timezone": self.timezone,
            "days": days_json
        }


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
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class CalendarAvailabilityResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
