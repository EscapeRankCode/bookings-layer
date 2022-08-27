import json
from app.api.exceptions.general_exception import GeneralException


# PATH CONSTANTS
ROUTES_FILE_PATH = "./app/api/routes.json"
SCHEMES_FILE_PATH = "./app/api/schemes.json"

# REQUEST CALENDAR FORMAT
CALENDAR_REQUEST_DATE_FORMAT = "%d/%m/%Y"

# DATE AND TIME_FORMAT
MAXIMUM_DATE_FORMAT = "%d/%m/%Y"
SIMPLYBOOK_DATE_FORMAT = "%Y-%m-%d"

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
BS_ID_SIMPLYBOOK = 3

# BACKEND_HOST
BACKEND_BASE = "http://devel.escaperank.com/api"
BACKEND_URL_get_last_token = "/bookings_layer/auth"
BACKEND_URL_set_last_token = "/bookings_layer/new_auth"

# MAXIMUM HOST
MAXIMUM_BS_HOST = 'http://dev.terraquesta.com'
MAXIMUM_BS_ENDPOINT_calendar_availability = '/api/schedule_with_offset'
MAXIMUM_BS_ENDPOINT_time_table = '/api/time_table'
MAXIMUM_BS_ENDPOINT_event_form = '/api/fields'
MAXIMUM_BS_ENDPOINT_booking_first_step = '/api/process'
MAXIMUM_BS_ENDPOINT_booking_second_step = '/api/update'

# SIMPLYBOOK HOST
SIMPLYBOOK_BS_HOST = 'https://user-api-v2.simplybook.me/admin'
SIMPLYBOOK_BS_authorize = '/auth'
SIMPLYBOOK_BS_refresh = '/auth/refresh-token'
SIMPLYBOOK_BS_services_categories_list = '/categories'
SIMPLYBOOK_BS_get_slots = '/schedule/slots'
SIMPLYBOOK_BS_get_slots_available = '/schedule/available-slots'
SIMPLYBOOK_BS_get_services = '/services'
SIMPLYBOOK_BS_get_client_fields = '/clients/fields'
SIMPLYBOOK_BS_get_additional_fields = '/additional-fields'
SIMPLYBOOK_BS_create_client = '/clients'
SIMPLYBOOK_BS_get_clients = '/clients'
SIMPLYBOOK_BS_update_clients = '/clients/field-values/'
SIMPLYBOOK_BS_create_booking = '/bookings'


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
