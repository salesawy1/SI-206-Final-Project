import matplotlib.pyplot as plt
from core.sql import SQLInterface
import numpy as np

def progress_bar(x, y):
    plt.barh(x, y, color='#f3e1ce')
    plt.xlabel('Number of Cities')
    plt.title('Cities with Air Quality Score < 0.7')
    plt.show()
    
def bar_chart(population_categories):
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
    
def scatter_plot(x, y, landfill_x, landfill_y, factory_x, factory_y):
    # plot
    plt.scatter(landfill_x, landfill_y, color='#f3e1ce', marker='o', label='Landfills')
    plt.scatter(factory_x, factory_y, color='#614444', marker='o', label='Factories')
    
    # line of best fit for landfills
    landfill_m, landfill_b = np.polyfit(landfill_x, landfill_y, 1)
    landfill_x = np.array(landfill_x)
    plt.plot(landfill_x, landfill_m * landfill_x + landfill_b, color='#f3e1ce')
        
    # line of best fit for factories
    factory_m, factory_b = np.polyfit(factory_x, factory_y, 1)
    factory_x = np.array(factory_x)
    plt.plot(factory_x, factory_m * factory_x + factory_b, color='#614444')
    
    plt.xlabel('Number of Factories and Landfills')
    plt.ylabel('Air Quality Score')
    plt.title('Number of Factories and Landfills vs Air Quality Score')
    plt.legend()
    plt.show()