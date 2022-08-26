import json
from datetime import datetime

import requests

from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.modules.bookings.api_bookings_interface import ApiBookingsInterface
from app.api.utils import general_utils
from app.models.requests.book_request import BookRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse
from app.models.responses.book_second_step_response import BookSecondStepResponse


class SimplybookApiBookings(ApiBookingsInterface):



    def __init__(self) -> None:
        self.auth_module = SimplybookApiAuth()

    def book_first_step(self, book_request: BookRequest):
        """
        Returns the confirmation of the booking, if it's correct, otherwise, in 'error' field, shows the error
        :param book_request:
        :return: always true, because simplybook does not support pre-booking a slot
        """

        # --- Get the credentials
        credentials = self.auth_module.authorize(None)  # map with token and refresh_token

        # --- Get the ticket selected (service)
        tickets_selection = json.loads(book_request.event_tickets[0]['tickets_selection'])
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

        found = False
        price = 0
        service_id = -1
        for service in response_json['data']:
            if service['name'] == ticket_selected_name:
                found = True
                price = service['price']
                service_id = service['id']
                break

        if not found:
            return None

        date_time_obj = datetime.strptime(book_request.event_date + " " + book_request.event_time, '%d/%m/%Y %H:%M')


        # Return always true because
        return BookFirstStepResponse(True, "", price, 0, "€", {
            "start_datetime": date_time_obj.strftime("%y-%m-%d %H:%M:%S"),
            "category_id": book_request.bs_config['category_id'],
            "provider_id": book_request.bs_config['provider_id'],
            "service_id": service_id,
            "price": price
        })

    def book_second_step(self, book_request: BookRequest):
        # --- Get the credentials
        credentials = self.auth_module.authorize(None)  # map with token and refresh_token

        # --- Try to create the client
        # ------- 1. Get the required fields
        # ------- 2. Search the required fields in form
        # ------- 3. Make the request


        # ------- 1. Get the required fields
        print("--- SECOND STEP: 1- Get required fields")
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


        # ------- 2. Search the required fields in form
        print("--- SECOND STEP: 2- Search required fields in form")
        email = None
        client_mandatory_fields = []
        for json_field in client_json_fields:
            field_to_find = None
            for field in book_request.event_fields:
                if field['field_key'] == json_field['id']:
                    print("Field found: " + field['field_key'])
                    field_to_find = field
                    if field['field_key'] == 'email':
                        email = json.loads(field['user_input'])['user_input_value']
                    break

            if field_to_find is not None:
                client_mandatory_fields.append({
                    "key": field_to_find['field_key'],
                    "value": json.loads(field_to_find['user_input'])['user_input_value']
                })
            else:
                return None


        # ------- 3. Make the request
        print("--- SECOND STEP: 3- Create client")
        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_create_client

        create_client_fields = {}
        for client_mandatory_field in client_mandatory_fields:
            create_client_fields[client_mandatory_field['key']] = client_mandatory_field['value']

        payload = json.dumps(create_client_fields)
        print("--- CREATE CLIENT PAYLOAD")
        print(payload)
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        print("--- CREATE CLIENT RESPONSE")
        print(response.text)


        # --- If error, client exists so: search the existing client
        client_id = -1
        if response.status_code != 200:
            print("--- SECOND STEP: 4.a- Edit the client")
            client_id = self.search_client(credentials, email)
            if client_id != -1:
                print("--- SECOND STEP: 4.a.1- Client found, now to update-client")
                updated = self.update_client(credentials, client_id, client_mandatory_fields)
                if not updated:
                    return None
            else:
                return None

        else:
            print("--- SECOND STEP: 4.b- Client created")
            client_id = response_json['id']


        print("--- SECOND STEP: 5- Client id is: " + str(client_id))

        # --- Create the booking and notify if it's ok
        print("--- SECOND STEP: 6- Create the booking")
        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_create_booking

        additional_fields_booking = []
        for request_field in book_request.event_fields:
            if not self.is_field_inside(request_field, client_mandatory_fields):
                additional_fields_booking.append({
                    "field": request_field['field_key'],
                    "value": json.loads(request_field['user_input'])['user_input_text']
                })

        booking_info = book_request.booking_bs_info
        payload = json.dumps({
            "count": 1,
            "start_datetime": booking_info['start_datetime'],
            "location_id": None,
            "category_id": booking_info['category_id'],
            "provider_id": booking_info['provider_id'],
            "service_id": booking_info['service_id'],
            "client_id": client_id,
            "additional_fields": json.dumps(additional_fields_booking)
        })
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            return BookSecondStepResponse(False, "Unable to create the booking", {})

        response_json = json.loads(response.text)
        print("Create booking response: " + response.text)

        b_info_object = {
            "price": book_request.booking_bs_info['price'],
            "id": response_json['bookings'][0]['id'],
            "code": response_json['bookings'][0]['code'],
            "client_id": client_id
        }

        return BookSecondStepResponse(True, "", b_info_object)

    def search_client(self, credentials, email: str) -> int:
        end = False
        page = 1
        elements_per_page = 100

        while not end:
            url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_clients + "?page=" + str(page) + "&on_page=" + str(elements_per_page)
            print("------ SEARCH CLIENT URL: " + url)
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'X-Company-Login': credentials['company'],
                'X-Token': credentials['token']
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            print("------ SEARCH CLIENT status code: " + str(response.status_code))
            if response.status_code != 200:
                return -1

            response_json = json.loads(response.text)
            print("------ SEARCH CLIENT response: " + response.text)
            response_data = response_json['data']
            response_metadata = response_json['metadata']

            total_clients = response_metadata['items_count']

            for client in response_data:
                print("CLIENT LOOKING: " + json.dumps(client))
                if client['email'] == email:
                    print("CLIENT FOUND! - ID CLIENT IS " + str(client['id']))
                    return client['id']

            if total_clients > (page * elements_per_page):
                page += 1
            else:
                end = True

        return -1

    def update_client(self, credentials, client_id, client_mandatory_fields) -> bool:
        fields = []
        for mandatory_field in client_mandatory_fields:
            fields.append({
                "id": mandatory_field['key'],
                "value": mandatory_field['value']
            })


        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_update_clients + str(client_id)

        payload = json.dumps({
            "id": client_id,
            "fields": fields
        })

        print("------ UPDATE CLIENT PAYLOAD: " + payload)

        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("------ UPDATE CILENT RESPONSE: " + response.text)
        return response.status_code == 200

    def is_field_inside(self, request_field, client_mandatory_fields):
        for mand_field in client_mandatory_fields:
            if request_field['field_key'] == mand_field['key']:
                return True
        return False
