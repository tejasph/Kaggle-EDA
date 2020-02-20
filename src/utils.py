# Plotting script
# Tejas Phaterpekar
# The primary goal of this script is create plot functions that can be imported into my app.py file for implementation into dashboards.
#  Ultimately, the goal is to generalize a class so that it can accept and prep multiple different "clean" datasets. 
#

# Requirements:
# data must be compatible as a dataframe

import pandas as pd
import altair as alt
import numpy as np

class Plotter:
    def __init__(self, data): 
        self.data = data
        # implement some sort of filter to get categorical columns separate from numerical columns 
        self.features = data.columns

        # User will specify these within the app
        self.numerical_feat = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
        self.categorical_feat = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal', 'target']

        self.x_trans = None

    def make_scatter(self, xval = 'age',yval = 'trestbps', color = "sex", x_transform = None, y_transform = None):
        '''
        '''

        df = self.data.copy(deep = True)

        if x_transform == "log":
            df[xval] = np.log(df[xval])

        if y_transform == "log":
            df[yval] = np.log(df[yval])
      
        x_scale = alt.Scale(domain = (df[xval].min(), df[xval].max()))
        y_scale = alt.Scale(domain = (df[yval].min(), df[yval].max()))

        scatter = alt.Chart(df).mark_circle(size=90, opacity = 0.3).encode(
                    alt.X(xval, scale = x_scale),
                    alt.Y(yval, scale = y_scale),
                    alt.Color(color + ":N", scale=alt.Scale(scheme='tableau10'), legend=alt.Legend(orient="left"))
                ).properties(width=300, height=200)

        x_hist = alt.Chart(df).mark_bar(opacity = 0.3).encode(
                alt.X(xval, bin=alt.Bin(extent = x_scale.domain), title = ""),
                alt.Y('count()', stack = None), 
                alt.Color(color + ":N")                 
            ).properties(title='{0} distribution'.format(xval),
                            width=300, height=100)

        y_hist = alt.Chart(df).mark_bar(opacity = 0.4).encode(
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
            alt.X("index", title = ""),
            alt.Y("var2", title = "")
        )
        heatmap = base.mark_rect().encode(
            alt.Color("corr_val", scale = alt.Scale(scheme = "lighttealblue"), title = "Pearson Corr.")
        )
        
        text = base.mark_text().encode(
        text = "corr_val"
        )
        return (heatmap).properties(height = 350, width = 430)

    def make_bar(self, x_val = 'sex'):

        bar_chart = alt.Chart(self.data).mark_bar().encode(
            alt.X(x_val + ":N"),
            alt.Y('count()'),
        ).properties(height = 375, width = 500)

        return bar_chart