import json
from datetime import datetime

import requests
from flask import request

from app.api.modules.events.api_events_interface import ApiEventsInterface
from app.api.utils import general_utils
import app.api.utils.apis_strings_utils as apis_strings
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_tickets_response import EventTicketsResponse, TicketInfoOption, Ticket, TicketType, \
    TotalRules, TicketsGroup


class MaximumApiEvents(ApiEventsInterface):

    # --------- EVENT TICKETS ---------
    def get_event_info(self, quest_id, date_string):
        """
        Returns the event (slot) information looking at the
        :param quest_id:
        :param date_string: day where the event belongs to, in format %d.%m.%y
        :return:
        """
        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_time_table

        payload = json.dumps({
            "id": quest_id,
            "date": date_string
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        time_table = json.loads(response.text)

        day = time_table['scheduleDay']
        price_blocks = day['proposalPriceRangeBlocks']
        for block in price_blocks:
            events = block['proposals']
            for event in events:
                if event['id'] == quest_id:
                    return event

        return None

    def get_event_tickets(self, api_request: EventTicketsRequest):
        event_date = datetime.strptime(api_request.event_date, general_utils.MAXIMUM_DATE_FORMAT)
        print("-- Event date:")
        print(event_date)
        get_event_info_date = event_date.strftime("%d.%m.%Y")

        event = self.get_event_info(api_request.bs_config['room'], get_event_info_date)
        print("-- Event:")
        print(event)

        response = self.encapsulate_event_tickets(event, api_request)
        print("-- Encapsulate response:")
        print(response)

        return response

    def encapsulate_event_tickets(self, event, event_tickets_request: EventTicketsRequest) -> EventTicketsResponse:

        # TODO: What happens if 'special' or 'multiSlot' are true (maximum)

        print("-- Event info:")
        print(event)

        if not event['multiSlot']:

            tickets = []

            # "2": 70.0
            # "3": 70.0
            # "4": 70.0
            prices = event['prices']
            print("-- Prices:")
            print(prices)

            for price in prices:
                ticket_info = TicketInfoOption(False, 1, float(prices[price]), "€")
                ticket = Ticket(price + apis_strings.BS_MAXIMUM_TICKET_PEOPLE, TicketType.option, ticket_info)
                tickets.append(ticket)

            total_rules = TotalRules(0, 0, 0, 0, 1, 1)

            tickets_group = TicketsGroup(tickets, total_rules)
            tick_groups = [tickets_group]

            return EventTicketsResponse(event['id'], tick_groups)

# TODO:
'''
    - A partir de los datos de get event info, encapsular los precios (dentro de la respuesta "event")
    - NO HACE FALTA HACER NINGUNA OTRA LLAMADA
'''

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
