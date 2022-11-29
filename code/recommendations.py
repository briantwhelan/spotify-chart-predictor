from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import get_recommendations
from json import dumps
from csv import writer

GENRES = 'alternative,blues,british,classical,club,country,dance,disco,disney,dubstep,electronic,emo,folk,funk,grunge,hip-hop,holidays,house,indie,jazz,k-pop,kids,latin,metal,new-release,opera,pop,rock,rock-n-roll,romance,show-tunes,soul,summer,techno,trance'
GENRES = GENRES.split(',')
recs = []

set_of_five = ''
for i, g in enumerate(GENRES):
    if (i % 5 == 0 and i != 0):
        print(f'i = {i} : {set_of_five}')
        recs.append(get_recommendations(seed_genres=set_of_five))
        set_of_five = g
    elif i == len(GENRES) - 1:
        set_of_five += f',{g}'
        print(f'i = {i} : {set_of_five}')
        recs.append(get_recommendations(seed_genres=set_of_five))
    elif i != 0:
        set_of_five += f',{g}'
    else:
        set_of_five += g

print('Requests complete')
    
rows = []

for rec in recs:
    for track in rec:
        track_id = track['id']
        track_name = track['name']
        
        artist = track['artists'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        # print(f'{track_name} - {artist_name}')
        rows.append([track_id, track_name, artist_id, artist_name])

filename = './data/recommendations.csv'
headings = ['track_id', 'track_name', 'artist_id', 'artist_name']

with open(filename, 'w') as file:
    out = writer(file)
    out.writerow(headings)
    out.writerows(rows)