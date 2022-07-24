import json
from app.api.exceptions.general_exception import GeneralException


# PATH CONSTANTS
ROUTES_FILE_PATH = "./app/api/routes.json"
SCHEMES_FILE_PATH = "./app/api/schemes.json"

# DATE AND TIME_FORMAT
MAXIMUM_DATE_FORMAT = "%d/%m/%Y"

# EVENT AVAILABILITY CONSTANTS
EVENT_AVAILABILITY_CLOSED = 1
EVENT_AVAILABILITY_NOT_AVAILABLE = 2
EVENT_AVAILABILITY_CONSULT = 3
EVENT_AVAILABILITY_FREE = 4

# DAY AVAILABILITY CONSTANTS
DAY_AVAILABILITY_CLOSED = 1
DAY_AVAILABILITY_MIXED = 2
DAY_AVAILABILITY_FREE = 3

# --------- BOOKING SYSTEMS CONSTANTS ---------
# BOOKING_SYSTEMS CONSTANTS
BS_ID_TURITOP = 1
BS_ID_MAXIMUM = 2

# MAXIMUM HOST
MAXIMUM_BS_HOST = 'http://dev.terraquesta.com'
MAXIMUM_BS_ENDPOINT_calendar_availability = '/api/schedule_with_offset'
MAXIMUM_BS_ENDPOINT_time_table = '/api/time_table'
MAXIMUM_BS_ENDPOINT_event_form = '/api/fields'


# METHODS
def get_schemes():
    try:
        with open(SCHEMES_FILE_PATH, 'r') as schemes_file:
            schemes = json.loads(schemes_file.read())
            return schemes
    except Exception as e:
        raise GeneralException("get_schemes - " + str(e))


def get_routes():
    try:
        with open(ROUTES_FILE_PATH, 'r') as routes_file:
            routes = json.loads(routes_file.read())
            return routes
    except Exception as e:
        raise GeneralException("get_routes - " + str(e))
