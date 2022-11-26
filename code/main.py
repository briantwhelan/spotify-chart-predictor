from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import get_track_id, extract_features
import pandas as pd
import numpy as np
from json import dumps
import csv
import os

# Import list of songs.
charted_songs = pd.read_csv("./data/charted_songs.csv")
uncharted_songs = pd.read_csv("./data/uncharted_songs.csv")
data = pd.concat([charted_songs, uncharted_songs], axis=0)
songs = data.to_numpy()

# Extract features from Spotify and classification from officialcharts.
features = []
for song in songs:
    track = song[1]
    artist = song[0]
    print(f'{track} by {artist}')
    if has_charted(track, artist):
        print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
    else:
        print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")
    track_id = get_track_id(track, artist)
    track_features = extract_features(track_id)
    features.append([track,artist,has_charted(track, artist),
                        track_features['danceability'],track_features['energy'],track_features['loudness'],
                        track_features['mode'],track_features['speechiness'],track_features['acousticness'],
                        track_features['instrumentalness'],track_features['liveness'],track_features['tempo'],
                        track_features['duration_ms'],track_features['time_signature'],track_features['num_sections']])



# Write to csv file.
filename = "./data/data.csv"
if(os.path.exists(filename) and os.path.isfile(filename)):
  os.remove(filename)
fields = ["track","artist","charted", 
            "danceability","energy","loudness",
            "mode","speechiness","acousticness", 
            "instrumentalness","liveness","tempo", 
            "duration_ms","time_signature","num_sections"] 
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(features)
    print("Data extracted")
    