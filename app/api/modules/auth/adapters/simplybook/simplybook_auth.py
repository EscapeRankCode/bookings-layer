import datetime
import json

import requests

from app.api.modules.auth.api_auth_interface import ApiAuthInterface
from app.api.utils import general_utils


class SimplybookApiAuth(ApiAuthInterface):

    AUTH_FILE = "/home/ubuntu/bookingslayer/bookings-layer/app/api/modules/auth/adapters/simplybook/credentials.json"
    EXPIRATION_TIME_LIMIT = 20

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

        # get the token from the backend
        url = general_utils.BACKEND_BASE + general_utils.BACKEND_URL_get_last_token

        payload = json.dumps({
            "booking_system_id": 3,
            "auth_info": None
        })
        headers = {
            'ApiKey': simplybook_credentials['backend_apikey'],
            'accept': 'application/json',
            'Authorization': simplybook_credentials['backend_authorization'],
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        last_token_response = json.loads(response.text)

        case = ''

        if last_token_response['token'] is not None:
            # Check if token is usable (expiration_datetime)
            expiration_datetime = datetime.datetime.strptime(last_token_response['expiration_datetime'], "")
            datetime_now = datetime.datetime.now()

            if datetime_now > expiration_datetime:
                case = 'A'  # Authorize

            else:
                minutes_remaining = divmod((expiration_datetime - datetime_now).total_seconds(), 60)[0]
                if minutes_remaining < self.EXPIRATION_TIME_LIMIT:
                    case = 'B'  # Refresh
                else:
                    return {
                        "company": simplybook_credentials['company'],
                        "token": last_token_response['token'],
                        "refresh_token": last_token_response['refresh_token']
                    }
        else:
            case = 'A'  # Authorize because there was no token

        if case == 'A':  # Authorize
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

            return {
                "company": simplybook_credentials['company'],
                "token": response_json['token'],
                "refresh_token": response_json['refresh_token']
            }

        elif case == 'B':  # Refresh
            return self.refresh({
                "company": simplybook_credentials['company'],
                "token": last_token_response['token'],
                "refresh_token": last_token_response['refresh_token']
            })


    def refresh(self, auth_credentials):
        """
        Returns a map with the token and the refresh_token.
        param auth_credentials: {
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

        # credentials_file = open(self.AUTH_FILE)
        # simplybook_credentials = json.load(credentials_file)

        url = general_utils.SIMPLYBOOK_BS_HOST + general_utils.SIMPLYBOOK_BS_refresh

        payload = json.dumps({
            "company": auth_credentials['company'],
            "refresh_token": auth_credentials['refresh_token']
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)

        return {
            "company": auth_credentials['company'],
            "token": response_json['token'],
            "refresh_token": response_json['refresh_token']
        }
