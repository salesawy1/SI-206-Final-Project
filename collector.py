from sql import SQLInterface
from wikipedia_fetcher import get_cities_list
from utils import python_to_sql_types, generate_sql_columns_from_data
from maps import get_location_count
from teleport import get_city_details

LIMIT = 25

if __name__ == '__main__':
    ## STEP 1: Get list of cities from Wikipedia
    cities = get_cities_list() # { id: int, city: string, state: string, population: string }[]
    
    # instantiate sql interface for cities
    cities_column_types = generate_sql_columns_from_data(cities)
    db_cities = SQLInterface('factories_and_urbanism', 'cities', cities_column_types)

    # insert data
    print(f'Inserting {LIMIT} cities into database...')
    cities = db_cities.insert(data=cities, limit=LIMIT, identifier='id')
    print(f'Inserted cities into database.')
    
    ## STEP 2: Get number of harmful environment factors in each city from Google Maps and insert into new table that has city_id as a foreign key
    print(f'Fetching environment factors for {LIMIT} cities...')
    environment_data = []
    env_processed_count = 0
    for city in cities:
        if city['id'] % 5 == 0:
            print(f'Fetched environment factors for {env_processed_count + 1}/{len(cities)} cities.')
        
        # get data
        factories_count = get_location_count('factory', city['city'] + ', ' + city['state'])
        landfills_count = get_location_count('landfill', city['city'] + ', ' + city['state'])
        if factories_count == 0 and landfills_count == 0:
            continue
        
        env = {
            'city_id': city['id'],
            'factories_count': factories_count,
            'landfills_count': landfills_count
        }
        
        environment_data.append(env)
        env_processed_count += 1

    # create/get table
    environment_data_column_types = generate_sql_columns_from_data(environment_data)
    db_environment = SQLInterface('factories_and_urbanism', 'environment', environment_data_column_types)

    # insert into db
    print(f'Fetched environment factors for {env_processed_count} cities. Inserting them now..')
    db_environment.insert(data=environment_data, limit=LIMIT, identifier='city_id')
    print(f'Inserted environment factors into database.')
    
    ## STEP 3: Now that we have the harmfuls, we need to see how they've affected the air quality, so we'll get the air quality data from Teleport and insert it into a new table that has city_id as a foreign key
    print(f'Fetching air quality data for {LIMIT} cities...')
    air_quality_data = []
    air_processed_count = 0
    for city in cities:
        if city['id'] % 5 == 0:
            print(f'Fetched air quality data for {air_processed_count + 1}/{len(cities)} cities.')
        
        # get data
        city_details = get_city_details(city['city'] + ', ' + city['state'], ['air_quality'])
        air_quality = city_details['air_quality']
        if air_quality == 'not_found':
            continue
        
        air = {
            'city_id': city['id'],
            'air_quality': air_quality
        }
        
        air_quality_data.append(air)
        air_processed_count += 1
        
    # create/get table
    air_quality_data_column_types = generate_sql_columns_from_data(air_quality_data)
    db_air_quality = SQLInterface('factories_and_urbanism', 'air_quality', air_quality_data_column_types)
    
    # insert into db
    print(f'Fetched air quality data for {air_processed_count} cities. Inserting them now..')
    db_air_quality.insert(data=air_quality_data, limit=LIMIT, identifier='city_id')
    print(f'Inserted air quality data into database.')