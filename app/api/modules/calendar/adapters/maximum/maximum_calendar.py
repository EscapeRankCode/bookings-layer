import requests
import json
from app.api.modules.calendar.api_calendar_interface import ApiCalendarInterface
from app.models.requests.calendar_availability_request import CalendarAvailabilityRequest
from datetime import datetime, date, timedelta
from app.api.utils import general_utils
from app.models.responses.calendar_availability_response import *


class MaximumApiCalendar(ApiCalendarInterface):
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

        maximum_availability = json.loads(response.text)

        response = self.encapsulate_calendar_availability(maximum_availability, calendar_availability_request)
        return response

    def encapsulate_calendar_availability(self, maximum_availability, request: CalendarAvailabilityRequest) -> CalendarAvailabilityResponse :

        calendar_days = []

        for schedule_day in maximum_availability['scheduleDays']:
            string_date_parts = schedule_day['linkDate'].split('-')

            year = int(string_date_parts[0])
            month = int(string_date_parts[1])
            day = int(string_date_parts[2])

            day_events = []

            total_events = 0
            free_events = 0

            #  Each range block has its own price (morning prices vs afternoon prices)
            for range_block in schedule_day['proposalPriceRangeBlocks']:

                # Each range block has its events
                for event in range_block['proposals']:
                    # Get the time
                    time_split_string = event['startTime'].split(':')
                    time = time_split_string[0] + ':' + time_split_string[1]

                    # Get the availability
                    availability_status = self.event_availability(event, request.bs_config, schedule_day['linkDate'])
                    if availability_status != general_utils.EVENT_AVAILABILITY_NOT_AVAILABLE and availability_status != general_utils.EVENT_AVAILABILITY_CONSULT:
                        total_events += 1
                        if availability_status == general_utils.EVENT_AVAILABILITY_FREE:
                            free_events += 1

                    # Build the event object
                    event_object = Event(time, event['id'], availability_status)
                    day_events.append(event_object)

            # After treating all events of a day, we set the day availability
            if total_events == free_events:
                day_availability = general_utils.DAY_AVAILABILITY_FREE
            elif free_events == 0:
                day_availability = general_utils.DAY_AVAILABILITY_CLOSED
            else:
                day_availability = general_utils.DAY_AVAILABILITY_MIXED

            # Create the
            day_object = Day(year, month, day, day_availability, day_events)
            calendar_days.append(day_object)

        # All days treated
        calendar = Calendar(request.bs_config['timezone'], calendar_days)
        return CalendarAvailabilityResponse(request.booking_system_id, request.bs_config['config_id'], calendar)


    def event_availability(self, event, bs_config, day_string) -> int:
        if event['expired']:
            return general_utils.EVENT_AVAILABILITY_NOT_AVAILABLE

        if event['reserved']:
            return general_utils.EVENT_AVAILABILITY_CLOSED

        session_datetime = datetime.strptime(day_string + ' ' + event['startTime'], '%Y-%m-%d %H:%M:%S')
        now_datetime = datetime.now()
        diff = session_datetime - now_datetime
        diff_hours = diff / timedelta(hours=1)

        if diff_hours < bs_config['min_hours_anticipation']:
            return general_utils.EVENT_AVAILABILITY_CONSULT

        return general_utils.EVENT_AVAILABILITY_FREE




