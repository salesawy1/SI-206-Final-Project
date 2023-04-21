import requests
from bs4 import BeautifulSoup
from typing import List, TypedDict

class CityData(TypedDict):
    city: str
    state: str
    population: int

def get_cities_list() -> List[CityData]:
    url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')
    cities = []
    for row in rows[1:]:
        cells = row.find_all('td')

        city_data = {
            'id': len(cities),
            'city': cells[0].find('a').text,
            'state': cells[1].find('a').text,
            'population': int(cells[2].text.replace('\n', '').replace(',', '')),
        }

        cities.append(city_data)

    return cities

print(get_cities_list())