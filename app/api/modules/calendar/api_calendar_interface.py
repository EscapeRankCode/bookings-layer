from flask import request

from app.models.requests.calendar_availability_request import CalendarAvailabilityRequest
from app.models.responses.calendar_availability_response import CalendarAvailabilityResponse


class ApiCalendarInterface:
    def get_calendar_availability(self, api_request: CalendarAvailabilityRequest):
        pass

    def encapsulate_calendar_availability(self, availability, request: CalendarAvailabilityRequest) -> CalendarAvailabilityResponse:
        pass
