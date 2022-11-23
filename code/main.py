from charts_data import CHARTING_THRESHOLD, has_charted

track = "Love Story (Taylor's Version)"
artist = "Taylor Swift"
print(f'{track} by {artist}')

if has_charted(track, artist):
    print(f"YES - Has charted in Top {CHARTING_THRESHOLD}")
else:
    print(f"NO - Has not charted in Top {CHARTING_THRESHOLD}")

# track = get_track_id(artist, song)
# features = extract_features(track)
# print(dumps(features, indent=2))