from charts_data import CHARTING_THRESHOLD, has_charted
import pandas as pd
import csv
import os
from sys import argv
from utils import split_csv, fix_dodgy_file_number

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
        artist = song[4]
        print(f'{i}. {track} by {artist}')

        # Check for empty entries
        # (NaN is only value that evaluates as not equal to itself)
        if (track != track) or (artist != artist):
            print(f'MISSING DATA')
            continue

        found, top_pos = has_charted(track, artist)
        if found and top_pos <= CHARTING_THRESHOLD:
            print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
            # track_features = extract_features(track_id)
            # For each feature field: Value OR None
            # charted_songs.append([track,artist,True,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
            charted_songs.append([track_id,top_pos])
        elif found:
            print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")
            # track_features = extract_features(track_id)
            # For each feature field: Value OR None
            # uncharted_songs.append([track,artist,False,*(track_features.get(x,None) for x in FEATURES_TO_EXTRACT)])
            uncharted_songs.append([track_id,top_pos])
        else:
            print('NOT FOUND')
            uncharted_songs.append([track_id,1000])


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
    file_number = argv[1]
    print(f'Classifying tracks in file {file_number}...')
    classify_training_tracks(
        in_filename=f"./data/rec_splits/recs_{file_number}.csv",
        out_charted_filename=f"./data/charted/charted_{file_number}.csv",
        out_uncharted_filename=f"./data/uncharted/uncharted_{file_number}.csv"
    )
    # fix_dodgy_file_number(file_number)
    
    # combine_csvs()

    # headings = ['track_id','track_name','track_popularity','artist_id','artist_name','artist_popularity','artist_followers']
    # split_csv('./data/new_recs.csv', 500, './data/rec_splits', 'recs', headings)
    
    # print('Check main...')
