import json

from flask import request

from app.api.modules.events.adapters.maximum.maximum_events import MaximumApiEvents
from app.api.utils import general_utils
from app.models.requests.event_form_request import EventFormRequest
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_tickets_response import EventTicketsResponseEncoder, EventTicketsResponse


class ApiEventsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiEvents(metaclass=ApiEventsMeta):
    def __init__(self):
        self.maximum_api_events = MaximumApiEvents()

    def get_event_tickets(self, api_request: request):
        event_tickets_request = EventTicketsRequest(api_request.json['data'])

        # Depending on the booking system
        if event_tickets_request.booking_system_id == general_utils.BS_ID_MAXIMUM:
            tickets = self.maximum_api_events.get_event_tickets(event_tickets_request)
            return json.dumps(tickets.to_json())

        return "Event Tickets Error", 400

    def get_event_form(self, api_request: request):
        event_form_request = EventFormRequest(api_request.json['data'])

        # Depending on the booking system
        if event_form_request.booking_system_id == general_utils.BS_ID_MAXIMUM:
            form = self.maximum_api_events.get_event_form(event_form_request)
            print("FORM TO JSON")
            print(str(form.to_json()))
            return json.dumps(form.to_json())

        return "Event Form Error", 400


