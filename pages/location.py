import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/location')

layout = html.Div([
    html.Div(
        [
            html.Img(
                id="back-button", 
                n_clicks=0, 
                src="/assets/back.png", 
                style={
                    "width": "30px", 
                    "height": "30px",
                    "position": "fixed", 
                    "top": "20px", 
                    "right": "20px", 
                    "zIndex": "9999",  # Ensures the button appears on top of other elements
                }
            ),    
            html.Div([
                html.H1("Find Hospitals Near Me", style={"textAlign": "left", "color": "#1C2337", "paddingTop": "20px", "fontSize": "24px"}),
                html.P(
                    "Find and compare information about the price and quality of care at over 4,000 Medicare-certified hospitals.",
                    style={"textAlign": "left", "color": "#1C2337", "paddingBottom": "20px", "fontSize": "18px"},
                ),
                html.Div([
                    html.Div([
                        html.Label(
                            "My Location",
                            style={
                                "color": "#1C2337",
                                "textAlign": "left",
                                "fontSize": "18px",
                                "fontWeight": "bold",
                            },
                        ),
                        html.Br(),
                        html.Label("Enter street, ZIP code, city, or state.", style={"textAlign": "left", "color": "black", "fontSize": "16px"}),
                        dcc.Input(id="location-input", type="text", style={"width": "100%", "padding": "10px", "marginTop": "10px", "borderRadius": "10px", "border": "2px solid #ddd"}),
                    ], style={"paddingRight": "5%", "width": "45%", "display": "inline-block"}),

                    html.Div([
                        html.Label(
                            "What service would you like?",
                            style={
                                "color": "black",
                                "textAlign": "left",
                                "fontSize": "18px",
                                "fontWeight": "bold",
                            },
                        ),
                        html.Br(),
                        html.Label("Search by keyword or CPT code", style={"textAlign": "left", "color": "black", "fontSize": "16px"}),
                        dcc.Input(id="service-input", type="text", style={"width": "100%", "padding": "10px", "marginTop": "10px", "borderRadius": "10px", "border": "2px solid #ddd"}),
                    ], style={"paddingLeft": "5%", "width": "45%", "display": "inline-block"}),
                ]),
            ]),
        ],
        style={"paddingBottom": "20px", "textAlign": "left"}
    ),
    html.Div(
        html.Button(id="search-button", n_clicks=0, children="Search", style={"marginTop": "20px", "fontWeight": "bold", "backgroundColor": "#adcae6", "color": "#1C2337", "border": "none", "borderRadius": "5px", "width": "100px"}),
        style={
            "color": "black",
            "fontSize": "24px",
            "textAlign": "center",
            "paddingTop": "20px",
        },
    ),
], style={"padding": "40px", "backgroundSize": "cover", "backgroundColor": "#F8F9FA", "height": "100vh", "display": "flex", "flexDirection": "column", "alignItems": "center"})
