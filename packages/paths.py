# paths.py

import os


class Path:
    """ Class that manages path directory """
    ROOT_DIR = 'packages\\strava\\user_info'

    @classmethod
    def refresh_token(cls):
        return os.path.join(os.getcwd(), cls.ROOT_DIR, 'refresh_token.json')

    @classmethod
    def access_token(cls):
        return os.path.join(os.getcwd(), cls.ROOT_DIR, 'access_token.json')

    @classmethod
    def user_id(cls):
        return os.path.join(os.getcwd(), cls.ROOT_DIR, 'user_id.json')
