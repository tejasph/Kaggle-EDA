# external libraries
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
server = app.server

colors = {"white": "#ffffff",
          "light_grey": "#d2d7df",
          "box1blue": "#8BBEE8FF ",
          "box2green": "#A8D5BAFF",
          "box3blue": "#8BBEE8FF",
          "box4green": "#A8D5BAFF",
          "black": "#000000",
          "light_purple": "#E3D1FB"
          }

app.layout = html.Div(style={'backgroundColor': colors['white']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['black'], 'border': '1px solid', "padding-left": 5}, children=[
        html.H3('Pollutants Matter BC – Visualization of Particulate Matter Concentrations',
                style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2}),
        html.P('This application tracks weighted monthly averages for pollution data collected from different stations across British Columbia. The measured pollutants, PM2.5 and PM10, refer to atmospheric particulate matter (PM) that have a diameter of less than 2.5 and 10 micrometers, respectively.',
                style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2})
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
