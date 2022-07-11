from flask import Flask, request

from app.api.utils import general_utils


class ApiCalendarMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiCalendar(metaclass=ApiCalendarMeta):
    def get_calendar_availability(self, api_request: request) -> str:
        # $booking_system_id, $bs_config_id, $start_date, $end_date
        # params = api_request.args
        # booking_system_id = params.get('booking_system_id', -1, 'int')
        # print("--------")
        # print("Params:")
        # print(params)

        print("JSON:")
        print(api_request.json)
        print("GET JSON:")
        print(api_request.get_json())
        print("--------")
        # bs_config = params.get('bs_config', -1, 'int')
        # start_date = params.get('start_date', -1, 'str')
        # end_date = params.get('end_date', -1, 'str')
        # print(bs_config)
        # print(start_date)
        # print(end_date)

        # if booking_system_id == general_utils.BS_ID_MAXIMUM:
        #    print("--------")
        #    print("MAXIMUM ESCAPE detected")
        #    pass

        return "{Hello World}"
