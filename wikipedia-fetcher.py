import requests
from bs4 import BeautifulSoup

def get_cities_list():
    url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')
    cities = []
    for row in rows[1:]:
        cells = row.find_all('td')
        city = cells[0].find('a').text + ', ' + cells[1].find('a').text
        cities.append(city)
    return cities

# print(get_cities_list())