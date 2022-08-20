import json


class BookFirstStepResponse:

    def __init__(self, pre_booked: bool, error: str, total_price: float, deposit_price: float, currency: str, booking_info):
        self.pre_booked = pre_booked
        self.error = error
        self.total_price = total_price
        self.deposit_price = deposit_price
        self.currency = currency
        self.booking_info = booking_info

    def __iter__(self):
        yield from {
            "pre_booked": self.pre_booked,
            "error": self.error,
            "total_price": self.total_price,
            "deposit_price": self.deposit_price,
            "currency": self.currency,
            "booking_info": self.booking_info
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "pre_booked": self.pre_booked,
            "error": self.error,
            "total_price": self.total_price,
            "deposit_price": self.deposit_price,
            "currency": self.currency,
            "booking_info": json.dumps(self.booking_info)
        }

