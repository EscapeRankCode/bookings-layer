import json
from enum import IntEnum
from json import JSONEncoder

# START READING FROM THE BOTTOM
class TotalRules:
    def __init__(self, counter_min_units: int, counter_max_units: int, check_min_units: int, check_max_units: int, option_min_units: int, option_max_units: int):
        self.counter_min_units = counter_min_units  # int
        self.counter_max_units = counter_max_units  # int
        self.check_min_units = check_min_units  # int
        self.check_max_units = check_max_units  # int
        self.option_min_units = option_min_units  # int
        self.option_max_units = option_max_units  # int

    def __iter__(self):
        yield from{
            "counter_min_units": self.counter_min_units,
            "counter_max_units": self.counter_max_units,
            "check_min_units": self.check_min_units,
            "check_max_units": self.check_max_units,
            "option_min_units": self.option_min_units,
            "option_max_units": self.option_max_units
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "counter_min_units": self.counter_min_units,
            "counter_max_units": self.counter_max_units,
            "check_min_units": self.check_min_units,
            "check_max_units": self.check_max_units,
            "option_min_units": self.option_min_units,
            "option_max_units": self.option_max_units
        }


class TicketInfo:
    def to_json(self):
        pass


class TicketInfoOption(TicketInfo):
    def __init__(self, default_value: bool, single_unit_value: int, price_per_unit: float, currency: str):
        self.default_value = default_value  # bool
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string

    def __iter__(self):
        yield from {
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }


class TicketInfoCheck(TicketInfo):
    def __init__(self, default_value: bool, single_unit_value: int, price_per_unit: float, currency: str):
        self.default_value = default_value  # bool
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string

    def __iter__(self):
        yield from {
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }


class TicketInfoCounter(TicketInfo):
    def __init__(self, min_option: int, max_option: int, default_value: int, single_unit_value: int, price_per_unit: float, currency: str):
        self.min_option = min_option  # int
        self.max_option = max_option  # int
        self.default_value = default_value  # int
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string

    def __iter__(self):
        yield from {
            "min_option": self.min_option,
            "max_option": self.max_option,
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "min_option": self.min_option,
            "max_option": self.max_option,
            "default_value": self.default_value,
            "single_unit_value": self.single_unit_value,
            "price_per_unit": self.price_per_unit,
            "currency": self.currency
        }


class TicketType(IntEnum):
    counter = 1
    check = 2
    option = 3


class Ticket:
    def __init__(self, ticket_name: str, ticket_type: TicketType, ticket_info: TicketInfo):
        self.ticket_name = ticket_name  # string
        self.ticket_type = ticket_type  # int (enum)
        self.ticket_info = ticket_info  # (TicketInfo) : TicketInfoOption / TicketInfoCheck / TicketInfoCounter

    def __iter__(self):
        yield from {
            "ticket_name": self.ticket_name,
            "ticket_type": self.ticket_type,
            "ticket_info": self.ticket_info
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "ticket_name": self.ticket_name,
            "ticket_type": self.ticket_type,
            "ticket_info": self.ticket_info.to_json()
        }

class TicketsSelection:
    def __init__(self, counter_selected_units: int, check_selected_units: int, option_selected_units: int, selected_tickets: [Ticket]):
        self.counter_selected_units = counter_selected_units  # int
        self.check_selected_units = check_selected_units  # int
        self.option_selected_units = option_selected_units  # int
        self.selected_tickets = selected_tickets  # list of Ticket

    def __iter__(self):
        yield from{
            "counter_selected_units": self.counter_selected_units,
            "check_selected_units": self.check_selected_units,
            "option_selected_units": self.option_selected_units,
            "selected_tickets": self.selected_tickets
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        selected_tickets_json = []

        for t in self.selected_tickets:
            selected_tickets_json.append(t.to_json())

        return {
            "counter_selected_units": self.counter_selected_units,
            "check_selected_units": self.check_selected_units,
            "option_selected_units": self.option_selected_units,
            "selected_tickets": selected_tickets_json
        }

class TicketsGroup:
    def __init__(self, tickets: [Ticket], total_rules: TotalRules, tickets_selection: TicketsSelection):
        self.tickets = tickets  # List of Ticket
        self.total_rules = total_rules  # object of TotalRules
        self.tickets_selection = tickets_selection  # object of TicketsSelection

    def __iter__(self):
        yield from {
            "tickets": self.tickets,
            "total_rules": self.total_rules,
            "tickets_selection": self.tickets_selection
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        tickets_json = []

        for t in self.tickets:
            tickets_json.append(t.to_json())

        return {
            "tickets": tickets_json,
            "total_rules": self.total_rules.to_json(),
            "tickets_selection": self.tickets_selection.to_json()
        }


class EventTicketsResponse:
    def __init__(self, event_id: str, tickets_groups: [TicketsGroup]) -> None:
        self.event_id = event_id  # string
        self.tickets_groups = tickets_groups  # list of TicketsGroup

    def __iter__(self):
        yield from {
            "event_id": self.event_id,
            "tickets_groups": self.tickets_groups
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        tickets_groups_json = []
        for tick_g in self.tickets_groups:
            tickets_groups_json.append(tick_g.to_json())

        return {
            "event_id": self.event_id,
            "tickets_groups": tickets_groups_json
        }


class EventTicketsResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
