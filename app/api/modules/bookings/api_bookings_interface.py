from flask import request

from app.models.requests.book_request import BookRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse


class ApiBookingsInterface:
    def book_first_step(self, api_request: BookRequest):
        pass

    def encapsulate_book_first_step_result(self, result, request: BookRequest) -> BookFirstStepResponse:
        pass
