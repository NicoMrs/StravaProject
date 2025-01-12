# token.py

import json
import os
import requests
from datetime import datetime

from ..paths import Path

__all__ = [
    'StravaUser',
    'RefreshToken',
    'AccessToken',
    'get_data_from_json'
]


def get_data_from_json(json_file):
    """ Returns data from json file """
    with open(json_file, 'r') as f:
        data = json.load(f)
        return data


class StravaUser:
    """ Store user id """

    def __init__(self, client_id, client_secret, redirect_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

    def __repr__(self):
        cls_name = type(self).__name__
        return (f"{cls_name}(client_id={self.client_id!r}, "
                f"client_secret={self._obfuscate(self.client_secret)!r}, "
                f"redirect_rul={self.redirect_url!r}")

    @staticmethod
    def _obfuscate(code):
        return f"{code[0:3]}**..."


class Token:
    def __init__(self, strava_user):
        if not isinstance(strava_user, StravaUser):
            raise TypeError(f"{strava_user} must be of type StravaUser")
        self.user = strava_user

    def __repr__(self):
        return f"{type(self).__name__}(user={self.user})"


class RefreshToken(Token):
    """ Refresh token is permanent. It enables the user to get a new access token which is temporary"""

    def __init__(self, strava_user):
        super().__init__(strava_user)
        self.token = self.get_refresh_token()

    def get_refresh_token(self):
        """
        Returns refresh token
        If not available from saved file, request a new one from Strava API. Then save it to a new json file
        """

        # Request from API
        if not os.path.isfile(Path.refresh_token()):
            print("Token not available, request from API")
            self._request_and_save_from_API()

        # Read from saved json
        data = get_data_from_json(Path.refresh_token())
        return data['refresh_token']

    def _request_and_save_from_API(self):
        """ Request refresh token from the API and save it in a json file"""

        # Authorization URL
        request_url = f'http://www.strava.com/oauth/authorize?client_id={self.user.client_id}' \
                      f'&response_type=code&redirect_uri={self.user.redirect_url}' \
                      f'&approval_prompt=force' \
                      f'&scope=profile:read_all,activity:read_all'

        # User prompt showing the Authorization URL
        # and asks for the code
        print('Click here:', request_url)
        print('Please authorize the app and copy&paste below the generated code!')
        print('P.S: you can find the code in the URL')
        code = input('Insert the code from the url: ')

        # Get the access token
        print('Requesting Refresh Token from API, response time might be long ...\n')
        token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                              data={'client_id': self.user.client_id,
                                    'client_secret': self.user.client_secret,
                                    'code': code,
                                    'grant_type': 'authorization_code'},
                              )

        # Save json response as a variable
        strava_token = token.json()

        # Save token
        with open(Path.refresh_token(), 'w') as outfile:
            json.dump(strava_token, outfile)

        print(f"SUCCESS: refresh token has been saved to {Path.refresh_token()}")


class AccessToken(Token):

    def __init__(self, strava_user, refresh_token):
        super().__init__(strava_user)

        if not isinstance(refresh_token, RefreshToken):
            raise TypeError(f"{refresh_token} must be of type RefreshToken")

        self.refresh_token = refresh_token
        self.expiring_time = None
        self.token = None

        self._initialize()

    def _initialize(self):
        """ Initialize attributes"""
        self.expiring_time = self.get_expire_time()
        self.token = self.get_access_token()

    @staticmethod
    def get_expire_time():
        """
        :return: expire time if found
        """

        # Request from API
        if not os.path.isfile(Path.access_token()):
            print("Token not available, must be requested from API\n")
            return None

        # Read from saved json
        data = get_data_from_json(Path.access_token())
        return data['expires_at']

    def _check_expiring_time(self):
        """ Check if access token has expired """
        current_time = datetime.now()
        expiring_time = datetime.fromtimestamp(self.expiring_time)
        if expiring_time > current_time:
            print("Access token still valid, remaining time:", expiring_time - current_time)
            return True
        return False

    def get_access_token(self):
        """
        Returns access token
        Check existing file if it exists. Check expiring time. Return access_token if found.
        Otherwise, request a new one from Strava API. Then save it to a new json file
        """

        # Request from API
        if not os.path.isfile(Path.access_token()) or not self._check_expiring_time():
            print("Token not available, request from API")
            self._request_from_API_and_save()

        # Read from saved json
        data = get_data_from_json(Path.access_token())
        return data['access_token']

    def _request_from_API_and_save(self):
        auth_url = "https://www.strava.com/oauth/token"

        # replace variables with values for your account
        payload = {
            'client_id': self.user.client_id,
            'client_secret': self.user.client_secret,
            'refresh_token': self.refresh_token.token,
            'grant_type': "refresh_token",
            'f': 'json'
        }

        print('Requesting Access Token from API, response time might be long ...\n')
        token = requests.post(auth_url, data=payload, verify=False)

        access_token = token.json()

        # Save token
        with open(Path.access_token(), 'w') as outfile:
            json.dump(access_token, outfile)

        print(f"SUCCESS: access token has been saved to {Path.access_token()}")

        # update expiring time
        self.expiring_time = self.get_expire_time()


if __name__ == "__main__":
    # retrieve user info
    user_info = get_data_from_json(Path.user_id())
    user = StravaUser(**user_info)

    # refresh token
    refresh_token = RefreshToken(strava_user=user)

    # access token
    access_token = AccessToken(strava_user=user, refresh_token=refresh_token)
    print("access token:", access_token.token)
