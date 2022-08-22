import json

from app.models.responses.event_tickets_response import Ticket


class BookRequest:

    def __init__(self, request_data):
        self.booking_system_id = request_data['booking_system_id']  # int
        self.escaperoom_id = request_data['escaperoom_id']  # int
        self.company_id = request_data['company_id']  # int
        self.bs_config = request_data['bs_config']  # object
        self.event_date = request_data['event_date']  # dd/mm/yyyy (string)
        self.event_time = request_data['event_time']  # HH:MM (string)
        self.event_id = request_data['event_id']  # string
        self.event_tickets = request_data['event_tickets']  # list<objects>
        self.event_fields = request_data['event_fields']  # list<objects>
        self.booking_bs_info = request_data['booking_bs_info']  # map with BS related info to make the booking

    def to_json(self):
        tickets_json = []
        fields_json = []


        """
        for ticket in self.event_tickets:
            tickets_json.append(ticket.to_json())

        for field in self.event_fields:
            fields_json.append(field.to_json())
        """


        return {
            "booking_system_id": self.booking_system_id,
            "escaperoom_id": self.escaperoom_id,
            "company_id": self.company_id,
            "bs_config": self.bs_config,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "event_id": self.event_id,
            "event_tickets": json.dumps(self.event_tickets),
            "event_fields": json.dumps(self.event_fields),
            "booking_bs_info": json.dumps(self.booking_bs_info)
        }
