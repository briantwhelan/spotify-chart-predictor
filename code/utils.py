import pandas as pd
import os

def stitch():
    # Stitch charted and uncharted classifications.
    charted_classifications = pd.DataFrame()
    uncharted_classifications = pd.DataFrame()
    for i in range(2000, 20000, 2000):
        charted_file = f'./data/charted/charted_{i}.csv'
        uncharted_file = f'./data/uncharted/uncharted_{i}.csv'
        if (os.path.exists(charted_file) and os.path.exists(uncharted_file)):  
            charted = pd.read_csv(charted_file)
            uncharted = pd.read_csv(uncharted_file)
            charted_classifications = pd.concat([charted_classifications, charted])
            uncharted_classifications = pd.concat([uncharted_classifications, uncharted])
    charted_classifications.to_csv('./data/charted/charted.csv', sep=',', encoding='utf-8', index=False)
    uncharted_classifications.to_csv('./data/uncharted/uncharted.csv', sep=',', encoding='utf-8', index=False)

    # Stitch features and classifications.
    features = pd.read_csv('./data/features.csv')
    charted_data = pd.merge(features, charted_classifications, left_on="track_id", right_on="track", how="inner")
    charted_data.to_csv('./data/charted_songs.csv', sep=',', encoding='utf-8', index=False)
    uncharted_data = pd.merge(features, uncharted_classifications, left_on="track_id", right_on="track", how="inner")
    uncharted_data.to_csv('./data/uncharted_songs.csv', sep=',', encoding='utf-8', index=False)

def split_csv(filename: str, increment_size: int, output_dir: str) -> None:
    csvfile = open(filename, 'r').readlines()
    number = 1
    for i in range(len(csvfile)):
        if i % increment_size == 0:
            open(f'{output_dir}/{filename}_{number}.csv', 'w').writelines(csvfile[i:i+increment_size])
            number += 1
