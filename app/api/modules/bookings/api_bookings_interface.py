from flask import request

from app.models.requests.book_first_step_request import BookFirstStepRequest
from app.models.responses.book_first_step_response import BookFirstStepResponse


class ApiBookingsInterface:
    def book_first_step(self, api_request: BookFirstStepRequest):
        pass

    def encapsulate_book_first_step_result(self, result, request: BookFirstStepRequest) -> BookFirstStepResponse:
        pass
