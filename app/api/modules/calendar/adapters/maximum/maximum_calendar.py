import requests
import json

from app.api.modules.calendar.api_calendar import ApiCalendar
from app.models.requests.calendar_availability_request import CalendarAvailabilityRequest
from datetime import datetime, date
from app.api.utils import general_utils


class MaximumApiCalendar(ApiCalendar):
    def get_calendar_availability(self, calendar_availability_request: CalendarAvailabilityRequest):

        actual_day = date.today()
        start_date = (datetime.strptime(calendar_availability_request.start_date, general_utils.DATE_FORMAT)).date()
        end_date = (datetime.strptime(calendar_availability_request.end_date, general_utils.DATE_FORMAT)).date()

        offset = (start_date - actual_day).days
        total_days = (end_date - start_date).days

        url = general_utils.MAXIMUM_BS_HOST + general_utils.MAXIMUM_BS_ENDPOINT_calendar_availability

        payload = json.dumps({
            "id": calendar_availability_request.bs_config['room'],
            "days": total_days,
            "offset": offset
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


        return None
        # TODO: BUILD THE DATA MODEL TO BE RETURNED
        # return super().get_calendar_availability(api_request)
