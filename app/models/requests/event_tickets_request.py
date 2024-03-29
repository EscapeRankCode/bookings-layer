
class EventTicketsRequest:
    def __init__(self, request_data):
        self.event_date = request_data['event_date']  # dd/mm/yyyy
        self.event_time = request_data['event_time']  # HH:MM
        self.booking_system_id = request_data['booking_system_id']  # int
        self.bs_config = request_data['bs_config']  # object
        self.event_id = request_data['event_id']  # string
