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


class TicketInfo:
    pass


class TicketInfoOption(TicketInfo):
    def __init__(self, default: bool, single_unit_value: int, price_per_unit: float, currency: str):
        self.default = default  # bool
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string


class TicketInfoCheck(TicketInfo):
    def __init__(self, default: bool, single_unit_value: int, price_per_unit: float, currency: str):
        self.default = default  # bool
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string


class TicketInfoCounter(TicketInfo):
    def __init__(self, min_option: int, max_option: int, default: int, single_unit_value: int, price_per_unit: float, currency: str):
        self.min_option = min_option  # int
        self.max_option = max_option  # int
        self.default = default  # int
        self.single_unit_value = single_unit_value  # int
        self.price_per_unit = price_per_unit  # float
        self.currency = currency  # string


class TicketType(Enum):
    counter = 1
    check = 2
    option = 3


class Ticket:
    def __init__(self, ticket_name: str, ticket_type: TicketType, ticket_info: TicketInfo):
        self.ticket_name = ticket_name  # string
        self.ticket_type = ticket_type  # int (enum)
        self.ticket_info = ticket_info  # (TicketInfo) : TicketInfoOption / TicketInfoCheck / TicketInfoCounter


class TicketsGroup:
    def __init__(self, tickets: [Ticket], total_rules: TotalRules):
        self.tickets = tickets  # List of Ticket
        self.total_rules = total_rules  # object of TotalRules


class EventTicketsResponse:
    def __init__(self, event_id: str, tickets_groups: [TicketsGroup]) -> None:
        self.event_id = event_id  # string
        self.tickets_groups = tickets_groups  # list of TicketsGroup


class EventTicketsResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
