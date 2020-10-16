import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import base64
import pandas as pd

from appModules.dataFetch import dataFetch


countries = {}

with open('countries.txt', 'r') as f:
    for line in f:
        (key, val) = line.split(',')
        countries[key] = val.split('\n')[0]

external_stylesheets = ['main.css', 'layout.css']
logo_location = 'assets/logo.png'
encoded_image = base64.b64encode(open(logo_location, 'rb').read()).decode('ascii')
slider_marks_color = 'black'

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

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
            id='country_dropdown',
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
        size=450,
        updatemode= 'mouseup',
        value=2015
        #tooltip={'placement': 'top', 'always_visible': False}
        #handleLabel={"showCurrentValue": True,"label": "VALUE"},
        )
    ],className='workSection'),
    html.Div([
        html.H2(["country"],id='countryName', className='countryName'),
        html.P(["year"],id='duration', className='duration')
    ],className='results'),
    html.Div([
        html.Div([
            html.P([0],id='numMentions', className='numXmentions'),
            html.P(['total mentions'], className='Xmentions'),
            html.P([0],id='avgscore', className='avgscore'),
            html.P(['average tone'], className='xavgscore')
        ], className='resultStatsLeft'),
        html.Div([
            html.Div([
                html.P([], id='first', className='first'),
                html.P([], id='firstScore', className='firstScore')
            ], className='firstResult'),
            html.Div([
                html.P([], id='second', className='second'),
                html.P([], id='secondScore', className='secondScore')
            ], className='secondResult'),
            html.Div([
                html.P([], id='third', className='third'),
                html.P([], id='thirdScore', className='thirdScore')
            ], className='thirdResult'),
            html.Div([
                html.P([], id='fourth', className='fourth'),
                html.P([], id='fourthScore', className='fourthScore')
            ], className='fourthResult'),
            html.Div([
                html.P([], id='fifth', className='fifth'),
                html.P([], id='fifthScore', className='fifthScore')
            ], className='fifthResult')
        ], className='resultStatsRight')
    ], className='resultStats', id = 'resultStats', style= {'display': 'block'})
], className='mainDiv')

@app.callback(
    Output(component_id='countryName', component_property='children'),
    [Input(component_id='country_dropdown', component_property='value')]
)
def update_output_div(input_value):
    """This function updates the country name on UI for reference

    Args:
        input_value (str): country name as passed from dash dropdown component

    Returns:
        str: name of the country
    """
    return '{}'.format(input_value)

@app.callback(
    Output(component_id='duration', component_property='children'),
    [Input(component_id='dateSlider', component_property='value')]
)
def update_output_div(input_value):
    """This function returns the selected value for the year in Dash Slider

    Args:
        input_value (int): year as filtered and selected in dash slider component

    Returns:
        int: year filter 
    """
    return '{}'.format(input_value)


@app.callback(
    Output(component_id='numMentions', component_property='children'),
    Output(component_id='avgscore', component_property='children'),
    [Input(component_id='dateSlider', component_property='value'),
    Input(component_id='country_dropdown', component_property='value')]
)
def getMentions(dateSlider, country_dropdown):
    """This function prints and displays the total number of mentions and average tone score for a country in a particular year via DB query

    Args:
        dateSlider (int): year for which the query needs to be filtered
        country_dropdown (str): name of the country to filter query for

    Returns:
        dataframe: a dataframe from the callback of dataFetch.py
    """
    result = dataFetch(country_dropdown, dateSlider, 0)
    return result.iloc[0,0], round(result.iloc[0,1],2)


@app.callback(
    Output(component_id='first', component_property='children'),
    Output(component_id='firstScore', component_property='children'),
    Output(component_id='second', component_property='children'),
    Output(component_id='secondScore', component_property='children'),
    Output(component_id='third', component_property='children'),
    Output(component_id='thirdScore', component_property='children'),
    Output(component_id='fourth', component_property='children'),
    Output(component_id='fourthScore', component_property='children'),
    Output(component_id='fifth', component_property='children'),
    Output(component_id='fifthScore', component_property='children'),
    [Input(component_id='dateSlider', component_property='value'),
    Input(component_id='country_dropdown', component_property='value')]
)

def updateArticles(dateSlider, country_dropdown):
    """This function prints and displays the top 5 articles from the query results via DB query

    Args:
        dateSlider (int): year for which the query needs to be filtered
        country_dropdown (str): name of the country to filter query for

    Returns:
        dataframe: a dataframe from the callback of dataFetch.py
    """
    df = dataFetch(country_dropdown, dateSlider, 1)
    return df.iloc[0,0], df.iloc[0,1], df.iloc[1,0], df.iloc[1,1], df.iloc[2,0], df.iloc[2,1], df.iloc[3,0], df.iloc[3,1], df.iloc[4,0], df.iloc[4,1]

if __name__ == '__main__':
    app.run_server(debug=False)
