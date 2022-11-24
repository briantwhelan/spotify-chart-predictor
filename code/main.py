from charts_data import CHARTING_THRESHOLD, has_charted
from spotify_data import get_recommendations
from json import dumps
from csv import writer


# print(dumps(get_genre_seeds(), indent=2))

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

# recs = get_recommendations(seed_artists='', seed_genres='', seed_tracks='')
print('Requests complete')

# print(recs)
# print(dumps(recs[0][0]['name'], indent=2))

# recs is a list of lists of tracks
# rec is a list of tracks
    
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

filename = 'recommendations.csv'
headings = ['track_id', 'track_name', 'artist_id', 'artist_name']

with open(filename, 'w') as file:
    out = writer(file)
    out.writerow(headings)
    out.writerows(rows)

# print(dumps(recs[0], indent=2))



# track = "Love Story (Taylor's Version)"
# artist = "Taylor Swift"
# print(f'{track} by {artist}')

# if has_charted(track, artist):
#     print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
# else:
#     print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")

# track = get_track_id(artist, song)
# features = extract_features(track)
# print(dumps(features, indent=2))