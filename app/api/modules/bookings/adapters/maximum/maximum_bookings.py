import json

import requests

from app.api.modules.bookings.api_bookings_interface import ApiBookingsInterface
from app.api.utils import general_utils
from app.models.requests.book_first_step_request import BookFirstStepRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse
from app.models.responses.event_tickets_response import TicketsGroup, Ticket


class MaximumApiBookings(ApiBookingsInterface):
    def book_first_step(self, book_first_step_request: BookFirstStepRequest):
        """
        Returns the confirmation of the booking, if it's correct, otherwise, in 'error' field, shows the error
        :param book_first_step_request:
        :return:
        """

        print("MAXIMUM BOOK SETP 1 REQUEST: " + json.dumps(book_first_step_request.to_json()))

        error_exists = False

        date_split = book_first_step_request.event_date.split('/')

        partner_id = book_first_step_request.booking_bs_info['partner_id']
        quest_id = book_first_step_request.bs_config['room']
        proposal_id = book_first_step_request.event_id
        date = date_split[2] + "-" + date_split[1] + "-" + date_split[0]  # "2022-08-15"
        name = None
        email = None
        phone = None
        playersCount = None
        comment = None
        gameLanguage = None
        couponCode = None

        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_time_table

        error = ""

        name_field = self.search_field(book_first_step_request.event_fields, 'name')
        if name_field is None:
            error += "Field 'name' not found in booking form\n"
            error_exists = True
        else:
            user_input = json.loads(name_field['user_input'])
            name = user_input['user_input_value']

        email_field = self.search_field(book_first_step_request.event_fields, 'email')
        if email_field is None:
            error += "Field 'email' not found in booking form\n"
            error_exists = True
        else:
            user_input = json.loads(name_field['user_input'])
            email = user_input['user_input_value']

        phone_field = self.search_field(book_first_step_request.event_fields, 'phone')
        if phone_field is None:
            error += "Field 'phone' not found in booking form\n"
            error_exists = True
        else:
            user_input = json.loads(name_field['user_input'])
            phone = user_input['user_input_value']

        comment_field = self.search_field(book_first_step_request.event_fields, 'comment')
        if comment_field is None:
            error += "Field 'comment' not found in booking form\n"
            error_exists = True
        else:
            user_input = json.loads(name_field['user_input'])
            comment = user_input['user_input_value']

        gameLanguage_field = self.search_field(book_first_step_request.event_fields, 'gameLanguage')
        if gameLanguage_field is None:
            error += "Field 'gameLanguage' not found in booking form\n"
            error_exists = True
        else:
            user_input = json.loads(name_field['user_input'])
            gameLanguage = user_input['user_input_value']

        couponCode_field = self.search_field(book_first_step_request.event_fields, 'gameLanguage')
        if couponCode_field is None:
            couponCode = ""
            # error += "Field 'couponCode' not found in booking form\n"
        else:
            user_input = json.loads(name_field['user_input'])
            couponCode = user_input['user_input_value']


        if error_exists:
            print("Error in fields not found:")
            print(error)
            return self.__build_error(error)

        #  PLAYERS COUNT comes from the selected ticket previously
        playersCount = self.players_count_from_tickets(book_first_step_request.event_tickets)
        if playersCount <= 0:
            return self.__build_error("Tickets selected error")

        payload = json.dumps({
            "partner_id": partner_id,
            "quest_id": quest_id,
            "proposal_id": proposal_id,
            "date": date,  # "2022-08-15"
            "name": name,
            "email": email,
            "phone": phone,
            "playersCount": playersCount,
            "comment": comment,
            "gameLanguage": gameLanguage,
            "couponCode": couponCode
        })
        headers = {
            'Content-Type': 'application/json'
        }

        print("PAYLOAD TO BOOK STEP 1 MAXIMUM IS:")
        print(payload)

        response = requests.request("POST", url, headers=headers, data=payload)

        maximum_first_step_result = json.loads(response.text)['event']
        print(maximum_first_step_result)

        if 'error' in maximum_first_step_result.keys():
            print("Error in maximum booking request: " + maximum_first_step_result['error'])
            return self.__build_error(maximum_first_step_result['error'])

        else:
            return self.encapsulate_book_first_step_result(maximum_first_step_result['event'], book_first_step_request)


    def encapsulate_book_first_step_result(self, result, request: BookFirstStepRequest) -> BookFirstStepResponse:
        pre_booked = True
        error = ""
        total_price = result['price']
        deposit_price = result['prePaidValue']
        currency = result['priceCurrencySymbol']
        booking_info = {
            "id": result['id'],
            "unicId": result['unicId'],
            'link': result['link']
        }
        return BookFirstStepResponse(pre_booked, error, total_price, deposit_price, currency, booking_info)


    def __build_error(self, error: str) -> BookFirstStepResponse:
        return BookFirstStepResponse(False, error, 0, 0, "", {})

    def search_field(self, fields, field_key):
        for field in fields:
            if field['field_key'] == field_key:
                return field
        return None

    def players_count_from_tickets(self, event_tickets):
        selected_tickets = []

        # ONLY ONE GROUP HAS TO BE HERE, AND ONLY ONE TICKET
        for group in event_tickets:
            group_selection = group['tickets_selection']
            for ticket in group_selection['selected_tickets']:
                selected_tickets.append(ticket)

        if len(selected_tickets) > 1:
            print("So many tickets selected")
            return -1
        else:
            ticket = selected_tickets[0]
            ticket_name = ticket['ticket_name']
            print("ticket selected was: " + ticket_name)
            return int(ticket_name.split(' ')[0])

