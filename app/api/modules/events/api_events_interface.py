from flask import request

from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_tickets_response import EventTicketsResponse


class ApiEventsInterface:
    def get_event_info(self, event_id, date_string):
        pass

    def get_event_tickets(self, api_request: request):
        pass

    def encapsulate_event_tickets(self, event, event_tickets_request: EventTicketsRequest) -> EventTicketsResponse:
        pass
