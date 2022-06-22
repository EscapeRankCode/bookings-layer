# GENERAL IMPORTS
from flask import Flask
from flask import request
import json


class ApiCalendarMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiCalendar(metaclass=ApiCalendarMeta):
    def get_calendar_data(self, api_request) -> str:
        return "{Hello World}"
