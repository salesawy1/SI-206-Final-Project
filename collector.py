from sql import SQLInterface
from wikipedia_fetcher import get_cities_list
from utils import python_to_sql_types, generate_sql_columns_from_data

LIMIT = 25

if __name__ == '__main__':
    cities = get_cities_list() # { id: int, city: string, state: string, population: string }[]
    
    # instantiate sql interface for cities
    cities_column_types = generate_sql_columns_from_data(cities)
    db_cities = SQLInterface('factories_and_urbanism', 'cities', cities_column_types)
    
    # insert data
    db_cities.insert(cities, LIMIT)