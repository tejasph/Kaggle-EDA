# Plotting script
# Tejas Phaterpekar
# The primary goal of this script is create plot functions that can be imported into my app.py file for implementation into dashboards.
#  Ultimately, the goal is to generalize a class so that it can accept and prep multiple different "clean" datasets. 
#

import pandas as pd
import altair as alt

class Plotter:
    def __init__(self, data): 
        self.data = data
        self.features = data.columns

    def make_scatter(self, xval = 'age',
              yval = 'trestbps'):
    # Don't forget to include imports


    # typeDict = {'Displacement':['quantitative','Displacement (mm)'],
    #             'Cylinders':['ordinal', 'Cylinders (#)'],
    #             'Miles_per_Gallon':['quantitative', 'Fuel Efficiency (mpg)'],
    #             'Horsepower':['quantitative', 'Horsepower (hp)']
    #             }

    # Create a plot from the cars dataset


        chart = alt.Chart(self.data).mark_point(size=90).encode(
                    alt.X(xval),
                    alt.Y(yval),
                    alt.Color("sex:N"),
                ).properties(title='{0} vs. {1}'.format(xval,yval),
                            width=300, height=200)


        return (chart)