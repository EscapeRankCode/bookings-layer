import json
from datetime import datetime

import requests

from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.modules.bookings.api_bookings_interface import ApiBookingsInterface
from app.api.utils import general_utils
from app.models.requests.book_request import BookRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse


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

        date_time_obj = datetime.strptime(book_request.event_date + " " + book_request.event_time, '%d/%m/%y %H:%M')


        # Return always true because
        return BookFirstStepResponse(True, "", price, 0, "€", {
            "start_datetime": date_time_obj.strftime("%y-%m-%d %H:%M:%S"),
            "category_id": book_request.bs_config['category_id'],
            "provider_id": book_request.bs_config['provider_id'],
            "service_id": service_id
        })

