from core.sql import SQLInterface
import numpy as np

air_quality_db = SQLInterface('factories_and_urbanism', 'air_quality')
cities_db = SQLInterface('factories_and_urbanism', 'cities')
environmental_db = SQLInterface('factories_and_urbanism', 'environment')

# input: none
# output: [x, y, landfill_x, landfill_y, factory_x, factory_y] where x and y are the number of factories and landfills
def get_bar_chart_data():
    cities_db = SQLInterface('factories_and_urbanism', 'cities')
    air_quality_db = SQLInterface('factories_and_urbanism', 'air_quality')
    
    pop_map = {
        '<350k': lambda city: city['population'] < 350000,
        '350k-500k': lambda city: city['population'] >= 500000 and city['population'] < 1000000,
        '500k-1m': lambda city: city['population'] >= 350000 and city['population'] < 500000,
        '>1m':  lambda city: city['population'] >= 1000000
    }
    
    cities = cities_db.select()
    population_categories = { category: { 'cities': [] } for category in pop_map.keys() }
    
    # assign each city to a category
    for city in cities:
        city['population'] = int(city['population'])
        
        for i, category in enumerate(population_categories.keys()):
            if pop_map[category](city):
                population_categories[category]['cities'].append(city)
                break
            
    # add an average air quality score for each category
    for category in population_categories.keys():
        skip = False
        population_categories[category]['avg_air_quality'] = 0
        for city in population_categories[category]['cities']:
            air_quality = air_quality_db.select(args=f'WHERE city_id = {str(city["id"])}')
            if len(air_quality) > 0:
                population_categories[category]['avg_air_quality'] += air_quality[0]['air_quality']
            else:
                skip = True
                continue
        if skip:
            continue
        else:
            population_categories[category]['avg_air_quality'] /= len(population_categories[category]['cities'])
    
    return population_categories

# input: none
# output: [x, y, landfill_x, landfill_y, factory_x, factory_y] where x and y are lists of ints and landfill_x, landfill_y, factory_x, factory_y are lists of ints
def get_scatter_plot_data():
    # get data
    cities = cities_db.select(args='JOIN environment ON cities.id = environment.city_id')
    x = []
    y = []
    landfill_x = []
    landfill_y = []
    factory_x = []
    factory_y = []
    for city in cities:
        air_quality = air_quality_db.select(args=f'WHERE city_id = {str(city["id"])}')
        if len(air_quality) > 0:
            factories = environmental_db.select(args=f'WHERE city_id = {str(city["id"])}')[0]['factories_count']
            landfills = environmental_db.select(args=f'WHERE city_id = {str(city["id"])}')[0]['landfills_count']
            x.append(int(factories) + int(landfills))
            y.append(air_quality[0]['air_quality'])
            landfill_x.append(landfills)
            landfill_y.append(air_quality[0]['air_quality'])
            factory_x.append(factories)
            factory_y.append(air_quality[0]['air_quality'])
            
    return [x, y, landfill_x, landfill_y, factory_x, factory_y]

# input: threshold
# output: [x, y] where x is a list of strings and y is a list of ints
def get_progress_bar_data(threshold):
    cities = cities_db.select()
    air_quality = air_quality_db.select()
    air_quality = [city['air_quality'] for city in air_quality]
    air_quality = np.array(air_quality)
    air_quality = air_quality[air_quality < threshold]
    x = [f'Cities with air quality < {threshold}', f'Cities with air quality >= {threshold}']
    y = [len(air_quality), len(cities) - len(air_quality)]
    return [x, y]