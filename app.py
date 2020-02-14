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
# - add histogram plotting function
# - add heatmap of correlations


# Wishlist: graphing options, feature transformation options, feature engineering options?

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

heart_df = pd.read_csv("heart.csv")
Plotter = utils.Plotter(heart_df)

##################
# dcc Components
##################
x_axis_dropdown =    dcc.Dropdown(
                id = 'x-axis',
                options = [{'label':k , 'value': k } for k in Plotter.features],
                value = 'thal'

            )

y_axis_dropdown =    dcc.Dropdown(
                id = 'y-axis',
                options = [{'label':k , 'value': k } for k in Plotter.features],
                value = 'target'
            )
                
color_dropdown = dcc.Dropdown(
    id = 'color', 
    options = [{'label': k, 'value': k } for k in Plotter.features],
    value = 'sex'
)


categorical_vars = dcc.Checklist(
    id = 'categ-select',
    options = [{'label':k , 'value': k } for k in Plotter.features],
    inputStyle={"margin-left": "20px", "margin-right" : "5px"}
)

# once variables are selected, we can disable everything else; or better yet, have the upload and variable selections in the first tab, disable other tabs
variable_manager = html.Div(
    [
        dbc.Button("Typify Variables", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("Select categorical variables; the rest will be considered numerical"),
                dbc.ModalBody(
                    categorical_vars
                ),
                dbc.ModalFooter(
                    dbc.Button("Submit", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            size = "lg",
            centered = True
        ),
    ]
)

jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Img(src='https://qtxasset.com/styles/breakpoint_sm_default_480px_w/s3/fiercebiotech/1555676120/connor-wells-534089-unsplash.jpg/connor-wells-534089-unsplash.jpg?MLzphivqxLKuCKifkgl.3eGf_mETvKfV&itok=ii7r9S1Q', 
                      width='100px'),
                html.H1("Kaggle EDA Heart Disease", className="display-3"),
                html.P(
                    "Add a description of the dashboard",
                    className="lead",
                ),
            ],
            fluid=True,
        ),
        dbc.Row([dbc.Col(html.P("X-Axis")), dbc.Col(html.P("Y-axis"))]),
        dbc.Row([dbc.Col(x_axis_dropdown), dbc.Col(y_axis_dropdown), dbc.Col(color_dropdown)])
        
    ],
    fluid=True
)


card = dbc.Card(
    
    dbc.CardBody(
        [
            html.P("test"),
            html.Iframe(
            sandbox='allow-scripts',
            id='scatter_plot',
            height='300',
            width='400',
            style={'border-width': '2', 'border': '2px solid red', 'backgroundColor': "white"},
            ################ The magic happens here
            srcDoc = Plotter.make_scatter().to_html()
            ################ The magic happens here
        )

        ]
    ),className="card text-white bg-secondary mb-3", style = {"width": "30rem"}
)



#####################
# Tab Layout
#####################

# Data Settings Tab Layout
data_settings_content = html.Div([
    variable_manager
])

# Exploratory Data Analysis Layout
eda_content = html.Div([jumbotron,
                        card])


app.layout = dbc.Tabs(
    [
        dbc.Tab(data_settings_content, label = "Data Settings"),
        dbc.Tab(eda_content, label = "Exploratory Data Analysis", id = "eda-tab")
    ]
)

#####################
# Callbacks
#####################


@app.callback(
    [Output("color","options"),
    Output("x-axis","options")],
    [Input("categ-select", 'value')]
)
def update_var_types(categ_vars):
    
    # If user declares categorical types, then update dropdown options.
    if categ_vars is None:
        return [{'label':k , 'value': k } for k in Plotter.features], [{'label':k , 'value': k } for k in Plotter.features]
    else:
        num_vars = list(set(categ_vars)^set(Plotter.features))
        print(num_vars)
        return [{'label': g, 'value' : g} for g in categ_vars], [{'label': g, 'value' : g} for g in num_vars]

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('scatter_plot', 'srcDoc'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value'),
     Input('color', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name,
                color_var):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = Plotter.make_scatter(xaxis_column_name,
                             yaxis_column_name, 
                             color_var).to_html()
    return updated_plot




if __name__ == '__main__':
    app.run_server(debug=True)

# container = dbc.Container([
#     dbc.Row([
#         dbc.Col(
#             # html.Iframe(
#             #     sandbox='allow-scripts',
#             #     id='basic_plot',
#             #     height='300',
#             #     width='400',
#             #     style={'border-width': '0'},
#             #     ################ The magic happens here
#             #     srcDoc = make_plot().to_html()
#             #     ################ The magic happens here
#             # )
#         )
#     ])
# ])


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

