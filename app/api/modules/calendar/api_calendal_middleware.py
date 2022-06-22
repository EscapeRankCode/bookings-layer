# GENERAL IMPORTS
from flask import Flask
from flask import request
import json
# PROJECT IMPORTS
from app.api.utils import GeneralUtils


class ApiCalendarMiddlewareMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApiCalendarMiddleware(ApiCalendarMiddlewareMeta):

    def __init__(cls):
        super().__init__()
        cls.schemes = GeneralUtils.get_schemes()

    def capture(self, api_request, endpoint: str):
        if endpoint is "getCalendarData":
            print("is getCalendarData")

        else:
            print("is not getCalendarData")
