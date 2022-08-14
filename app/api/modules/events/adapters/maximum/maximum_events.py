import json
from datetime import datetime

import requests
from flask import request

from app.api.modules.events.api_events_interface import ApiEventsInterface
from app.api.utils import general_utils
import app.api.utils.apis_strings_utils as apis_strings
from app.models.requests.event_form_request import EventFormRequest
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_form_response import EventFormResponse, Field, FieldType
from app.models.responses.event_tickets_response import EventTicketsResponse, TicketInfoOption, Ticket, TicketType, \
    TotalRules, TicketsGroup, TicketInfoCounter, TicketInfoCheck


class MaximumApiEvents(ApiEventsInterface):

    def get_event_info(self, event_ticket_request: EventTicketsRequest, date_string):
        """
        Returns the event (slot) information looking at
        :param event_ticket_request: object received in the request
        :param date_string: day when the event belongs to, in format %d.%m.%y
        :return:
        """
        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_time_table

        payload = json.dumps({
            "id": event_ticket_request.bs_config['room'],
            "date": date_string
        })
        headers = {
            'Content-Type': 'application/json'
        }

        to_find_id = int(event_ticket_request.event_id)

        response = requests.request("POST", url, headers=headers, data=payload)

        time_table = json.loads(response.text)

        day = time_table['scheduleDay']
        price_blocks = day['proposalPriceRangeBlocks']
        for block in price_blocks:
            events = block['proposals']
            for event in events:
                if event['id'] == to_find_id:
                    return event

        return None

    # --------- EVENT TICKETS ---------
    def get_event_tickets(self, api_request: EventTicketsRequest) -> EventTicketsResponse:
        event_date = datetime.strptime(api_request.event_date, general_utils.MAXIMUM_DATE_FORMAT)

        get_event_info_date = event_date.strftime("%d.%m.%Y")

        event = self.get_event_info(api_request, get_event_info_date)

        response = self.encapsulate_event_tickets(event, api_request)

        return response

    def encapsulate_event_tickets(self, event, event_tickets_request: EventTicketsRequest) -> EventTicketsResponse:

        # TODO: What happens if 'special' or 'multiSlot' are true (maximum)

        if not event['multiSlot']:

            tickets = []
            prices = event['prices']

            for price in prices:

                ticket_info = TicketInfoOption(False, 1, float(prices[price]), "€")  # Good one (counter)
                # ticket_info = TicketInfoCounter(0, 4, 0, 1, 1, "€")  # Counter
                # ticket_info = TicketInfoCheck(False, 1, 1, "€")  # Check

                ticket = Ticket(price + apis_strings.BS_MAXIMUM_TICKET_PEOPLE, TicketType.option, ticket_info)  # Good one (counter)
                # ticket = Ticket(price + apis_strings.BS_MAXIMUM_TICKET_PEOPLE, TicketType.counter, ticket_info)  # Counter
                # ticket = Ticket(price + apis_strings.BS_MAXIMUM_TICKET_PEOPLE, TicketType.check, ticket_info)  # Check

                tickets.append(ticket)

            total_rules = TotalRules(0, 0, 0, 0, 1, 1)  # Good one
            # total_rules = TotalRules(1, 2, 1, 2, 1, 2)

            tickets_group = TicketsGroup(tickets, total_rules)
            tick_groups = [tickets_group]

            return EventTicketsResponse(str(event['id']), tick_groups)

    # --------- EVENT FORM ---------
    def get_event_form(self, event_form_request: EventFormRequest) -> EventFormResponse:
        """
        Returns the form list of fields
        :param event_form_request: object received in the request
        :return:
        """
        date_split = event_form_request.event_date.split('/')

        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_event_form

        payload = json.dumps({
            "language_code": "es",
            "quest_id": event_form_request.bs_config['room'],
            "proposal_id": int(event_form_request.event_id),
            "date": date_split[2] + "-" + date_split[1] + "-" + date_split[0]  # "2022-08-15"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        maximum_form = json.loads(response.text)['client_form']
        form = self.encapsulate_event_form(maximum_form, event_form_request)


    """
    {
        "key": "phone",
        "name": "Número de teléfono",
        "type": "text",
        "required": true,
        "options": null,
        "disabled": false
    }
    """

    def encapsulate_event_form(self, form, event_form_request: EventFormRequest) -> EventFormResponse:
        fields = []
        for maximum_field in form:
            field = Field()

    def translate_type(self, bs_type: str) -> FieldType:
        if bs_type == "text":
            return FieldType.text
        if bs_type == "select" or bs_type == "radio":
            return FieldType.select
        if bs_type == "checkbox":
            return FieldType.check

        # If type not matches with any defined type, we name it like 'unknown'
        return FieldType.unknown


'''
    def get_event_form(self, api_request: EventFormRequest):
        event_date = datetime.strptime(api_request.event_date, general_utils.MAXIMUM_DATE_FORMAT)

        event = self.get_event_info(api_request.bs_config['room'], get_event_info_date)

        language_code = "es"

        event_date_request = event_date.strftime("%Y-%m-%d")

        quest_id = str(api_request.bs_config['room'])

        proposal_id = api_request.event_id

        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_event_form

        payload = json.dumps({
            "language_code": language_code,
            "quest_id": quest_id,
            "proposal_id": proposal_id,
            "date": event_date_request
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        maximum_event_form = json.loads(response.text)

        response = self.encapsulate_event_form(maximum_event_form, api_request)
        return response
'''
