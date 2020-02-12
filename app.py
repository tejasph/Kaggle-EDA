import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import altair as alt
import vega_datasets
import pandas as pd
from src import utils

#To do:
# - add new graph types
# - get a nice layout going, using DBC cards or other boostrap componenets
# - add user upload of their own data option

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

# dcc Components



x_axis =    dcc.Dropdown(
                id = 'x-axis',
                options = [{'label':k , 'value': k } for k in Plotter.features],
                value = 'thal'

            )

y_axis =    dbc.Col(
                dcc.Dropdown(
                    id = 'y-axis',
                    options = [{'label':k , 'value': k } for k in Plotter.features],
                    value = 'target'
                )
                
            )

categorical_vars = dcc.Checklist(
    id = 'categorical selection',
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
        dbc.Row([dbc.Col(x_axis), dbc.Col(y_axis)])
        
    ],
    fluid=True
)

container = dbc.Container([
    dbc.Row([
        dbc.Col(
            # html.Iframe(
            #     sandbox='allow-scripts',
            #     id='basic_plot',
            #     height='300',
            #     width='400',
            #     style={'border-width': '0'},
            #     ################ The magic happens here
            #     srcDoc = make_plot().to_html()
            #     ################ The magic happens here
            # )
        )
    ])
])

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


app.layout = html.Div([variable_manager,
                        jumbotron,
                        container,
                        card])


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
     Input('y-axis', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = Plotter.make_scatter(xaxis_column_name,
                             yaxis_column_name).to_html()
    return updated_plot




if __name__ == '__main__':
    app.run_server(debug=True)



# logo = dbc.Row(dbc.Col(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
#                       width='15%'), width=4))

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

