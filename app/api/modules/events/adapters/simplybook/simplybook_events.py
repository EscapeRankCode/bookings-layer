import json

import requests
from flask import request

from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.modules.events.api_events_interface import ApiEventsInterface
from app.api.utils import general_utils
from app.models.requests.event_form_request import EventFormRequest
from app.models.requests.event_tickets_request import EventTicketsRequest
from app.models.responses.event_form_response import EventFormResponse, FieldType, Field, FieldOption
from app.models.responses.event_tickets_response import EventTicketsResponse, Ticket, TicketType, TicketInfoOption, \
    TotalRules, TicketsGroup, TicketsSelection


class SimplybookApiEvents(ApiEventsInterface):

    def __init__(self):
        self.auth_module = SimplybookApiAuth()

    def get_event_tickets(self, api_request: EventTicketsRequest) -> EventTicketsResponse:
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

        # print("-- RESPONSE FROM <GET SERVICES CATEGORIES>")
        # print(response.text)

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

            # print("-- RESPONSE FROM <GET SERVICES>")
            # print(response.text)

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

            if ticket_found is not None:
                ticket_info = TicketInfoOption(False, 1, ticket_found['price'], '€')
                ticket = Ticket(ticket_found['name'], TicketType.option, ticket_info)
                tickets.append(ticket)

        total_rules = TotalRules(0, 0, 0, 0, 1, 1)
        tickets_group = TicketsGroup(tickets, total_rules, TicketsSelection(0, 0, 0, []))

        tickets_groups = [tickets_group]

        return EventTicketsResponse(event_tickets_request.event_id, tickets_groups)

    def get_event_form(self, api_request: EventFormRequest) -> EventFormResponse:
        # ----------------- Get the client fields
        credentials = self.auth_module.authorize(None)  # map with token and refresh_token

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_client_fields
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        client_json_fields = response_json['data']

        # ----------------- Get the tickets ('services') TO FIND THE SERVICE ID
        tickets_selection = json.loads(api_request.event_tickets[0]['tickets_selection'])
        selected_tickets = json.loads(tickets_selection['selected_tickets'])
        # ticket = json.loads()
        ticket_selected_name = selected_tickets[0]['ticket_name']

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_services
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        print("GET SERVICES RESPONSE\n")
        print(response.text)
        service_id = -1
        for service in response_json['data']:
            if service['name'] == ticket_selected_name:
                service_id = service['id']
                break


        print("Service is: " + str(service_id))
        print("TICKET NAME: " + ticket_selected_name)
        if service_id == -1:
            return None

        # ----------------- Get the additional fields for this service (ticket)
        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_additional_fields + "?filter[service_id]=" + str(service_id)
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        print("GET ADDITIONAL FIELDS RESPONSE\n")
        print(response.text)

        additional_json_fields = response_json['data']

        encapsulate_parameter = {
            "client_fields": client_json_fields,
            "additional_fields": additional_json_fields
        }

        form = self.encapsulate_event_form(encapsulate_parameter, api_request)
        return form

    def encapsulate_event_form(self, form, event_form_request: EventFormRequest) -> EventFormResponse:
        fields = []

        client_fields = form['client_fields']
        print(json.dumps(client_fields))

        for json_field in client_fields:
            field_type = self.translate_type(json_field['type'])

            if field_type == FieldType.text:
                new_field = self.encapsulate_field_type_text(json_field, {
                    "client_field": True
                })
                fields.append(new_field)


        additional_fields = form['additional_fields']
        print(json.dumps(client_fields))

        for json_field in additional_fields:
            field_type = self.translate_type(json_field['field_type'])

            if field_type == FieldType.text:
                new_field = self.encapsulate_field_type_text(json_field, {
                    "client_field": False
                })
                fields.append(new_field)

            if field_type == FieldType.select:
                new_field = self.encapsulate_field_type_select(json_field, {
                    "client_field": False
                })
                fields.append(new_field)

        return EventFormResponse(event_form_request.event_id, fields)

    def translate_type(self, bs_type: str) -> FieldType:
        if bs_type == "text" or bs_type == "email" or bs_type == "phone" or bs_type == "digits":
            return FieldType.text
        if bs_type == "select":
            return FieldType.select
        if bs_type == "checkbox":
            return FieldType.check

        # If type not matches with any defined type, we name it like 'unknown'
        return FieldType.unknown

    def encapsulate_field_type_text(self, bs_field, extra_info) -> Field:
        if extra_info['client_field']:
            return Field(FieldType.text, not bs_field['is_optional'], bs_field['id'], bs_field['title'], bs_field['default_value'], [], None)
        else:
            return Field(FieldType.text, not bs_field['optional'], bs_field['name'], bs_field['field_name'], bs_field['default_value'], [], None)

    def encapsulate_field_type_select(self, bs_field, extra_info) -> Field:
        field_options = []
        # json_field_options = json.loads()  ## TODO: ADDED

        for option in bs_field['field_options']:
            field_options.append(FieldOption(option, option, {}))

        return Field(FieldType.select, not bs_field['optional'], bs_field['name'], bs_field['field_name'], bs_field['default_value'], [], None)

