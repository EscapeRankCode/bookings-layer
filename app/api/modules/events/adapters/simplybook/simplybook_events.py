import json

import requests
from flask import request

from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.modules.events.api_events_interface import ApiEventsInterface
from app.api.utils import general_utils
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_tickets_response import EventTicketsResponse, Ticket, TicketType, TicketInfoOption, \
    TotalRules, TicketsGroup, TicketsSelection


class SimplybookApiEvents(ApiEventsInterface):

    def __init__(self):
        self.auth_module = SimplybookApiAuth()

    def get_event_tickets(self, api_request: EventTicketsRequest):
        credentials = self.auth_module.authorize(None)  # map with token and refresh_token

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_services_categories_list
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        category_id_to_search = api_request.bs_config['category_id']
        category_found = None

        # Search the game (category)
        for category in response_json["data"]:
            if category['id'] == category_id_to_search:
                category_found = category
                break

        services = []
        # Now we get the tickets' id (services)
        if category_found is not None:
            services = category_found['services']

        if len(services) > 0:
            # Get the tickets ('services')
            url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_services
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'X-Company-Login': credentials['company'],
                'X-Token': credentials['token']
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = json.loads(response.text)

            response_tickets = self.encapsulate_tickets(services, response_json, api_request)
            return response_tickets

        return None

    def encapsulate_tickets(self, services, response_json, event_tickets_request: EventTicketsRequest) -> EventTicketsResponse:
        tickets = []
        for service_id in services:

            ticket_found = None
            for json_ticket in response_json['data']:
                if json_ticket['id'] == service_id:
                    ticket_found = json_ticket
                    break

            """
            "id": 2,
            "name": "Proyecto Secreto - 2 Personas",
            "description": "",
            "price": 40.0,
            "currency": "EUR",
            "tax_id": null,
            "tax": null,
            "duration": 60,
            "buffer_time_after": 0,
            "recurring_settings": null,
            "picture": null,
            "picture_preview": null,
            "memberships": [],
            "is_active": true,
            "is_visible": true,
            "duration_type": null,
            "limit_booking": null,
            "min_group_booking": null
            """

            if ticket_found is not None:
                ticket_info = TicketInfoOption(False, 1, ticket_found['price'], '€')
                ticket = Ticket(ticket_found['name'], TicketType.option, ticket_info)
                tickets.append(ticket)

        total_rules = TotalRules(0, 0, 0, 0, 1, 1)
        tickets_group = TicketsGroup(tickets, total_rules, TicketsSelection(0, 0, 0, []))

        return EventTicketsResponse(event_tickets_request.event_id, tickets_group)
