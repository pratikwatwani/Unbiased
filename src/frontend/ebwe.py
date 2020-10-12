import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

import base64

countries = {}
with open('countries.txt', 'r') as f:
    for line in f:
        (key, val) = line.split(',')
        countries[key] = val.split('\n')[0]

external_stylesheets = ['main.css', 'layout.css']
logo_location = 'assets/logo.png'
encoded_image = base64.b64encode(open(logo_location, 'rb').read()).decode('ascii')
slider_marks_color = 'black'
app = dash.Dash('EBWE',external_stylesheets=external_stylesheets)

options = {}
    #Get countries from the data
    # Actor2Geo_FullName == 1
    # Actor2Geo_CountryCode
    # This will get countries, filter out unique


app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), className = 'logo'),
            html.H1("UNBIASED", className = 'title')
        ],className='header'),
        html.Br(),
        html.Div([
            html.H3(["Spatio-Temporal Event Based Wikipedia Activity"], className = 'tagline')
        ],className='subHeader')
    ], className='mainHeader'),
    html.Div([
        html.Div(
            children = [dcc.Dropdown(
            options=[{'label': countries[key], 'value': countries[key]} for key in countries],
            searchable=True, 
            className='country-dropdown',
            id='country-dropdown',
            placeholder="Select a country",
            clearable=True,
            value='Afghanistan'
            ),
        html.Br(),  
        ]),
        daq.Slider(
        min=2015,
        max=2019,
        step=None,
        marks={
            2015: {'label' :'2015', 'style': {'color': '#f50', 'fontFamily':'sans-serif', 'fontWeight':300}},
            2016: {'label' :'2016', 'style': {'color': 'black', 'fontFamily':'sans-serif', 'fontWeight':300}},
            2017: {'label' :'2017', 'style': {'color': 'black', 'fontFamily':'sans-serif', 'fontWeight':300}},
            2018: {'label' :'2018', 'style': {'color': 'black', 'fontFamily':'sans-serif', 'fontWeight':300}},
            2019: {'label' :'2019', 'style': {'color': '#f50', 'fontFamily':'sans-serif', 'fontWeight':300}} 
        },
        className='dateSlider',
        id='dateSlider',
        size=450
        #tooltip={'placement': 'top', 'always_visible': False}
        #handleLabel={"showCurrentValue": True,"label": "VALUE"},
        )        
    ],className='workSection'),
    html.Div([
        html.H2(id='countryName', className='countryName'),
        html.P(id='duration', className='duration')
    ],className='results'),
    html.Div([
        html.Div([], className='resultStatsLeft'),
        html.Div([], className='resultStatsRight')
    ], className='resultStats')
], className='mainDiv')
    
@app.callback(
    Output(component_id='countryName', component_property='children'),
    [Input(component_id='country-dropdown', component_property='value')]
)

def update_output_div(input_value):
    return '{}'.format(input_value)
    return{'display':'block'}

@app.callback(
    Output(component_id='duration', component_property='children'),
    [Input(component_id='dateSlider', component_property='value')]
)

def update_output_div(input_value):
    return 'Activity for the year {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
