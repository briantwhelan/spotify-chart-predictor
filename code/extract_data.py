import os
import requests
import json
from dotenv import load_dotenv

BASE_URL = 'https://api.spotify.com/v1/'

# Load environment variables.
load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Authenticate.
AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Need to pass access token into header to send properly formed GET request to API server
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# Get the track id for the specified track.
def get_track_id(artist, track):
  response = requests.get(BASE_URL + 'search?q=artist:' + artist + '%20track:' + track + '&type=track', headers=headers)
  response_json = response.json()
  return response_json['tracks']['items'][0]['id']

# Get the audio features for the specified track.
def get_track_audio_features(track):
  response = requests.get(BASE_URL + 'audio-features/' + track, headers=headers)
  response_json = response.json()
  return response_json

song = "Fearless"
print(song)
track = get_track_id("Taylor Swift", song)
features = get_track_audio_features(track)
json_formatted_str = json.dumps(features, indent=4)
print(json_formatted_str)