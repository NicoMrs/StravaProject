## Requesting And Store Data Using the Strava API

This application is designed to requests personnal data through the Strava API.

<p align="center">
  <img src="images/strava.png?raw=true" width="200">
</p>

Before requesting your data, one needs its:
 - client_id
 - client_secret

You can find client ID and client secret in your [application page](https://www.strava.com/settings/api). 

Then you should update the [user_id.json](https://github.com/NicoMrs/Strava/tree/main/packages/strava/user_info) with these information.

Once it is done, you can run main... 


### a. Get Credentials
The first part will help you retrieve your credentials necessary to make requests to the API. You will retrieve your refresh_token which is permanent 
along with an access_token which is temporary. Once requested, the access_token and the refresh_token will be saved to json files in './packages/strava/user_info'
When a new request is made the access_token is either:
- read from the json file if still valid 
- requested then saved in the json file if not valid anymore


### b. Get The Data
You can start the app to download your personnal data. 

The application is set to download the data concerning 3 marathons done on:
- Hamburg 	24/04/2022
- Valence 	04/12/2022
- Rotterdam 	14/04/2024

As well as all activities during the 16 weeks preceding the marathons. 

The data will be stored in './data'.