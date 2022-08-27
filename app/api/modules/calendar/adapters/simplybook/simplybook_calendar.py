import json

import requests
from flask import request
from datetime import datetime, date, timedelta

from app.api.modules.auth.adapters.simplybook.simplybook_auth import SimplybookApiAuth
from app.api.utils import general_utils
from app.api.modules.calendar.api_calendar_interface import ApiCalendarInterface
from app.models.requests.calendar_availability_request import CalendarAvailabilityRequest
from app.models.responses.calendar_availability_response import CalendarAvailabilityResponse, Calendar, Event, Day


class SimplybookApiCalendar(ApiCalendarInterface):

    def __init__(self):
        self.auth_module = SimplybookApiAuth()

    def get_calendar_availability(self, api_request: CalendarAvailabilityRequest):
        # GET THE TOKEN
        credentials = self.auth_module.authorize(None)  # map with token and refresh_token
        print("Credentials in calendar availability:")
        print(json.dumps(credentials))

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_services_categories_list
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'X-Company-Login': credentials['company'],
            'X-Token': credentials['token']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        print("calendar response: " + response.text)

        category_id_to_search = api_request.bs_config['category_id']
        category_found = None

        # Search the game (category)
        for category in response_json["data"]:
            if category['id'] == category_id_to_search:
                category_found = category
                break

        service = -1

        # Now we get one of the tickets to see the slots
        if category_found is not None:
            services = category_found['services']
            if len(services) > 0:
                service = services[0]

        if service == -1:
            return CalendarAvailabilityResponse(api_request.booking_system_id, api_request.bs_config['bs_config_id'],
                                                Calendar(api_request.bs_config['timezone'], []))

        start_date = (datetime.strptime(api_request.start_date, general_utils.CALENDAR_REQUEST_DATE_FORMAT)).date()
        end_date = (datetime.strptime(api_request.end_date, general_utils.CALENDAR_REQUEST_DATE_FORMAT)).date()

        calendar_days = []

        for date_x in self.daterange(start_date, end_date):
            print("Demanded date")
            print(str(date_x))
            # Refresh the token
            # credentials = self.auth_module.refresh(credentials)

            # Call to get all slots
            url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_slots + \
                  "?date_to=" + date_x.strftime(general_utils.SIMPLYBOOK_DATE_FORMAT) + \
                  "&provider_id=" + str(api_request.bs_config['provider_id']) + \
                  "&service_id=" + str(service)
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'X-Company-Login': credentials['company'],
                'X-Token': credentials['token']
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            slots_json = json.loads(response.text)
            print("All slots url is: " + url)
            print("Token: " + credentials['token'])
            print("All slots: ")
            print(response.text)

            # Call to get only available slots
            url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_get_slots_available + \
                  "?date=" + date_x.strftime(general_utils.SIMPLYBOOK_DATE_FORMAT) + \
                  "&provider_id=" + str(api_request.bs_config['provider_id']) + \
                  "&service_id=" + str(service)
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'X-Company-Login': credentials['company'],
                'X-Token': credentials['token']
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            available_slots_json = json.loads(response.text)
            print("Available slots: ")
            print(response.text)

            day = self.encapsulate_day(slots_json, available_slots_json, date_x, api_request.bs_config)
            calendar_days.append(day)

        calendar = Calendar(api_request.bs_config['timezone'], calendar_days)
        print("CALENDAR FORMED = " + json.dumps(calendar.to_json()))
        return CalendarAvailabilityResponse(api_request.booking_system_id, api_request.bs_config['config_id'], calendar)

    # AUXILIARY FUNCTIONS

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def encapsulate_day(self, all_slots, available_slots, date_x: datetime, bs_config) -> Day:
        total_slots = len(all_slots)
        total_available_slots = len(available_slots)

        day_events = []

        for slot in all_slots:
            status = self.event_availability(slot, available_slots, bs_config, date_x)
            time = self.build_time_var(slot['time'])
            day_events.append(Event(time, slot['time'], status))

        day_availability = general_utils.DAY_AVAILABILITY_FREE
        if total_available_slots == 0:
            day_availability = general_utils.DAY_AVAILABILITY_CLOSED
        elif total_available_slots < total_slots:
            day_availability = general_utils.DAY_AVAILABILITY_MIXED

        return Day(date_x.year, date_x.month, date_x.day, day_availability, day_events)



    def is_slot_available(self, slot, available_slots):
        for available_slot in available_slots:
            if available_slot['time'] == slot['time']:
                return True
        return False

    def event_availability(self, slot, available_slots, bs_config, date_x):
        if not self.is_slot_available(slot, available_slots):
            return general_utils.EVENT_AVAILABILITY_CLOSED
        else:
            # session_datetime = datetime.strptime(day_string + ' ' + event['startTime'], '%Y-%m-%d %H:%M:%S')
            now_datetime = datetime.now().date()
            diff = date_x - now_datetime
            diff_hours = diff / timedelta(hours=1)

            if diff_hours < bs_config['min_hours_anticipation']:
                return general_utils.EVENT_AVAILABILITY_CONSULT

            return general_utils.EVENT_AVAILABILITY_FREE

    def build_time_var(self, time_string: str):
        # with format ("HH:MM:SS")
        parts = time_string.split(':')
        return parts[0] + ":" + parts[1]
