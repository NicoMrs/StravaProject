from packages import strava
from packages.paths import Path
from packages.timing import Date
from packages.utils import save_json, clear_file

if __name__ == "__main__":

    #
    # ** Get User Credentials
    #

    # retrieve user info
    user_info = strava.get_data_from_json(Path.user_id())
    user = strava.StravaUser(**user_info)

    # refresh token
    refresh_token = strava.RefreshToken(strava_user=user)

    # access token
    access_token = strava.AccessToken(strava_user=user, refresh_token=refresh_token)
    print("access token:", access_token.token)

    #
    # ** Requests Data And Store
    #

    output_dir = 'data'

    marathons_days = {
        'hamburg': Date(2022, 4, 24),
        'valence': Date(2022, 12, 4),
        'rotterdam': Date(2024, 4, 14)
    }

    marathons = []
    for marathon, date in marathons_days.items():

        # retrieve marathon day
        activity = strava.get_activities(access_token=access_token.token,
                                         before=date.tolerance_up,
                                         after=date.tolerance_down)
        marathons.extend(activity)

        # retrieve all data per race
        activities = strava.get_activities(access_token=access_token.token,
                                           before=date.tolerance_down,
                                           after=date.start_training.timestamp)

        clear_file(output_dir, f"{marathon}.json")
        save_json(output_dir, f"{marathon}.json", activities)

    clear_file(output_dir, 'marathons.json')
    save_json(output_dir, 'marathons.json', marathons)

