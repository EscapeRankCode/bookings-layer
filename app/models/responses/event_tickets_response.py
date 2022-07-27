import json
from enum import Enum
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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class TicketInfo:
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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class TicketType(Enum):
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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class TicketsGroup:
    def __init__(self, tickets: [Ticket], total_rules: TotalRules):
        self.tickets = tickets  # List of Ticket
        self.total_rules = total_rules  # object of TotalRules

    def __iter__(self):
        yield from {
            "tickets": self.tickets,
            "total_rules": self.total_rules
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


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
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class EventTicketsResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
