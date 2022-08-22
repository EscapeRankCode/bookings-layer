import json


class BookSecondStepResponse:


    def __init__(self, booked: bool, error: str, booking_info):
        self.booked = booked
        self.error = error
        self.booking_info = booking_info

    def __iter__(self):
        yield from {
            "booked": self.booked,
            "error": self.error,
            "booking_info": self.booking_info
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "booked": self.booked,
            "error": self.error,
            "booking_info": json.dumps(self.booking_info)
        }
