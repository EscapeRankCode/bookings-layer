from flask import Flask, request

from app.api.modules.calendar.adapters.maximum.maximum_calendar import MaximumApiCalendar
from app.api.utils import general_utils
from app.models.requests.calendar_availability_request import CalendarAvailabilityRequest


class ApiCalendarMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiCalendar(metaclass=ApiCalendarMeta):

    def __init__(self):
        self.maximum_api_calendar = MaximumApiCalendar()

    """
    Endpoint: /calendar_availability
    Data:
    [
        'start_date' : date - string format %d/%m/%Y
        'end_date' : date - string format %d/%m/%Y
        'booking_system_id' : booking system identifier - int
            // defined in general utils
        'bs_config' : date in string format
            --> Maximum:
            [
                'config_id' : int - escaperank configuration id
                'room' : int - maximum escape id
                'city_id' : int - maximum location id (city)
            ]
    ]
    """
    def get_calendar_availability(self, api_request: request):
        print("JSON:")
        print(api_request.json)
        calendar_availability_request = CalendarAvailabilityRequest(api_request.json['data'])

        availability = None
        # Depending on the booking system
        if calendar_availability_request.booking_system_id == general_utils.BS_ID_MAXIMUM:
            print("MAXIMUM ESCAPE detected")
            availability = self.maximum_api_calendar.get_calendar_availability(calendar_availability_request)

        return availability
