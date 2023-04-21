import matplotlib.pyplot as plt
from core.sql import SQLInterface
import numpy as np

if __name__ == "__main__":
    cities_db = SQLInterface('factories_and_urbanism', 'cities')
    environmental_db = SQLInterface('factories_and_urbanism', 'environment')
    air_quality_db = SQLInterface('factories_and_urbanism', 'air_quality')
    
    ## Visualization #1: Plot cities split into 4 categories (>1m, 500k, 250k, <250k) by population
    # plot map with a key being the key and the value would be af unction that checks if the city is in that category
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
            air_quality = air_quality_db.select(condition=f'city_id = {str(city["id"])}')
            if len(air_quality) > 0:
                population_categories[category]['avg_air_quality'] += air_quality[0]['air_quality']
            else:
                skip = True
                continue
        if skip:
            continue
        else:
            population_categories[category]['avg_air_quality'] /= len(population_categories[category]['cities'])
    
    # plot
    x = np.arange(len(population_categories.keys()))
    height = [population_categories[category]['avg_air_quality'] for category in population_categories.keys()]
    plt.bar(x, height, color='#f3e1ce')
    plt.xticks(x, population_categories.keys())

    # labels
    plt.xlabel('Population Category')
    plt.ylabel('Average Air Quality Score')
    plt.title('Average Air Quality Score by Population Category')

    plt.show()
    
    