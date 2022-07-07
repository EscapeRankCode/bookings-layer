# GENERAL IMPORTS
from flask import Flask
from flask import request
import json


# MODULES IMPORT
from app.api.modules.calendar.api_calendal_middleware import ApiCalendarMiddleware
from app.api.modules.calendar.api_calendar import ApiCalendar
from app.api.utils import general_utils


# GET ROUTES CONFIG
routes = general_utils.get_routes()


# INITIALIZE MODULES
# -- CALENDAR MODULE
calendar_module = ApiCalendar()
calendar_module_middleware = ApiCalendarMiddleware()


# CREATE FLASK APP
rest = Flask(__name__)


# DEFINE ENDPOINTS FOR EACH MODULE
# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarAvailability'])
def get_calendar_availability():
    return calendar_module.get_calendar_availability(request)

