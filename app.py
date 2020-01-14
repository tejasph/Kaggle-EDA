import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

heart_df = pd.read_csv("heart.csv")

def make_plot(xval = 'age',
              yval = 'trestbps', 
              data = heart_df):
    # Don't forget to include imports


    # typeDict = {'Displacement':['quantitative','Displacement (mm)'],
    #             'Cylinders':['ordinal', 'Cylinders (#)'],
    #             'Miles_per_Gallon':['quantitative', 'Fuel Efficiency (mpg)'],
    #             'Horsepower':['quantitative', 'Horsepower (hp)']
    #             }

    # Create a plot from the cars dataset


    chart = alt.Chart(data).mark_point(size=90).encode(
                alt.X(xval),
                alt.Y(yval),
                alt.Color("sex:N"),
            ).properties(title='{0} vs. {1}'.format(xval,yval),
                        width=300, height=200)


    return (chart)

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
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id = 'x-axis',
                    options = [{'label':k , 'value': k } for k in heart_df.columns],
                    value = 'thal'

                ), width = 3
            ),
            dbc.Col(
                dcc.Dropdown(
                    id = 'y-axis',
                    options = [{'label':k , 'value': k } for k in heart_df.columns],
                    value = 'target'
                ), width = 3
                
            )
        ])
        
    ],
    fluid=True,
)

container = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Iframe(
                sandbox='allow-scripts',
                id='basic_plot',
                height='300',
                width='400',
                style={'border-width': '0'},
                ################ The magic happens here
                srcDoc = make_plot().to_html()
                ################ The magic happens here
            )
        )
    ])
])

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

footer = dbc.Container([dbc.Row(dbc.Col(html.P('This Dash app was made collaboratively by the DSCI 532 class in 2019/20!'))),
         ])

app.layout = html.Div([jumbotron,
                        container,
                       footer])

@app.callback(
    dash.dependencies.Output('basic_plot', 'srcDoc'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value')])
def update_plot(xaxis_column_name,
                yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,
                             yaxis_column_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)