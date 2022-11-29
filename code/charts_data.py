from bs4 import BeautifulSoup
from requests import get
from charts_utilities import remove_featured_artists

BASE_URL = 'https://www.officialcharts.com/search/singles/'
CHARTING_THRESHOLD = 40

# Scrape officialcharts.com to find chart information on specified track in specified URL.
def __scrape(url: str) -> list:
    response = get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    table = html.find('tbody', class_='chart-results-content')
    rows = table.find_all('tr')

    results = []

    for row in rows:
        title = row.find('div', class_='title')
        artist = row.find('div', class_='artist')
        position = row.find('span', class_='position')

        if title:
            results.append({
                'title': title.find('a').text.strip(),
                'artist': artist.find('a').text.strip(),
                'position': int(position.text.strip())
            })

    return results

# Get the top chart position for the specified track.
def _get_top_position(track_name: str, artist_name: str) -> int:
    url = BASE_URL + track_name
    results = __scrape(url)
    max = -1

    for result in results:
        if result['artist'].lower().count(artist_name.lower()) and (max < 1 or result['position'] < max) :
            max = result['position']

    return max

# Check whether the specified track has charted.
def has_charted(track_name: str, artist_name: str) -> bool:
    top_pos = _get_top_position(remove_featured_artists(track_name), artist_name)
    return {
        'found': top_pos > 0,
        'charted': top_pos < CHARTING_THRESHOLD
    }