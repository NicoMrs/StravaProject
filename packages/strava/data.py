# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 08:19:46 2023

@author: Nico
"""

import json
import os
import requests
import time


accessToken = "e50a62114af364414a571e6d3e9af4ea057f6d58"


#
## GET ALL ACTIVITIES
#

def acitivities_from_page(access_token, page_number):
    """
    Get all activities from page_number
    """
    
    bearer_header = "Bearer " + str(access_token)
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page':  page_number}
    activities = requests.get(activites_url, headers=header, params=param).json()
    
    return activities

activities = acitivities_from_page(accessToken, 1)


# Save JSON file
with open('activities.json', 'w') as outfile:
  json.dump(activities, outfile)

## Get all activities

# for i in range(1,5):
    
#     activities = acitivities_from_page(accessToken, i)
#     # Save JSON file
#     with open('activities{0}.json'.format(i), 'w') as outfile:
#       json.dump(activities, outfile)
    

#
## GET ACTIVITIES BY ID
#

# GET /activities/{id}/laps

def laps_from_activity(activity_id, access_token):
    
    bearer_header = "Bearer " + str(access_token)
    strava_activity_url = "https://www.strava.com/api/v3/activities/" + str(activity_id) + "/laps"
    headers = {'Content-Type': 'application/json', 'Authorization': bearer_header}
    response = requests.get(strava_activity_url, headers=headers, )
    more_activity_data = response.json()
    
    return more_activity_data

activity_id = 7924812139
activity = laps_from_activity(activity_id, accessToken)

# Save JSON file
with open('activity_{}.json'.format(activity_id), 'w') as outfile:
  json.dump(activity  , outfile)


