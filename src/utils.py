# Plotting script
# Tejas Phaterpekar
# The primary goal of this script is create plot functions that can be imported into my app.py file for implementation into dashboards.
#  Ultimately, the goal is to generalize a class so that it can accept and prep multiple different "clean" datasets. 
#

# Requirements:
# data must be compatible as a dataframe

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
        
        x_scale = alt.Scale(domain = (self.data[xval].min(), self.data[xval].max()))
        y_scale = alt.Scale(domain = (self.data[yval].min(), self.data[yval].max()))

        scatter = alt.Chart(self.data).mark_circle(size=90).encode(
                    alt.X(xval),
                    alt.Y(yval),
                    alt.Color(color + ":N", legend=alt.Legend(orient="left"))
                ).properties(width=300, height=200)

        x_hist = alt.Chart(self.data).mark_bar(opacity = 0.3).encode(
                alt.X(xval, bin=alt.Bin(extent = x_scale.domain), title = ""),
                alt.Y('count()', stack = None), 
                alt.Color(color + ":N")                 
            ).properties(title='{0} distribution'.format(xval),
                            width=300, height=100)

        y_hist = alt.Chart(self.data).mark_bar(opacity = 0.4).encode(
            alt.X('count()', stack = None),
            alt.Y(yval, bin = alt.Bin(extent = y_scale.domain), title = ""),
            alt.Color(color + ":N")
            ).properties(title='{0} distribution'.format(yval),
                            width=100, height=200)

        return (x_hist & (scatter | y_hist)).configure_view(strokeWidth=0)

    def make_heatmap(self):
        '''
        Take in a dataframe and creates a heatmap
        
        Arguments: 
        corr_df (DataFrame) - Dataframe of correlational values
        '''

        corr_df = self.data.corr().round(2).reset_index().melt(id_vars = "index",var_name = "var2", value_name = "corr_val")
        
        base = alt.Chart(corr_df).encode(
            alt.X("index"),
            alt.Y("var2")
        )
        heatmap = base.mark_rect().encode(
            alt.Color("corr_val", scale = alt.Scale(scheme = "viridis"))
        )
        
        text = base.mark_text().encode(
        text = "corr_val"
        )
        return (heatmap + text).properties(height = 500, width = 500)