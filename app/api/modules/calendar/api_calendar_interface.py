from app.api.modules.calendar.api_calendar import ApiCalendar


class ApiCalendarInterface(ApiCalendar):
    def get_calendar_data(self, api_request) -> str:
        pass
