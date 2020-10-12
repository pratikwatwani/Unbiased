import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#import dash_bootstrap_components as dbc
import base64
import psycopg2



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
        html.Div([
            html.P(id='numMentions', className='numXmentions'),
            html.P(['total mentions'], className='Xmentions')
        ], className='resultStatsLeft'),
        html.Div([], className='resultStatsRight')
    ], className='resultStats', id = 'resultStats', style= {'display': 'block'})
], className='mainDiv')
    
@app.callback(
    Output(component_id='countryName', component_property='children'),
    [Input(component_id='country_dropdown', component_property='value')]
)

def update_output_div(input_value):
    return '{}'.format(input_value)
    return{'display':'block'}

@app.callback(
    Output(component_id='duration', component_property='children'),
    [Input(component_id='dateSlider', component_property='value')]
)

def update_output_div(input_value):
    return '{}'.format(input_value)


@app.callback(
    Output(component_id='numMentions', component_property='children'),
    [Input(component_id='dateSlider', component_property='value'), Input(component_id='country_dropdown', component_property='value')]
)

def getMentions(dateSlider, country_dropdown):

    conn = psycopg2.connect(
    dbname='ebwe',
    user="admin",
    password="admin",
    host="ec2-54-158-246-201.compute-1.amazonaws.com",
    port='5321'
    )

    cur = conn.cursor(name = 'fetch_large_result')
    """x = cur.execute('select count(*) from mentions;')"""
    
    cur.execute("""select sum(nummentions) from geographies k inner join events g 
            on k.globaleventid = g.globaleventid where k.actor1name = '{0}' or k.actor1geo_fullname = '{0}' 
            or k.actor2name = '{0}' or k.actor2geo_fullname= '{0}' or k.actiongeo_fullname= '{0}' and 
            extract(year from dateadded)='{1}';
            """.format(country_dropdown.lower(), dateSlider))
    rows=cur.fetchall()
    result = [t[0] for t in rows]
  
    return result

if __name__ == '__main__':
    app.run_server(debug=True)
