import json

import requests

from app.api.modules.auth.api_auth_interface import ApiAuthInterface
from app.api.utils import general_utils


class SimplybookApiAuth(ApiAuthInterface):

    AUTH_FILE = "/home/ubuntu/bookingslayer/bookings-layer/app/api/modules/auth/adapters/simplybook/credentials.json"

    def authorize(self, auth_credentials):
        """
        Returns a map with the token and the refresh_token
        :param auth_credentials: None

        Infomration is in a json file
        {
            "company": "xxxxxx",
            "login": "xxxxxx",
            "password": "xxxxxx"
        }
        :return: a map with the token and the refresh token
        {
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "refresh_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        """

        credentials_file = open(self.AUTH_FILE)
        simplybook_credentials = json.load(credentials_file)

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_authorize

        payload = json.dumps({
            "company": simplybook_credentials['company'],
            "login": simplybook_credentials['login'],
            "password": simplybook_credentials['password']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        print("RESPONSE OF -AUTHORIZE-")
        print(response.text)

        print("TOKEN: " + response_json['token'])
        print("REFRESH TOKEN: " + response_json['refresh_token'])

        return {
            "company": simplybook_credentials['company'],
            "token": response_json['token'],
            "refresh_token": response_json['refresh_token']
        }

    def refresh(self, auth_credentials):
        """
        Returns a map with the token and the refresh_token
        :param auth_credentials: {
            "company" : "xxxxxxxxxx",
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "refresh_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }

        Infomration is in a json file
        {
            "company": "xxxxxx",
            "login": "xxxxxx",
            "password": "xxxxxx"
        }
        :return: a map with the token and the refresh token
        {
            "company" : "xxxxxxxxxx",
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "refresh_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        """

        credentials_file = open(self.AUTH_FILE)
        simplybook_credentials = json.load(credentials_file)

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_authorize

        payload = json.dumps({
            "company": simplybook_credentials['company'],
            "refresh_token": auth_credentials['refresh_token']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        print("RESPONSE OF -REFRESH-")
        print(response.text)

        print("TOKEN: " + response_json['token'])
        print("REFRESH TOKEN: " + response_json['refresh_token'])

        return {
            "company": simplybook_credentials['company'],
            "token": response_json['token'],
            "refresh_token": response_json['refresh_token']
        }
