# GENERAL IMPORTS
from flask import Flask
import json


# MODULES IMPORT
from .modules.api_calendar import ApiCalendar


# CONSTANTS
ROUTES_FILE_PATH = "./app/api/routes.json"
SCHEMES_FILE_PATH = "./app/api/schemes.json"


# LOAD CONFIGS
with open(ROUTES_FILE_PATH, 'r') as routes_file:
    routes = json.loads(routes_file.read())
with open(SCHEMES_FILE_PATH, 'r') as schemes_file:
    schemes = json.loads(schemes_file.read())


# INITIALIZE MODULES
calendar_module = ApiCalendar()


# CREATE FLASK APP
rest = Flask(__name__)


# DEFINE API ROUTES
# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarData'])
def get_calendar_data():
    return calendar_module.get_calendar_data()

