import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import vega_datasets
import pandas as pd

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

from src import utils

#To do:
# - better data read-in functionality
# - disable 2nd tab until variables selected (postpone)
# - add tool tips
# - add a dashtable and variable typification
# - automate default graph variables that are used



# Wishlist: graphing options, feature transformation options, feature engineering options?



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.config['suppress_callback_exceptions'] = True


app.title = 'Heart Disease EDA'

# Manipulate this to read in your data correctly
heart_df = pd.read_csv("heart.csv")

Plotter = utils.Plotter(heart_df)

##################
# dcc Components
##################
x_axis_dropdown =    dcc.Dropdown(
                id = 'x-axis-num',
                options = [{'label':k , 'value': str(k) } for k in Plotter.numerical_feat],
                value = 'age'

            )

y_axis_dropdown =    dcc.Dropdown(
                id = 'y-axis-num',
                options = [{'label':k , 'value': str(k) } for k in Plotter.numerical_feat],
                value = 'chol'
            )
                
color_dropdown = dcc.Dropdown(
    id = 'color', 
    options = [{'label': k, 'value': str(k) } for k in Plotter.categorical_feat],
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
# scatterplot = dbc.Card(
    
#     dbc.CardBody(
#         [
#         dbc.Row(dbc.Col(html.H4("Title of the Scatterplot", className="card-title", id = 'scatter-title'))),
#         dbc.Row(dbc.Col(html.Iframe(
#         sandbox='allow-scripts',
#         id='scatter-plot',
#         height='450',
#         width='600',
#         style={'border-width': '2', 'border': '2px solid black', 'backgroundColor': "white"},
#         ################ The magic happens here
#         srcDoc = Plotter.make_scatter().to_html()
#         ################ The magic happens here
#         ))),
#         ]

#     ), 
#     className="card border-primary mb-3"
# )

# Heatmap
heatmap = dbc.Card(
    
    dbc.CardBody(
        [
        dbc.Row(dbc.Col(html.H4("Pearson Correlational Heatmap", className="card-title"))),
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
        dbc.Row(dbc.Col(html.H4("Class Imbalance", className="card-title", id = 'bar-title'))),
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
    className="card border-primary mb-3"
)

var_list = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Variable Codebook"),
                dbc.ListGroupItemText(
                    [
                        dbc.Row(html.P("age -- age in years")),
                        dbc.Row(html.P("sex -- (1 = male; 0 = female)")),
                        dbc.Row(html.P("cp -- chest pain type (0 - Typical Angina (Heart related), 1 - Atypical Angina (Non-heart related), 2 - Non-Anginal pain (Non-heart related), 3 - Asymptomatic (No disease)")),
                        dbc.Row(html.P("trestbps -- resting blood pressure (in mm Hg on admission to the hospital)")),
                        dbc.Row(html.P("chol -- serum cholestoral in mg/dl (health levels are < 200mg/dl)")),
                        dbc.Row(html.P("fbs -- (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)")),
                        dbc.Row(html.P("restecg -- resting electrocardiographic results ( 0 = normal, 1 = ST-T wave abnormality, 2= probable or definite left ventricular hypertrophy by Estes' criteria )")),
                        dbc.Row(html.P("thalach -- maximum heart rate achieved")),
                        dbc.Row(html.P("exang -- exercise induced angina (1 = yes; 0 = no)")),
                        dbc.Row(html.P("oldpeak -- ST depression induced by exercise relative to rest")),
                        dbc.Row(html.P("slope -- the slope of the peak exercise ST segment (1 = upsloping, 2 = flat, 3 = downsloping)")),
                        dbc.Row(html.P("ca -- number of major vessels (0-3) colored by flourosopy")),
                        dbc.Row(html.P("thal -- (1 = normal; 2 = fixed defect; 3 = reversable defect)")),
                        dbc.Row(html.P("target -- (1 -heart problem or 0 - no heart problem)" ))
                    ]        
                ),
            ]
        ),
    ]
)

#####################
# Layout
#####################



app.layout = dbc.Container([
                dbc.Row(dbc.Col(jumbotron)),
                dbc.Row([dbc.Col(bar_chart, width = {'size':6})]),
                dbc.Row([dbc.Col(var_list), dbc.Col(heatmap, width = {'size': 6})], justify = "center")
                ], fluid = True)

#                dbc.Row([dbc.Col(scatterplot, width = {'size':6}), dbc.Col(bar_chart, width = {"size" : 6})]),
#               dbc.Row([dbc.Col(var_list), dbc.Col(heatmap, width = {'size': 6})], justify = "center")


#####################
# Callbacks
#####################


# @app.callback(
#     [Output('scatter-plot', 'srcDoc'),
#     Output('scatter-title','children')],
#     [Input('x-axis-num', 'value'),
#      Input('y-axis-num', 'value'),
#      Input('color', 'value'), 
#      Input('x-trans', 'value'),
#      Input('y-trans', 'value')])
# def update_plot(xaxis_column_name,
#                 yaxis_column_name,
#                 color_var, 
#                 x_trans,
#                 y_trans):
#     '''
#     Takes in an xaxis_column_name and calls make_plot to update our Altair figure
#     '''
#     updated_plot = Plotter.make_scatter(xaxis_column_name,
#                              yaxis_column_name, 
#                              color_var, x_trans, y_trans).to_html()
#     return updated_plot, f"{xaxis_column_name} vs {yaxis_column_name}"


# @app.callback(
#     [Output('bar-chart', 'srcDoc'),
#     Output('bar-title', 'children')],
#     [Input('color', 'value')])
# def update_bar(category):
#     updated_plot = Plotter.make_bar(category).to_html()
    
#     return updated_plot, f"Class count for {category}"


if __name__ == '__main__':
    app.run_server(debug=True)




