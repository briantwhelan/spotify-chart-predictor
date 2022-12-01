import os
import requests
from dotenv import load_dotenv
from json import dumps
from math import ceil

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

def get_batch_audio_features(track_ids: str) -> list:
  """
  params: (str) comma separated list of track ids to get features for

  return: (list<dict>) list of audio features for input tracks
  """
  response = requests.get(BASE_URL + f'audio-features?ids={track_ids}', headers=headers)
  response_json = response.json()
  return response_json['audio_features']

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
  # sections = get_track_sections(track_id)

  return {
    **{key:value for key,value in features.items() if key in FEATURES_TO_EXTRACT}
    # 'num_sections': len(sections)
  }

def batch_features(track_ids: list) -> list:
  """
  Makes as many API calls as necessary to get features for tracks in input list.

  Each API call returns features for up to 100 tracks, so be weary of API rate limits for larger input lists.

  params:
    track_ids: list<str> -> list of any number of track IDs.

  return: list<dict> -> list of track features for each ID in input list 
  """
  features = []
  print(f'Starting {ceil(len(track_ids) / 100)} API calls to get features for {len(track_ids)} tracks...\nThis may take a while...')

  ids_processed = 0
  while ids_processed < len(track_ids):
    offset = min(100, len(track_ids) - ids_processed)
    ids_processed += offset
    
    print(f'Getting features for {ids_processed - offset} to {ids_processed - 1}')
    curr = track_ids[ids_processed - offset : ids_processed]
    
    ids_string = curr[0]
    for id in curr[1:]:
      ids_string += f',{id}'
    
    # features.append(*get_batch_audio_features(ids_string))
    features.extend(get_batch_audio_features(ids_string))

  return features

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
  'valence',
  # Musical
  'key',
  'mode',
  'tempo',
  'time_signature',
  # Meta
  'duration_ms'
  # 'num_sections'
}

def get_genre_seeds():
  response = requests.get(BASE_URL + 'recommendations/available-genre-seeds', headers=headers)
  response_json = response.json()
  return response_json

REC_LIMIT=100
def get_recommendations(seed_artists = '', seed_genres = '', seed_tracks=''):
  response = requests.get(BASE_URL + f'recommendations?seed_artists={seed_artists}&seed_genres={seed_genres}&seed_tracks={seed_tracks}&limit={REC_LIMIT}', headers=headers)
  response_json = response.json()
  return response_json['tracks']
