import json
from flask import request

from app.api.modules.bookings.adapters.maximum.maximum_bookings import MaximumApiBookings
from app.api.utils import general_utils
from app.models.requests.book_request import BookRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse


class ApiBookingsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ApiBookings(metaclass=ApiBookingsMeta):
    def __init__(self):
        self.maximum_api_bookings = MaximumApiBookings()

    def book_first_step(self, api_request: request):
        print("BOOK 1ST STEP REQUEST")
        print(request.json)
        book_first_step_request = BookRequest(api_request.json['data'])

        # Depending on the booking system
        if book_first_step_request.booking_system_id == general_utils.BS_ID_MAXIMUM:
            first_step_result = self.maximum_api_bookings.book_first_step(book_first_step_request)
            return first_step_result.to_json()
            #  return json.dumps(first_step_result.to_json())


        return "Book First Step Error", 400

    def book_second_step(self, api_request: request):
        book_second_step_request = BookRequest(api_request.json['data'])

        # Depending on the booking system
        if book_second_step_request.booking_system_id == general_utils.BS_ID_MAXIMUM:
            second_step_result = self.maximum_api_bookings.book_second_step(book_second_step_request)
            return second_step_result.to_json()
            #  return json.dumps(first_step_result.to_json())


        return "Book First Step Error", 400

