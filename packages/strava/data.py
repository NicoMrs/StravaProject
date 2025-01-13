# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 08:19:46 2023

@author: Nico
"""

import json
import requests
from packages.timing import Date

__all__ = ['get_activities']


def get_activities(access_token, before, after, per_page = 100):
    """ Return all activities from page_number """
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': 1, 'before': before, 'after': after}
    activities = requests.get(url="https://www.strava.com/api/v3/athlete/activities",
                              headers=header,
                              params=param).json()

    return activities


if __name__ == '__main__':
    access_token = "28809100886bf15dac680647dca65341a45bd5ea"

    marathons = []

    hamburg = Date(2022, 4, 24)
    activity = get_activities(access_token, before=hamburg.tolerance_up, after=hamburg.tolerance_down)
    marathons.append(activity)

    valence = Date(2022, 12, 4)
    activity = get_activities(access_token, before=valence.tolerance_up, after=valence.tolerance_down)
    marathons.append(activity)

    rotterdam = Date(2024, 4, 14)
    activity = get_activities(access_token, before=rotterdam.tolerance_up, after=rotterdam.tolerance_down)
    marathons.append(activity)

    # Save JSON file
    with open('Marathons.json', 'a') as outfile:
        json.dump(marathons, outfile)
