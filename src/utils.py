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
        # implement some sort of filter to get categorical columns separate from numerical columns 
        self.features = data.columns

        # User will specify these within the app
        self.numerical_feat = []
        self.categorical_feat = []

    def make_scatter(self, xval = 'age',
              yval = 'trestbps',
              color = "sex"):

        chart = alt.Chart(self.data).mark_point(size=90).encode(
                    alt.X(xval),
                    alt.Y(yval),
                    alt.Color(color + ":N")
                ).properties(title='{0} vs. {1}'.format(xval,yval),
                            width=300, height=200)

        return (chart)