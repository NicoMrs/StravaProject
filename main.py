
from packages import strava
from packages.paths import Path

if __name__ == "__main__":
    # retrieve user info
    user_info = strava.get_data_from_json(Path.user_id())
    user = strava.StravaUser(**user_info)

    # refresh token
    refresh_token = strava.RefreshToken(strava_user=user)

    # access token
    access_token = strava.AccessToken(strava_user=user, refresh_token=refresh_token)
    print("access token:", access_token.token)