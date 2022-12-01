from spotify_data import batch_features, FEATURES_TO_EXTRACT
from csv import writer
import pandas as pd

in_file = './data/recs_no_duplicates.csv'
out_file = './data/features.csv'

df = pd.read_csv(in_file)
df = df['track_id']

arr = df.to_numpy()
all_features = batch_features(arr)

fields = ['track_id', *(FEATURES_TO_EXTRACT)]
rows = []

for i in range(len(arr)):
    rows.append([arr[i], *(all_features[i].get(feat,None) for feat in FEATURES_TO_EXTRACT)])

with open(out_file, 'w') as csvfile:
    csvwriter = writer(csvfile, lineterminator='\n')
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
