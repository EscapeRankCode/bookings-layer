
class CalendarAvailabilityRequest:
    def __init__(self, request_data):
        self.start_date = request_data['start_date']  # dd/mm/yyyy
        self.end_date = request_data['end_date']  # dd/mm/yyyy
        self.booking_system_id = request_data['booking_system_id']
        self.bs_config = request_data['bs_config']

