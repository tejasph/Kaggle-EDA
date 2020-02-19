import base64
import datetime
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_table

import altair as alt
import vega_datasets
import pandas as pd

from src import utils

#To do:
# - better data read-in functionality
# - disable 2nd tab until variables selected (postpone)
# - add tool tips
# - add a dashtable and variable typification
# - automate default graph variables that are used



# Wishlist: graphing options, feature transformation options, feature engineering options?

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

# Manipulate this to read in your data correctly
heart_df = pd.read_csv("heart.csv")

Plotter = utils.Plotter(heart_df)

##################
# dcc Components
##################
x_axis_dropdown =    dcc.Dropdown(
                id = 'x-axis-num',
                options = [{'label':k , 'value': k } for k in Plotter.numerical_feat],
                value = 'age'

            )

y_axis_dropdown =    dcc.Dropdown(
                id = 'y-axis-num',
                options = [{'label':k , 'value': k } for k in Plotter.numerical_feat],
                value = 'chol'
            )
                
color_dropdown = dcc.Dropdown(
    id = 'color', 
    options = [{'label': k, 'value': k } for k in Plotter.categorical_feat],
    value = 'sex'
)

x_trans = dcc.RadioItems(
    id = 'x-trans',
    options=[
        {'label': 'Unscaled', 'value': 'Unscaled'},
        {'label': 'Natural Log Transformation', 'value': 'log'}
    ],
    value='Unscaled',
    inputStyle={"margin-left": "20px", "margin-right" : "5px"}
)  

y_trans = dcc.RadioItems(
    id = 'y-trans',
    options=[
        {'label': 'Unscaled', 'value': 'Unscaled'},
        {'label': 'Natural Log Transformation', 'value': 'log'}
    ],
    value='Unscaled',
    inputStyle={"margin-left": "20px", "margin-right" : "5px"}
)  

# categorical_vars = dcc.Checklist(
#     id = 'categ-select',
#     options = [{'label':k , 'value': k } for k in Plotter.features],
#     inputStyle={"margin-left": "20px", "margin-right" : "5px"}
# )

# # once variables are selected, we can disable everything else; or better yet, have the upload and variable selections in the first tab, disable other tabs
# variable_manager = html.Div(
#     [
#         dbc.Button("Typify Variables", id="open"),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader("Select categorical variables; the rest will be considered numerical"),
#                 dbc.ModalBody(
#                     categorical_vars
#                 ),
#                 dbc.ModalFooter(
#                     dbc.Button("Submit", id="close", className="ml-auto")
#                 ),
#             ],
#             id="modal",
#             size = "lg",
#             centered = True
#         ),
#     ]
# )
# https://qtxasset.com/styles/breakpoint_sm_default_480px_w/s3/fiercebiotech/1555676120/connor-wells-534089-unsplash.jpg/connor-wells-534089-unsplash.jpg?MLzphivqxLKuCKifkgl.3eGf_mETvKfV&itok=ii7r9S1Q
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                dbc.Row(dbc.Col(html.Img(src='https://cdn.wallpapersafari.com/71/89/cGTxAy.jpg', 
                      width='160px'))),
                dbc.Row(dbc.Col(html.H1("Kaggle EDA Heart Disease", className="display-4"))),
                dbc.Row(dbc.Col(html.P(
                    "Select variables to update the scatterplot and barplot.",
                    className="lead",
                ))),
                dbc.Row([dbc.Col(html.P("X-Axis")), dbc.Col(html.P("Y-Axis")), dbc.Col(html.P("Category"))]),
                dbc.Row([dbc.Col(x_axis_dropdown), dbc.Col(y_axis_dropdown), dbc.Col(color_dropdown)]),
                dbc.Row([dbc.Col(x_trans, width = 4), dbc.Col(y_trans, width = {'size': 4})])               
            ],
            fluid=True,
        ),       
    ],
    fluid=True
)

# Scatterplot
scatterplot = dbc.Card(
    
    dbc.CardBody(
        [
        dbc.Row(dbc.Col(html.H4("Title of the Scatterplot", className="card-title"))),
        dbc.Row(dbc.Col(html.Iframe(
        sandbox='allow-scripts',
        id='scatter-plot',
        height='450',
        width='600',
        style={'border-width': '2', 'border': '2px solid black', 'backgroundColor': "white"},
        ################ The magic happens here
        srcDoc = Plotter.make_scatter().to_html()
        ################ The magic happens here
        ))),
        ]

    ), 
    className="card border-secondary mb-3"
)

# Heatmap
heatmap = dbc.Card(
    
    dbc.CardBody(
        [
        dbc.Row(dbc.Col(html.H4("Title of the Heatmap", className="card-title"))),
        dbc.Row(dbc.Col(html.Iframe(
        sandbox='allow-scripts',
        id='heatmap',
        height='450',
        width='625',
        style={'border-width': '2', 'border': '2px solid black', 'backgroundColor': "white"},
        ################ The magic happens here
        srcDoc = Plotter.make_heatmap().to_html()
        ################ The magic happens here
        ))),
        ]

    ), 
    className="card border-primary mb-3"
)

# BarChart
bar_chart = dbc.Card(
    
    dbc.CardBody(
        [
        dbc.Row(dbc.Col(html.H4("Title of the Bar Chart", className="card-title"))),
        dbc.Row(dbc.Col(html.Iframe(
        sandbox='allow-scripts',
        id='bar-chart',
        height='450',
        width='600',
        style={'border-width': '2', 'border': '2px solid black', 'backgroundColor': "white"},
        ################ The magic happens here
        srcDoc = Plotter.make_bar().to_html()
        ################ The magic happens here
        ))),
        ]

    ), 
    className="card text-white bg-secondary mb-3"
)

#####################
# Layout
#####################



app.layout = dbc.Container([
                dbc.Row(dbc.Col(jumbotron)), 
                dbc.Row([dbc.Col(scatterplot, width = {'size':6}), dbc.Col(bar_chart, width = {"size" : 6})]),
                dbc.Row(dbc.Col(heatmap, width = {'size': 6}), justify = "center")
                ], fluid = True)


#####################
# Callbacks
#####################


# @app.callback(
#     [Output('color','options'),
#     Output('x-axis-num','options'),
#     Output('y-axis-num', 'options')],
#     [Input('categ-select', 'value')]
# )
# def update_var_types(categ_vars):
#     all_vars = [{'label':k , 'value': k } for k in Plotter.features]
#     # If user declares categorical types, then update dropdown options.
#     if categ_vars is None:
#         return all_vars, all_vars, all_vars
#     else:
#         num_vars = [{'label': g, 'value' : g} for g in list(set(categ_vars)^set(Plotter.features))]
#         return [{'label': g, 'value' : g} for g in categ_vars], num_vars, num_vars

# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
    
#     if n1 or n2:
#         return not is_open
#     return is_open

@app.callback(
    Output('scatter-plot', 'srcDoc'),
    [Input('x-axis-num', 'value'),
     Input('y-axis-num', 'value'),
     Input('color', 'value'), 
     Input('x-trans', 'value'),
     Input('y-trans', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name,
                color_var, 
                x_trans,
                y_trans):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = Plotter.make_scatter(xaxis_column_name,
                             yaxis_column_name, 
                             color_var, x_trans, y_trans).to_html()
    return updated_plot

# @app.callback(
#     Output('scatter-plot', 'srcDoc'),
#     [Input('x-trans', 'value')]
# )
# def transform_plot(x_trans):
#     updated

@app.callback(
    Output('bar-chart', 'srcDoc'),
    [Input('color', 'value')])
def update_bar(category):
    updated_plot = Plotter.make_bar(category).to_html()
    
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True)



# content = dbc.Container([
#     dbc.Row(
#                 [
#                     dbc.Col(

#                         dcc.Dropdown(
#                             id='dd-chart-x',
#                             options=[
#                                 {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
#                                 {'label': 'Cylinders', 'value': 'Cylinders'},
#                                 {'label': 'Displacement', 'value': 'Displacement'},
#                                 {'label': 'Horsepower', 'value': 'Horsepower'}
#                             ],
#                             value='Horsepower',
#                             # style=dict(width='45%',
#                             #         verticalAlign="middle")
#                             ), 
#                             width= {'size':2, 'offset': 10}
#                             ),
#                     dbc.Col(        
#                         dcc.Dropdown(
#                         id='dd-chart-y',
#                         options=[
#                             {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
#                             {'label': 'Cylinders', 'value': 'Cylinders'},
#                             {'label': 'Displacement', 'value': 'Displacement'},
#                             {'label': 'Horsepower', 'value': 'Horsepower'}
#                         ],
#                         value='Displacement'
#                         ), width=2
#                     ),
#                     dbc.Col(
#                     html.Iframe(
#                         sandbox='allow-scripts',
#                         id='plot',
#                         height='560',
#                         width='700',
#                         style={'border-width': '0'},
#                         ################ The magic happens here
#                         srcDoc=make_plot().to_html()
#                         ################ The magic happens here
#                         ),width='6'),
#                 ]
#             )
#     ]
# )

