import pandas as pd
import os
from csv import writer, reader

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

def split_csv(filename: str, increment_size: int, output_dir: str = './splits', title: str = 'split', headings: list = []) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read input csv file
    with open(filename, 'r', encoding="utf-8") as csv_in:
        csvreader = reader(csv_in)
        rows = []
        number = 0

        # Keep record of all rows, and output in blocks of specified size
        for i, row in enumerate(csvreader):
            rows.append(row)
            if i % increment_size == 0 and i != 0:
                with open(f'{output_dir}/{title}_{number}.csv', 'w', encoding='utf-8') as csv_out:
                    csvwriter = writer(csv_out, lineterminator='\n')
                    csvwriter.writerow(headings)
                    csvwriter.writerows(rows)
                    rows = []
                number += 1

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
        csvwriter = writer(csvfile, lineterminator='\n')
        csvwriter.writerow(['track_id','charted'])
        csvwriter.writerows(charted)
        csvwriter.writerows(uncharted)

# Create duplicate free copy of csv file
def remove_duplicates(filename_in: str, filename_out: str) -> None:
    data = pd.read_csv(filename_in)
    no_dupes = data.drop_duplicates()
    no_dupes.to_csv(filename_out, index=False)