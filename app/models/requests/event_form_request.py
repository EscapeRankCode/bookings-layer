
class EventFormRequest:

    def __init__(self, request_data):
        self.booking_system_id = request_data['booking_system_id']  # int
        self.bs_config = request_data['bs_config']  # int
        self.event_date = request_data['event_date']  # dd/mm/yyyy (string)
        self.event_time = request_data['event_time']  # HH:MM (string)
        self.event_id = request_data['event_id']  # string
        self.event_tickets = request_data['event_tickets']  # list<objects>

