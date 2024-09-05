import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

welcome_page_style = {
    "backgroundColor": "rgba(255, 255, 255, 0.3)",  # Adjust transparency here
    "padding": "20px",
    "borderRadius": "10px",
    "textAlign": "left",
    "margin": "auto",
    "display": "block",
    "top": "20%",
    "right": "5%",
    "height": "70vh",
    "width": "18%",
    "position": "fixed",
    "backdropFilter": "blur(15px)",
    "color": "black",
    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",  # Optional: to add some shadow effect
}

layout = html.Div([
    html.Div(
        [
            html.Div(
                [
                    html.Br(),
                    html.P(
                        "Patient Estimates",
                        style={"fontSize": "24px", "color": "black"},
                    ),
                    html.Br(),
                    html.P(
                        "Disclaimer\nI acknowledge that this is just an estimate of what I would pay and does not represent a guarantee. "
                        "The actual price I pay may be higher or lower than this estimate.",
                        style={"color": "black"},
                    ),
                    html.Br(),
                    dcc.Link(
                        html.Button(
                            "Accept and continue", id="accept-button", n_clicks=0, style={"backgroundColor": "#C7D5FF", "borderRadius": "10px"}
                        ),
                        href="/location"
                    )
                ],
                style=welcome_page_style,
            ),
        ],
        style={
            "position": "relative",
            "zIndex": "1",
            "textAlign": "center",
            "marginTop": "200px",
        },
    ),
])
