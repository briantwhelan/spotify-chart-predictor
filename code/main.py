from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import get_track_id, extract_features
import pandas as pd
import numpy as np
from json import dumps
import csv
import os

# Import list of songs.
data = pd.read_csv("./data/songs.csv")
songs = data.to_numpy()

# Extract features from Spotify and classification from officialcharts.
charted_songs = []
uncharted_songs = []
for song in songs:
    track_id = song[0]
    track = song[1]
    artist = song[3]
    print(f'{track} by {artist}')
    found, charted = has_charted(track, artist)
    if found and charted:
        print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
        #track_id = get_track_id(track, artist)
        track_features = extract_features(track_id)
        charted_songs.append([track,artist,True,
            track_features['danceability'],track_features['energy'],track_features['loudness'],
            track_features['mode'],track_features['speechiness'],track_features['acousticness'],
            track_features['instrumentalness'],track_features['liveness'],track_features['tempo'],
            track_features['duration_ms'],track_features['time_signature'],track_features['num_sections']])
    elif found:
        print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")
        #track_id = get_track_id(track, artist)
        track_features = extract_features(track_id)
        uncharted_songs.append([track,artist,False,
            track_features['danceability'],track_features['energy'],track_features['loudness'],
            track_features['mode'],track_features['speechiness'],track_features['acousticness'],
            track_features['instrumentalness'],track_features['liveness'],track_features['tempo'],
            track_features['duration_ms'],track_features['time_signature'],track_features['num_sections']])

# Write to csv file.
fields = ["track","artist","charted", 
            "danceability","energy","loudness",
            "mode","speechiness","acousticness", 
            "instrumentalness","liveness","tempo", 
            "duration_ms","time_signature","num_sections"] 

filename = "./data/charted_songs.csv"
if(os.path.exists(filename) and os.path.isfile(filename)):
  os.remove(filename)
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(charted_songs)

filename = "./data/uncharted_songs.csv"
if(os.path.exists(filename) and os.path.isfile(filename)):
  os.remove(filename)
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(uncharted_songs)
    