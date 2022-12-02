from spotify_data import get_recommendations, batch_artists
import numpy as np
from csv import writer
from json import dumps

GENRES = 'alternative,blues,british,classical,club,country,dance,disco,disney,dubstep,electronic,emo,folk,funk,grunge,hip-hop,holidays,house,indie,jazz,k-pop,kids,latin,metal,new-release,opera,pop,rock,rock-n-roll,romance,show-tunes,soul,summer,techno,trance'
GENRES = GENRES.split(',')
recs = []

iterations = 100
for iteration in range(iterations):
    for i, g in enumerate(GENRES):
        try:
            recs.append(get_recommendations(seed_genres=f'{g}'))
        except:
            print(f'Error with genre {i}: {g}')

    print(f'{iteration + 1}/{iterations} completed')

print('Requests complete')

rows: list[list] = []
genres = []

track_ids = []
artist_ids = []

for rec in recs:
    for track in rec:
        track_id = track['id']
        track_name = track['name']
        track_pop = track['popularity']
        # print(f'Track {track_name}: {track_pop}')
        
        artist = track['artists'][0]

        # print(dumps(artist, indent=2))

        artist_id = artist['id']
        artist_name = artist['name']

        artist_ids.append(artist_id)

        # rows.append([track_id, track_name, track_pop, artist_id, artist_name, artist_pop, artist_followers])
        rows.append([track_id, track_name, track_pop, artist_id, artist_name])
        # genres.append([track_id, *artist_genres])


artists = batch_artists(artist_ids)

# for i, row in enumerate(rows):
for i, artist in enumerate(artists):
    artist_id = artist['id']
    artist_pop = artist['popularity']
    artist_followers = artist['followers']['total']
    artist_genres = artist['genres']

    if rows[i][3] == artist_id:
        rows[i].extend([artist_pop, artist_followers])
        genres.append([artist_id, *artist_genres])
    else:
        print('Mismatch')

# Remove duplicates
recs_no_dups = []
for elem in rows:
    if elem not in recs_no_dups:
        recs_no_dups.append(elem)
genres_no_dups = []
for elem in genres:
    if elem not in genres_no_dups:
        genres_no_dups.append(elem)

file_recs = './data/new_recs.csv'
headings = ['track_id', 'track_name', 'track_popularity', 'artist_id', 'artist_name', 'artist_popularity', 'artist_followers']

file_genres = './data/new_genres.csv'
# headings_genres = ['track_id', '']

with open(file_recs, 'w', encoding="utf-8") as file:
    out = writer(file, lineterminator='\n')
    out.writerow(headings)
    out.writerows(recs_no_dups)

with open(file_genres, 'w', encoding="utf-8") as file:
    out = writer(file, lineterminator='\n')
    out.writerows(genres_no_dups)
    