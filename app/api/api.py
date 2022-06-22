# GENERAL IMPORTS
from flask import Flask
from flask import request
import json


# MODULES IMPORT
from app.api.modules.calendar.api_calendal_middleware import ApiCalendarMiddleware
from app.api.modules.calendar.api_calendar import ApiCalendar
from app.api.utils import GeneralUtils


# GET ROUTES CONFIG
routes = GeneralUtils.get_routes()


# INITIALIZE MODULES
calendar_module = ApiCalendar()
calendar_module_middleware = ApiCalendarMiddleware()


# CREATE FLASK APP
rest = Flask(__name__)


# DEFINE API ROUTES
# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarData'])
def get_calendar_data():
    calendar_module_middleware.capture(request, 'getCalendarData')
    return calendar_module.get_calendar_data(request)

