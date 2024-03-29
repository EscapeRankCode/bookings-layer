# GENERAL IMPORTS
from flask import Flask
from flask import request
import logging

from app.api.modules.bookings.api_bookings import ApiBookings
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
bookings_module = ApiBookings()
# calendar_module_middleware = ApiCalendarMiddleware()


# disable logger
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# CREATE FLASK APP
rest = Flask(__name__)
rest.logger.disabled = True
log.disabled = True


# DEFINE ENDPOINTS FOR EACH MODULE
# -- CALENDAR MODULE
@rest.route(routes['modules']['calendar']['getCalendarAvailability'], methods=['POST'])
def get_calendar_availability():
    print("\nRECEIVED: getCalendarAvailability")
    return calendar_module.get_calendar_availability(request)

# -- EVENTS MODULE
@rest.route(routes['modules']['events']['getEventTickets'], methods=['POST'])
def get_event_tickets():
    print("\nRECEIVED: getEventTickets")
    return events_module.get_event_tickets(request)

@rest.route(routes['modules']['events']['getEventForm'], methods=['POST'])
def get_event_form():
    print("\nRECEIVED: getEventForm")
    return events_module.get_event_form(request)

@rest.route(routes['modules']['booking']['bookFirstStep'], methods=['POST'])
def book_first_step():
    print("\nRECEIVED: bookFirstStep")
    return bookings_module.book_first_step(request)

@rest.route(routes['modules']['booking']['bookSecondStep'], methods=['POST'])
def book_second_step():
    print("\nRECEIVED: bookSecondStep")
    return bookings_module.book_second_step(request)


