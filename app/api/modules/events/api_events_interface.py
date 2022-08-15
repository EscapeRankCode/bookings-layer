from flask import request

from app.models.requests.event_form_request import EventFormRequest
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_form_response import EventFormResponse, FieldType, Field
from app.models.responses.event_tickets_response import EventTicketsResponse


class ApiEventsInterface:
    #  -- EVENT INFO --
    def get_event_info(self, event_ticket_request: EventTicketsRequest, date_string):
        pass

    #  -- EVENT TICKETS --
    def get_event_tickets(self, api_request: request):
        pass

    def encapsulate_event_tickets(self, event, event_tickets_request: EventTicketsRequest) -> EventTicketsResponse:
        pass

    #  -- EVENT FORM --
    def get_event_form(self, api_request: request):
        pass

    def encapsulate_event_form(self, form, event_form_request: EventFormRequest) -> EventFormResponse:
        pass

    def translate_type(self, bs_type: str) -> FieldType:
        pass

    def field_has_to_enter_in_form(self, bs_field, field_type: FieldType) -> bool:
        return True  # By default :)

    def encapsulate_field_type_check(self, bs_field, extra_info) -> Field:
        pass

    def encapsulate_field_type_text(self, bs_field, extra_info) -> Field:
        pass

    def encapsulate_field_type_number(self, bs_field, extra_info) -> Field:
        pass

    def encapsulate_field_type_select(self, bs_field, extra_info) -> Field:
        pass

    def encapsulate_field_type_date(self, bs_field, extra_info) -> Field:
        pass

    def encapsulate_field_type_unknown(self, bs_field, extra_info) -> Field:
        pass
