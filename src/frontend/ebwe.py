import dash
import dash_core_components as dcc
import dash_html_components as html
import base64


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
        html.Div([
            html.H3(["Spatio-Temporal Event Based", html.Br(), "Wikipedia Activity"], className = 'tagline')
        ],className='subHeader')
    ], className='mainHeader'),
    html.Div([
        html.Div(
            children = [dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            searchable=True, 
            className='country-dropdown',
            placeholder="Select a country",
            ),
        html.Br(),  
        ]),
        dcc.Slider(
        min=30,
        max=1825,
        step=None,
        marks={
            30: {'label' :'30 Days', 'style': {'color': '#f50', 'fontFamily':'sans-serif', 'fontWeight':300}},
            60: {'label' :'', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            90: {'label' :'', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            180: {'label' :'180 Days', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            365: {'label' :'1 Years', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            730: {'label' :'2 Years', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            1095: {'label' :'3 Years', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            1460: {'label' :'4 Years', 'style': {'color': slider_marks_color, 'fontFamily':'sans-serif', 'fontWeight':300}},
            1825: {'label': '5 Years', 'style': {'color': '#f50', 'fontFamily':'sans-serif'}}
        },
        className='dateSlider',
        tooltip={'placement': 'top', 'always_visible': False}
        )        
    ],className='workSection')
], className='mainDiv')
    
if __name__ == '__main__':
    app.run_server(debug=True)

    marker_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)