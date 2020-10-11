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
            html.H1("UNBIASED")
        ], className='leftpane')
], className='mainDiv')
if __name__ == '__main__':
    app.run_server(debug=True)

    marker_style = dict(color='#444', fontFamily='sans-serif', fontWeight=300)