import os
import requests
from dotenv import load_dotenv
from json import dumps

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
def get_track_id(track_name: str, artist_name: str):
  response = requests.get(BASE_URL + 'search?q=artist:' + artist_name + '%20track:' + track_name + '&type=track', headers=headers)
  response_json = response.json()
  return response_json['tracks']['items'][0]['id']

# Get the audio features for the specified track.
def get_track_audio_features(track_id: str):
  response = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
  response_json = response.json()
  return response_json

# Only using for sections. Most other content is in audio_features.
def get_track_audio_analysis(track_id: str):
  response = requests.get(BASE_URL + 'audio-analysis/' + track_id, headers=headers)
  response_json = response.json()
  return response_json

# At the minute only using this to get the number of sections.
# Could do more with section start times, durations, etc. later on.
def get_track_sections(track_id: str):
  analysis = get_track_audio_analysis(track_id)
  sections = analysis['sections']
  return sections

# Extract desired features from data returned from API.
def extract_features(track_id: str):
  features = get_track_audio_features(track_id)
  sections = get_track_sections(track_id)

  return {
    **{key:value for key,value in features.items() if key in FEATURES_TO_EXTRACT},
    'num_sections': len(sections)
  }

# Other features which aren't included in the API data
#   are commented out but included here for convenience of reading.
FEATURES_TO_EXTRACT = {
  # Sound
  'acousticness',
  'danceability',
  'energy',
  'instrumentalness',
  'liveness',
  'loudness',
  'speechiness',
  'valence'
  # Musical
  'key',
  'mode',
  'tempo',
  'time_signature',
  # Meta
  'duration_ms'
  # 'num_sections'
}