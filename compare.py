# import dash
# from dash import dcc, html, callback, Input, Output, ALL, State
# import dash_bootstrap_components as dbc
# from geopy.distance import geodesic
# import pgeocode
# import pandas as pd
# import json
# from urllib.parse import quote, unquote


# dash.register_page(__name__, path='/compare')

# layout = html.Div([
#     dcc.Location(id='compare-url', refresh=True),
#     html.Div([
#         html.Div(id = 'compare-content', style = {'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'}),
#     ], 
#    )
# ], style = {"backgroundSize": "cover", 'padding': "20px", "backgroundColor": "white", 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)', 
#              'height': '600px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
# )

# def display_star_rating(rating):
#     full_stars = int(rating)  # Number of full stars
#     half_star = rating - full_stars  # Check for half star
#     empty_stars = 5 - full_stars - (1 if half_star > 0 else 0)  # Remaining empty stars

#     star_html = [
        
#     ]

#     # Full stars
#     star_html.extend([html.Span('★', style={"color": "#FDDA0D", "fontSize": "24px", "marginRight": "2px"}) for _ in range(full_stars)])

#     # Half star (if any)
#     if half_star > 0:

#         star_html.append(html.Span('★', style={
#             "color": "#FDDA0D",
#             "fontSize": "24px",
#             "marginRight": "2px",
#             "position": "relative",
#             "display": "inline-block",
#             "width": "12px",  # Half width
#             "overflow": "hidden",
#             "left": "-1px",  # Move left to overlap
#             'top':'8.5px'
#         }))

#     # Empty stars
#     # star_html.extend([html.Span('★', style={"color": "gray", "fontSize": "24px", "marginRight": "2px"}) for _ in range(empty_stars)])

#     return html.Div(star_html, style={"textAlign": "center"})




# @callback(
#     Output('compare-content', 'children'),
#     Input('compare-url', 'search'),
# )
# def display_compare_data(search):
#     params = search.lstrip('?')
#     data_params = dict(params.split('=') for params in params.split('&')).get('data', '')
    
#     if data_params:
#         try:
#             # Decode and parse the data
#             json_data = unquote(data_params)
#             hospital_data = json.loads(json_data)
#             print('hospital_data', hospital_data)
#             table_header = [
#                 html.Thead(html.Tr(
#                     [
#                         html.Th("Overview", style={"textAlign": "left", "padding": "12px", "fontSize": "20px", "fontWeight": "bold", "borderBottom": "2px inset #adcae6", "color": "#000080", "border": "none"}),
#                         *[
#                             html.Th(h.get('Hospital Name', 'Unknown'), style={"textAlign": "center", "padding": "12px", "fontSize": "18px", "fontWeight": "bold", "borderBottom": "2px inset #adcae6", "color": "#000080", "border": "none"})
#                             for h in hospital_data
#                         ]
#                     ]
#                 ))
#             ]
    
#             table_rows = []
#             attrubute_labels = {
#                 'Estimate Payment': 'Estimate Payment',
#                 'Distance': 'Distance',
#                 'Overall Star Rating': 'Overall Star Rating',
#                 'Patient Survey Rating': 'Patient Survey Rating',

#             }


#             for attribute, label in attrubute_labels.items():
#                 row = [html.Td(label, style={"padding": "12px", "fontWeight": "bold", "color": "#000080", "border": "1px solid #adcae6"})]
#                 for hospital in hospital_data:
#                     value = hospital.get(attribute, 'N/A')
#                     print('value', value)
#                     if attribute == 'Estimate Payment':
#                         try:
#                             hospital_fees = float(hospital.get('Hosptial Fees', 0))
#                             physican_fees = float(hospital.get('Physican Fees', 0))
#                             value = f'${hospital_fees + physican_fees: ,.1f}' if hospital_fees > 0 or physican_fees > 0 else 'N/A'
#                             value_style =  {"padding": "12px", "border": "1px solid #adcae6", "color": "green", "fontWeight": "bold"}
#                         except(ValueError, TypeError):
#                             value = 'N/A' 
#                             value_style = {"padding": "12px", "border": "1px solid #adcae6"}
#                     elif attribute == 'Distance':
#                         try:
#                             value = f'{float(value):.1f} Miles' if value not in ['N/A',''] else 'N/A'
#                         except(ValueError, TypeError):
#                             value = 'N/A' 
#                         value_style = {"padding": "12px", "border": "1px solid #adcae6", "fontWeight": "bold", "color":"#000080"}

#                     elif attribute in ['Overall Star Rating', 'Patient Survey Rating']:
#                         try:
#                             value = float(value)
#                             value = display_star_rating(value) 
#                             value_style = {"padding": "12px", "border": "1px solid #adcae6"}
#                         except(ValueError, TypeError):
#                             value = 'N/A'
#                             value_style = {"padding": "12px", "border": "1px solid #adcae6", "fontWeight": "bold", "color":"#000080"} 
#                     else:
#                         value_style = {"padding": "12px", "border": "1px solid #adcae6", "fontWeight": "bold", "color":"#000080"} 
#                     row.append(html.Td(value, style = value_style))
#                     table_rows.append(html.Tr(row, style={"backgroundColor": "#f9f9f9", "borderBottom": "1px solid #adcae6", "transition": "background-color 0.3s"}))
#                 table_body = [html.Tbody(table_rows)]
#                 return html.Div(html.Table(table_header+table_body,   style={"width": "100%", "border": "none", "borderCollapse": "separate", "borderSpacing": "0 10px", "backgroundColor": "white", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "overflow": "hidden", "padding": '20px'}),
#                     style={"backgroundColor": "#f0f8ff", "padding": "20px", "borderRadius": "15px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"})


#         except(json.JSONDecodeError, TypeError) as e:
#             return html.Div (f'Error Decoding Data{str(e)}', style={"color": "red", "fontWeight": "bold", "padding": "20px", "backgroundColor": "#ffe6e6", "borderRadius": "10px"})

#     return html.Div('No Data to Compare', style={"color": "#0044cc", "fontWeight": "bold", "padding": "20px", "backgroundColor": "#e6f0ff", "borderRadius": "10px"})


from dash import dcc, html, Input, Output, callback
import dash
import json
from urllib.parse import unquote


dash.register_page(__name__, path='/compare')
# Define the layout of the compare page
layout = html.Div(
    [
        dcc.Location(id='comp-url', refresh=True),  # To capture URL parameters
        html.Div(
            [
                html.Div(id='compare-content',
                         style={"backgroundColor": "white", "padding": "20px", "borderRadius": "5px", "backdropFilter": "blur(15px)",})
            ]
        ),
    ], style={"padding": "40px", "backgroundSize": "cover", "backgroundColor": "white", "borderRadius": "10px", "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)",
              "height": "635px", "display": "flex", "alignItems": "center", "justifyContent": "center"}
)

def display_star_rating(rating):
    full_stars = int(rating)  # Number of full stars
    half_star = rating - full_stars  # Check for half star
    empty_stars = 5 - full_stars - (1 if half_star > 0 else 0)  # Remaining empty stars

    star_html = [

    ]

    # Full stars
    star_html.extend([html.Span('★', style={"color": "#FDDA0D", "fontSize": "24px", "marginRight": "2px"}) for _ in range(full_stars)])

    # Half star (if any)
    if half_star > 0:

        star_html.append(html.Span('★', style={
            "color": "#FDDA0D",
            "fontSize": "24px",
            "marginRight": "2px",
            "position": "relative",
            "display": "inline-block",
            "width": "12px",  # Half width
            "overflow": "hidden",
            "left": "-1px",  # Move left to overlap
            'top':'8.5px'
        }))

    # Empty stars
    # star_html.extend([html.Span('★', style={"color": "gray", "fontSize": "24px", "marginRight": "2px"}) for _ in range(empty_stars)])

    return html.Div(star_html, style={"textAlign": "center"})


@callback(
    Output('compare-content', 'children'),
    [Input('comp-url', 'search')]
)
def display_compare_data(search):
    # Extract data from URL parameters
    params = search.lstrip('?')
    data_param = dict(param.split('=') for param in params.split('&')).get('data', '')
    print('data_param',data_param)
    if data_param:
        try:
            # Decode and parse the data
            json_data = unquote(data_param)
            hospital_data = json.loads(json_data)
            print('hospital_data',hospital_data)
            table_header = [
                html.Thead(html.Tr(
                    [
                        html.Th("Overview", style={"textAlign": "left", "padding": "12px", "fontSize": "20px", "fontWeight": "bold", "borderBottom": "2px inset #adcae6", "color": "#000080", "border": "none"}),
                        *[
                            html.Th(h.get('Hospital Name', 'Unknown'), style={"textAlign": "center", "padding": "12px", "fontSize": "18px", "fontWeight": "bold", "borderBottom": "2px inset #adcae6", "color": "#000080", "border": "none"})
                            for h in hospital_data
                        ]
                    ]
                ))
            ]

            table_rows = []
            attribute_labels = {
                'Estimated Payment': 'Estimated Payment',  # New attribute for the sum
                'Distance': 'Distance',
                'Overall Star Rating': 'Overall Star Rating',
                'Patient Survey Rating': 'Patient Survey Rating',
                'Hospital Type': 'Hospital Type',  # Added row for Hospital Type
                'Provides Emergency Services?': 'Provides Emergency Services?'  # Added row for Emergency Services
            }

            for attribute, label in attribute_labels.items():
                row = [html.Td(label, style={"padding": "12px", "fontWeight": "bold", "color": "#000080", "border": "1px solid #adcae6"})]
                for hospital in hospital_data:
                    value = hospital.get(attribute, 'N/A')
                    print('value,',value)

                    if attribute == "Estimated Payment":
                        try:
                            hospital_fees = float(hospital.get("Hospital Fees", 0))
                            physician_fees = float(hospital.get("Physician Fees", 0))
                            value = f"${hospital_fees + physician_fees:,.1f}" if hospital_fees > 0 or physician_fees > 0 else 'N/A'
                            value_style = {"padding": "12px", "border": "1px solid #adcae6", "color": "green", "fontWeight": "bold"}
                        except (ValueError, TypeError):
                            value = 'N/A'
                            value_style = {"padding": "12px", "border": "1px solid #adcae6"}
                    elif attribute == "Distance":
                        try:
                            value = f"{float(value):.1f} miles" if value not in ['N/A', ''] else 'N/A'
                            # value_style = {"padding": "12px", "border": "1px solid #adcae6",
                            #                "fontWeight": "bold"}
                        except (ValueError, TypeError):
                            value = 'N/A'
                        value_style = {"padding": "12px", "border": "1px solid #adcae6", "fontWeight": "bold", "color":"#000080"}
                    elif attribute in ["Overall Star Rating", "Patient Survey Rating"]:
                        try:
                            value = float(value)
                            star_rating = display_star_rating(value)
                            value = star_rating
                            value_style = {"padding": "12px", "border": "1px solid #adcae6"}
                        except (ValueError, TypeError):
                            value = 'N/A'
                            value_style = {"padding": "12px", "border": "1px solid #adcae6"}
                    elif attribute in ["Hospital Type", "Provides Emergency Services?"]:
                        
                        value_style = {"padding": "12px", "border": "1px solid #adcae6", "fontWeight": "bold", "color": "#000080"}
                    else:
                        value_style = {"padding": "12px", "border": "1px solid #adcae6"}

                    row.append(html.Td(value, style=value_style))
                table_rows.append(html.Tr(row, style={"backgroundColor": "#f9f9f9", "borderBottom": "1px solid #adcae6", "transition": "background-color 0.3s"}))

            table_body = [html.Tbody(table_rows)]

            return html.Div(
                html.Table(table_header + table_body,
                           style={"width": "100%", "border": "none", "borderCollapse": "separate", "borderSpacing": "0 10px", "backgroundColor": "white", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "overflow": "hidden", "padding": '20px'}),
                style={"backgroundColor": "#f0f8ff", "padding": "20px", "borderRadius": "15px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"}
            )
        except (json.JSONDecodeError, TypeError) as e:
            return html.Div(f'Error decoding data: {str(e)}', style={"color": "red", "fontWeight": "bold", "padding": "20px", "backgroundColor": "#ffe6e6", "borderRadius": "10px"})

    return html.Div('No data to compare', style={"color": "#0044cc", "fontWeight": "bold", "padding": "20px", "backgroundColor": "#e6f0ff", "borderRadius": "10px"})
 