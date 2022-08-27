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
        datetime_now = datetime.datetime.now()

        case = ''

        if last_token_response['token'] is not None:
            # Check if token is usable (expiration_datetime)
            expiration_datetime = datetime.datetime.strptime(last_token_response['expiration_datetime'], "%Y-%m-%d %H:%M:%S")

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
            print("There is no token in db")
            case = 'A'  # Authorize because there was no token

        if case == 'A':  # Authorize
            print("CASE A: AUTHORIZE")
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

            print("Authorization token received from simplybook: " + response_json['token'])

            new_credentials = {
                "company": simplybook_credentials['company'],
                "token": response_json['token'],
                "refresh_token": response_json['refresh_token'],
                "expiration_datetime": datetime_now.strftime("%Y/%m/%d %H:%M:%S")
            }

            # SAVE THE NEW TOKEN IN DB
            print("Saving token to db: " + response_json['token'])
            self.save_token_in_db(simplybook_credentials, new_credentials['token'], new_credentials['refresh_token'], new_credentials['expiration_datetime'])

            print("Elements to return:")
            print("-- company: " + simplybook_credentials['company'])
            print("-- token: " + new_credentials['token'])
            print("-- refresh_token: " + new_credentials['refresh_token'])

            return {
                "company": simplybook_credentials['company'],
                "token": new_credentials['token'],
                "refresh_token": new_credentials['refresh_token']
            }

        elif case == 'B':  # Refresh
            print("CASE B: REFRESH")
            new_credentials = self.refresh({
                "company": simplybook_credentials['company'],
                "token": last_token_response['token'],
                "refresh_token": last_token_response['refresh_token']
            })

            print("Refreshed elements to return:")
            print("-- company: " + new_credentials['company'])
            print("-- token: " + new_credentials['token'])
            print("-- refresh_token: " + new_credentials['refresh_token'])

            # SAVE THE NEW TOKEN IN DB
            print("Saving refreshed data to db")
            self.save_token_in_db(simplybook_credentials, new_credentials['token'], new_credentials['refresh_token'], datetime_now.strftime("%Y/%m/%d %H:%M:%S"))

            return new_credentials

    def save_token_in_db(self, simplybook_credentials, token, refresh_token, expiration_datetime):
        # get the token from the backend
        url = general_utils.BACKEND_BASE + general_utils.BACKEND_URL_set_last_token

        auth_info = {
            "company": simplybook_credentials['company'],
            "token": token,
            "refresh_token": refresh_token,
            "expiration_datetime": expiration_datetime
        }

        payload = json.dumps({
            "booking_system_id": 3,
            "auth_info": auth_info
        })
        headers = {
            'ApiKey': simplybook_credentials['backend_apikey'],
            'accept': 'application/json',
            'Authorization': simplybook_credentials['backend_authorization'],
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("saved token to db. response is: " + response.text)


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
