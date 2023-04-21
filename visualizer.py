import matplotlib.pyplot as plt
from core.sql import SQLInterface
import numpy as np
from post_process.process import get_bar_chart_data, get_progress_bar_data, get_scatter_plot_data
from post_process.visualize import bar_chart, progress_bar, scatter_plot

if __name__ == "__main__":
    cities_db = SQLInterface('factories_and_urbanism', 'cities')
    environmental_db = SQLInterface('factories_and_urbanism', 'environment')
    air_quality_db = SQLInterface('factories_and_urbanism', 'air_quality')
    
    ## Visualization #1: Plot cities split into 4 categories (>1m, 500k, 250k, <250k) by population
    population_categories = get_bar_chart_data()
    bar_chart(population_categories)
    
    # Visualization #2: Scatter plot of number of factories and landfills vs air quality
    [x, y, landfill_x, landfill_y, factory_x, factory_y] = get_scatter_plot_data()
    scatter_plot(x, y, landfill_x, landfill_y, factory_x, factory_y)

    # Visualization #3: Progress bar 
    [x, y] = get_progress_bar_data(0.7)
    progress_bar(x, y)

    # output number of cities with air quality below 0.7
    cities = cities_db.select()
    air_quality = air_quality_db.select()
    num_cities = len(cities)
    num_cities_below_0_7 = 0
    for city in cities:
        city_air_quality = air_quality_db.select(args=f'WHERE city_id = {str(city["id"])}')
        if len(city_air_quality) > 0:
            if city_air_quality[0]['air_quality'] < 0.7:
                num_cities_below_0_7 += 1

    # output to file
    with open('output.txt', 'w') as f:
        f.write(f'Number of cities with air quality below 0.7 (not good): {num_cities_below_0_7}/{num_cities}')