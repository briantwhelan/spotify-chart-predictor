from bs4 import BeautifulSoup
from requests import get

BASE_URL = 'https://www.officialcharts.com/search/singles/'
CHARTING_THRESHOLD = 40

def scrape(url: str) -> list:
    reponse = get(url)
    html = BeautifulSoup(reponse.content, 'html.parser')

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

def get_top_position(track_name: str, artist_name: str) -> int:
    url = BASE_URL + track_name
    results = scrape(url)
    max = -1

    for result in results:
        if result['artist'].lower() == artist_name.lower() and (max < 1 or result['position'] < max):
            max = result['position']

    return max

def has_charted(track_name: str, artist_name: str) -> bool:
    top_pos = get_top_position(track_name, artist_name)

    if top_pos > 0:
        print(f'Top position: {top_pos}')
        if top_pos < CHARTING_THRESHOLD:
            return True

    return False