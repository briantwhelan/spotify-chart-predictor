# Find next closed bracket after given index
def _next_close_bracket(string: str, after: int) -> int:
    cut_string = string[after:]
    return cut_string.find(')') + after

# Typical patterns in track names for featured artists
FEATURED_PATTERNS = [
    'featuring',
    'feat',
    'ft',
]
# Cut featured artists section out of track name
def _remove_featured_artists(track_name: str) -> str:
    lower = track_name.lower()
    for pattern in FEATURED_PATTERNS:
        # Check for "feat " or "feat.", not just "feat" in case of words like "feather"
        cut_index = max([lower.find('(' + pattern + ' '), lower.find('(' + pattern + '.')])

        if(cut_index != -1):
            # print(f'- {pattern} tag at {cut_index} -> "{track_name[cut_index]}{track_name[cut_index+1]}"')
            next_brack = _next_close_bracket(lower, cut_index)
            # print(f'- finished at {next_brack} -> "{track_name[next_brack - 1]}{track_name[next_brack]}"')
            return track_name[:cut_index].strip() + track_name[next_brack + 1:]
        
        # max because it will be one or the other, so one will be -1
        cut_index = max([track_name.find(' ' + pattern + ' '), track_name.find(' ' + pattern + '.')])
        if (cut_index != -1):
            return track_name[:cut_index].strip()

    return track_name

# Remove tags that indicate a track is from a movie or show
# e.g. Song Name - From Frozen
def _remove_from_tag(track_name: str) -> str:
    lower = track_name.lower()

    cut_index = lower.find('- from ')

    if cut_index != -1:
        return track_name[:cut_index].strip()

    return track_name

def clean_title(track_name: str) -> str:
    """
    Remove sections of title which might conflict with track name on charts.

    Currently removes:

        featured artist tags, e.g. Song (feat. Artist 2)
        
        'from' tags, e.g. Song - From Frozen
    """
    # Don't pass as lower because wan't to keep original case for scraping
    # Only use lower within individual functions for pattern matching
    return _remove_from_tag(_remove_featured_artists(track_name))