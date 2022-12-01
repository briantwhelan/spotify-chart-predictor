from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import extract_features, FEATURES_TO_EXTRACT
import pandas as pd
import csv
import os

# Create duplicate free copy of csv file
def remove_duplicates(filename_in: str, filename_out: str) -> None:
    data = pd.read_csv(filename_in)
    no_dupes = data.drop_duplicates()
    no_dupes.to_csv(filename_out, index=False)

# Classify tracks in specified file as charted or not
def classify_training_tracks(filename) -> None:
    # Import list of songs.
    data = pd.read_csv(filename)
    songs = data.to_numpy()

    filename_charted = "./data/charted_2.csv"
    filename_uncharted = "./data/uncharted_2.csv"

    if(os.path.exists(filename_charted) and os.path.isfile(filename_charted)):
        os.remove(filename_charted)
    if(os.path.exists(filename_uncharted) and os.path.isfile(filename_uncharted)):
        os.remove(filename_uncharted)

    # Fields for writing to csv file.
    fields = ["track","artist","charted",*(FEATURES_TO_EXTRACT)] 

    # Extract features from Spotify and classification from officialcharts.
    charted_songs = []
    uncharted_songs = []
    for i, song in enumerate(songs):
        track_id = song[0]
        track = song[1]
        artist = song[3]
        print(f'{i}. {track} by {artist}')

        # Check for empty entries
        # (NaN is only value that evaluates as not equal to itself)
        if (track != track) or (artist != artist):
            print(f'NO DATA')
            continue

        found, charted = has_charted(track, artist)
        if found and charted:
            print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
            track_features = extract_features(track_id)
            # For each feature field: Value OR None
            charted_songs.append([track,artist,True,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
        elif found:
            print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")
            track_features = extract_features(track_id)
            # For each feature field: Value OR None
            uncharted_songs.append([track,artist,False,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
        else:
            print('NOT FOUND')

        # Write to CSV files every 100 tracks for safety
        if i % 100 == 0:
            with open(filename_charted, 'w') as csvfile:  
                csvwriter = csv.writer(csvfile, lineterminator='\n') 
                csvwriter.writerow(fields) 
                csvwriter.writerows(charted_songs)

            with open(filename_uncharted, 'w') as csvfile:  
                csvwriter = csv.writer(csvfile, lineterminator='\n') 
                csvwriter.writerow(fields) 
                csvwriter.writerows(uncharted_songs)
    
    with open(filename_charted, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile, lineterminator='\n') 
        csvwriter.writerow(fields) 
        csvwriter.writerows(charted_songs)

    with open(filename_uncharted, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile, lineterminator='\n') 
        csvwriter.writerow(fields) 
        csvwriter.writerows(uncharted_songs)
    
# remove_duplicates("./data/recommendations.csv", "./data/recs_no_duplicates.csv")
classify_training_tracks("./data/recs_no_duplicates.csv")
