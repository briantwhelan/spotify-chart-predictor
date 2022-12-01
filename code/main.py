from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import extract_features, FEATURES_TO_EXTRACT
import pandas as pd
import csv
import os
from sys import argv

# Create duplicate free copy of csv file
def remove_duplicates(filename_in: str, filename_out: str) -> None:
    data = pd.read_csv(filename_in)
    no_dupes = data.drop_duplicates()
    no_dupes.to_csv(filename_out, index=False)

def combine_csvs() -> None:
    charted = []
    uncharted = []

    combined_file = './data/classifications.csv'
    # combined_uncharted_file = './data/uncharted/uncharted_combined/csv'

    for i in range(2000, 20000, 2000):
        charted_file = f'./data/charted/charted_{i}.csv'
        uncharted_file = f'./data/uncharted/uncharted_{i}.csv'

        if not (os.path.exists(charted_file) and os.path.exists(charted_file)):
            continue

        df_charted = pd.read_csv(charted_file)
        charted.extend(df_charted.to_numpy())
        df_uncharted = pd.read_csv(uncharted_file)
        uncharted.extend(df_uncharted.to_numpy())

    with open(combined_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator='\n')
        csvwriter.writerow(['track_id','charted'])
        csvwriter.writerows(charted)
        csvwriter.writerows(uncharted)


# Classify tracks in specified file as charted or not
def classify_training_tracks(in_filename: str, out_charted_filename: str, out_uncharted_filename: str) -> None:
    # Import list of songs.
    data = pd.read_csv(in_filename)
    songs = data.to_numpy()

    if(os.path.exists(out_charted_filename) and os.path.isfile(out_charted_filename)):
        os.remove(out_charted_filename)
    if(os.path.exists(out_uncharted_filename) and os.path.isfile(out_uncharted_filename)):
        os.remove(out_uncharted_filename)

    # Fields for writing to csv file.
    # fields = ["track","artist","charted",*(FEATURES_TO_EXTRACT)] 
    fields = ["track","charted"] 

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
            print(f'MISSING DATA')
            continue

        found, charted = has_charted(track, artist)
        if found and charted:
            print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
            # track_features = extract_features(track_id)
            # For each feature field: Value OR None
            # charted_songs.append([track,artist,True,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
            charted_songs.append([track_id,True])
        elif found:
            print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")
            # track_features = extract_features(track_id)
            # For each feature field: Value OR None
            # uncharted_songs.append([track,artist,False,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
            uncharted_songs.append([track_id,False])
        else:
            print('NOT FOUND')

        # Write to CSV files every 100 tracks for safety
        if i % 100 == 0:
            with open(out_charted_filename, 'w') as csvfile:  
                csvwriter = csv.writer(csvfile, lineterminator='\n') 
                csvwriter.writerow(fields) 
                csvwriter.writerows(charted_songs)

            with open(out_uncharted_filename, 'w') as csvfile:  
                csvwriter = csv.writer(csvfile, lineterminator='\n') 
                csvwriter.writerow(fields) 
                csvwriter.writerows(uncharted_songs)
    
    with open(out_charted_filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile, lineterminator='\n') 
        csvwriter.writerow(fields) 
        csvwriter.writerows(charted_songs)

    with open(out_uncharted_filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile, lineterminator='\n') 
        csvwriter.writerow(fields) 
        csvwriter.writerows(uncharted_songs)
    
# remove_duplicates("./data/recommendations.csv", "./data/recs_no_duplicates.csv")

if __name__ == '__main__':
    file_to_classify = argv[1]
    print(f'Classifying tracks in file {file_to_classify}...')
    classify_training_tracks(
        in_filename=f"./data/recs/recs_{file_to_classify}.csv",
        out_charted_filename=f"./data/charted/charted_{file_to_classify}.csv",
        out_uncharted_filename=f"./data/uncharted/uncharted_{file_to_classify}.csv"
    )
    # combine_csvs()
