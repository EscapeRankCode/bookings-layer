import json
from enum import IntEnum
from json import JSONEncoder

class UserInput:
    def __init__(self, user_input_text: str, user_input_value: str, user_input_others_map: dict):
        self.user_input_text = user_input_text
        self.user_input_value = user_input_value
        self.user_input_others_map = user_input_others_map

    def __iter__(self):
        yield from {
            "user_input_text": self.user_input_text,
            "user_input_value": self.user_input_value,
            "user_input_others_map": self.user_input_others_map
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "user_input_text": self.user_input_text,
            "user_input_value": self.user_input_value,
            "user_input_others_map": json.dumps(self.user_input_others_map)
        }

class FieldType(IntEnum):
    check = 1
    text = 2
    number = 3
    select = 4
    date = 5
    unknown = 6

class FieldOption:
    def __init__(self, option_text: str, option_value: str, option_others_map: dict):
        self.option_text = option_text  # str
        self.option_value = option_value  # str
        self.option_others_map = option_others_map  # dict {}

    def __iter__(self):
        yield from {
            "option_text": self.option_text,
            "option_value": self.option_value,
            "option_others_map": self.option_others_map
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "option_text": self.option_text,
            "option_value": self.option_value,
            "option_others_map": json.dumps(self.option_others_map)
        }

class Field:
    def __init__(self, field_type: FieldType, field_required: bool, field_key: str, field_text: str, field_default_value: str, field_options: [FieldOption], user_input: UserInput):
        self.field_type = field_type  # FieldType
        self.field_required = field_required  # bool
        self.field_key = field_key  # str
        self.field_text = field_text  # str
        self.field_default_value = field_default_value  # str
        self.field_options = field_options  # list of [FieldOption]
        self.user_input = user_input  # UserInput

    def __iter__(self):
        yield from {
            "field_type": self.field_type,
            "field_required": self.field_required,
            "field_key": self.field_key,
            "field_text": self.field_text,
            "field_default_value": self.field_default_value,
            "field_options": self.field_options,
            "user_input": self.user_input
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):

        if self.user_input == None:
            user_input_json = None
        else:
            user_input_json = self.user_input.to_json()

        options_json = []
        for option in self.field_options:
            options_json.append(option.to_json())

        return {
            "field_type": self.field_type,
            "field_required": self.field_required,
            "field_key": self.field_key,
            "field_text": self.field_text,
            "field_default_value": self.field_default_value,
            "field_options": options_json,
            "user_input": user_input_json
        }

class EventFormResponse:
    def __init__(self, event_id: str, fields: [Field]):
        self.event_id = event_id
        self.fields = fields

    def __iter__(self):
        yield from {
            "event_id": self.event_id,
            "fields": self.fields
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        fields_json = []
        for field in self.fields:
            fields_json.append(field.to_json())

        return {
            "event_id": self.event_id,
            "fields": fields_json
        }


class EventFormResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
