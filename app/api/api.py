# GENERAL IMPORTS
from flask import Flask
from flask import request


# MODULES IMPORT
from app.api.modules.calendar.api_calendar import ApiCalendar
from app.api.modules.events.api_events import ApiEvents
from app.api.utils import general_utils


# GET ROUTES CONFIG
routes = general_utils.get_routes()


# INITIALIZE MODULES
# -- CALENDAR MODULE
calendar_module = ApiCalendar()
events_module = ApiEvents()
# calendar_module_middleware = ApiCalendarMiddleware()


# CREATE FLASK APP
rest = Flask(__name__)


# DEFINE ENDPOINTS FOR EACH MODULE
# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarAvailability'], methods=['POST'])
def get_calendar_availability():
    return calendar_module.get_calendar_availability(request)

# -- EVENTS MODULE
@rest.route(routes['modules']['events']['getEventTickets'], methods=['POST'])
def get_event_tickets():
    return events_module.get_event_tickets(request)

@rest.route(routes['modules']['events']['getEventForm'], methods=['POST'])
def get_event_form():
    return events_module.get_event_form(request)
