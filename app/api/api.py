# GENERAL IMPORTS
from flask import Flask
from flask import request
import json


# MODULES IMPORT
from app.api.modules.calendar.api_calendal_middleware import ApiCalendarMiddleware
from app.api.modules.calendar.api_calendar import ApiCalendar
from app.api.modules.general.api_general import ApiGeneral
from app.api.utils import GeneralUtils


# GET ROUTES CONFIG
routes = GeneralUtils.get_routes()


# INITIALIZE MODULES
# -- CALENDAR MODULE
general_module = ApiGeneral()
# -- CALENDAR MODULE
calendar_module = ApiCalendar()
calendar_module_middleware = ApiCalendarMiddleware()


# CREATE FLASK APP
rest = Flask(__name__)


# DEFINE ENDPOINTS FOR EACH MODULE
# -- CALENDAR MODULE
@rest.route(routes['modules']['general']['getBookingSystem'])
def get_booking_system():
    return general_module.get_booking_system(request)


# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarData'])
def get_calendar_data():
    calendar_module_middleware.capture(request, 'getCalendarData')
    return calendar_module.get_calendar_data(request)

