import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, callback, no_update
from dash.dependencies import Output, Input, State, ALL




# Dash app setup
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

header_style = {
    "backgroundColor": "#1C2337",
    "padding": "10px",
    "color": "white",
    "fontSize": "10px",
    "fontWeight": "bold",
    "fontFamily": "sans-serif",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-between",
    "position": "relative"
}

title_style = {
    "margin-left": "40%",
    "textAlign": "center",
    "fontSize": "20px"
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dcc.Location(id='compare-link', refresh=True),
    html.Div(
        style={
            "backgroundImage": "url('/assets/image.jpg')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "width": "100%",
            "height": "100vh",
            "position": "absolute",
            "top": "59px",
            "left": "0",
            "zIndex": "-1",
        },
    ),
    html.Div(
        [
            html.Div("Price Estimate and Comparison Tool", style=title_style),
            html.Img(src="/assets/logo.png", height="50px", style={"marginRight": "10px", "width": "150px", "height": "40px"})
        ],
        style=header_style
    ),
    dash.page_container,
])


@callback(
    Output('url', 'href'),
    [Input("search-button", 'n_clicks')],
    [State("location-input", 'value'),
    State("service-input", "value")],
)
def update_url(n_clicks, location, service):
    if(n_clicks > 0):
        if(location and service):
            return f'/results?location={location}&service={service}'
        else:
            return '/location'
    return dash.no_update
        

if __name__ == "__main__":
    app.run_server(debug=True)
