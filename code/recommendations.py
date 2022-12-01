from spotify_data import get_recommendations
from csv import writer

GENRES = 'alternative,blues,british,classical,club,country,dance,disco,disney,dubstep,electronic,emo,folk,funk,grunge,hip-hop,holidays,house,indie,jazz,k-pop,kids,latin,metal,new-release,opera,pop,rock,rock-n-roll,romance,show-tunes,soul,summer,techno,trance'
GENRES = GENRES.split(',')
recs = []

iterations = 100
for iteration in range(iterations):
    for i, g in enumerate(GENRES):
        recs.append(get_recommendations(seed_genres=f'{g}'))
    print(f'{iteration + 1}/{iterations} completed')

print('Requests complete')

rows = []

for rec in recs:
    for track in rec:
        track_id = track['id']
        track_name = track['name']
        
        artist = track['artists'][0]
        artist_id = artist['id']
        artist_name = artist['name']

        rows.append([track_id, track_name, artist_id, artist_name])

filename = './data/recommendations.csv'
headings = ['track_id', 'track_name', 'artist_id', 'artist_name']

with open(filename, 'w', encoding="utf-8") as file:
    out = writer(file, lineterminator='\n')
    out.writerow(headings)
    out.writerows(rows)
    