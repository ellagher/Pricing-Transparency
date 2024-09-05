# import dash
# from dash import dcc, html, callback, Input, Output, ALL, State
# import dash_bootstrap_components as dbc
# from geopy.distance import geodesic
# import pgeocode
# import pandas as pd
# import json
# from urllib.parse import quote, unquote
# import urllib.parse

# dash.register_page(__name__, path='/results')

# layout = html.Div([
#     #dcc.Location(id='url', refresh=True),
#     dcc.Location( id = 'compare-link', href = '/compare', refresh = False),
#     dcc.Store(id = 'compare-store', data = [], storage_type = 'memory'),
#     dcc.Location(id = 'redirect', refresh = True),
#     html.Div(id='results-container', style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center'})
# ])

# def get_hospital_data():
#     data = pd.read_csv(r"C:\Users\emgherghescu\OneDrive - Carilion\Documents\my_dash_app\data\PricingTransparency_2.csv")
#     data = data.rename(columns=lambda x: x.strip())
#     data['Zip'] = data['Zip'].astype(str)
#     data['CPT'] = data['CPT'].astype(str)
#     return data

# def get_lat_lon(zip_code, cache):
#     geocoder = pgeocode.Nominatim('us')
#     if zip_code in cache:
#         return cache[zip_code]
#     location = geocoder.query_postal_code(zip_code)
#     if location.latitude and location.longitude:
#         coords = (location.latitude, location.longitude)
#     else:
#         coords = (None, None)
#     cache[zip_code] = coords
#     return coords

# def get_nearby_hospitals(hospital_data, user_zip, service_code):
#     cache = {}
#     user_lat, user_lon = get_lat_lon(user_zip, cache)
#     if user_lat is None or user_lon is None:
#         raise ValueError("Invalid Zipcode")
#     user_coords = (user_lat, user_lon)
#     unique_zip_codes = hospital_data['Zip'].unique()

#     zip_coords = {zip_code: get_lat_lon(zip_code, cache) for zip_code in unique_zip_codes}
#     hospital_data['Latitude'] = hospital_data['Zip'].map(lambda z: zip_coords[z][0])
#     hospital_data['Longitude'] = hospital_data['Zip'].map(lambda z: zip_coords[z][1])
#     hospital_data['CPT'] = hospital_data['CPT'].astype(str).str.strip()
#     hospital_data['Procedure Name'] = hospital_data['Procedure Name'].astype(str).str.strip()
    
#     if service_code:
#         service_code = urllib.parse.unquote(service_code).strip()

#     if service_code:
#         service_hospitals = hospital_data[hospital_data['CPT'] == str(service_code)]
#         if service_hospitals.empty:
#             raise ValueError("Invalid CPT")
    
#     def calculate_distance(row):
#         hospital_coords = (row['Latitude'], row['Longitude'])
#         return geodesic(user_coords, hospital_coords).miles   

#     service_hospitals['Distance'] = service_hospitals.apply(calculate_distance, axis=1)
#     nearby_hospitals = service_hospitals.sort_values(by=['Distance'], ascending=True).head(10)
#     return nearby_hospitals

# #hospital_data = get_hospital_data()

# def generate_star_rating(rating, prefix):
#     full_stars = int(rating)
#     half_star = rating - full_stars
#     star_html = [
#         html.Div([

#         ]), 
#         html.H5(f"{prefix} Rating", style = {"text-align" : "center", "fontSize" : "15px"})
#     ]
#     star_html.extend([star_html.extend([html.Span('★', style={"color": "#FDDA0D", "fontSize": "24px", "marginRight": "2px"}) for _ in range(full_stars)])
#  ])

#     if half_star > 0:
#         star_html.append(html.Span('★', style={
#         "color": "#FDDA0D",
#         "fontSize": "24px",
#         "marginRight": "2px",
#         "position": "relative",
#         "display": "inline-block",
#         "width": "12px",  # Half width
#         "overflow": "hidden",
#         "left": "-1px",  # Move left to overlap
#         'top':'8.5px'
#     }))
#     return html.Div(star_html, style = {"text-align": "center"})

# @callback(
#     [Output('results-container', 'children'),
#     Output('compare-store', 'data')],
#     [Input('url', 'search'),
#      Input({'type': 'compare-button', "index": ALL}, 'n_clicks')], 
#      [State({'type': 'compare-button', "index": ALL}, 'id'),
#       State('compare-store', 'data')]
# )
# def display_results(search, n_clicks, stored_data, button_id):
#     hospital_data = get_hospital_data()
#     cards = []
#     hospital_data_to_store = []
#     hospital_data_to_store_json = json.dumps([])
#     #stored_hospital_data = json.loads(stored_data) if stored_data else []
#     stored_hospital_data = stored_data if isinstance(stored_data, list) else json.loads(stored_data) if stored_data else []
   
#     #if search:
#     params = search.replace('?', '').split('&')
#     print("params", params)
#     user_zip = params[0].split('=')[1]
#     print("user_zip", user_zip)
#     service_code = params[1].split('=')[1]
#     print("service_code", service_code)
    
#     nearby_hospitals = get_nearby_hospitals(hospital_data, user_zip, service_code)
#     print(nearby_hospitals)
    
#     for index, row in nearby_hospitals.iterrows():
#         card = dbc.Card(
#             dbc.CardBody(
#                 dbc.Row([
#                     dbc.Col(
#                         html.Div([
#                             html.Div(style={"height": "85px"}),
#                             html.Img(src="/assets/location.png",  style={"height":"30px","marginBottom": "5px", "textAlign": "center"}),
#                             html.Div(style={"height":"5px"}),
#                             html.P(f"{row['Distance']:.1f} Miles", style={"fontSize": "18px", "fontWeight": "bold"})
#                         ], style={"textAlign": "center", "padding": "5px"}),
#                         width="auto",
#                     ),
                    
#                     dbc.Col([
#                         html.Div(style={"height": "90px"}), 
#                         html.H4(row['Hospital Name']),
#                         html.Div([
#                             html.P(row['Address']),
#                         ]),    
#                     ], width=True, style={"paddingLeft": "1px", "borderRight": "1px solid #adcae6", "paddingTop": "10px"}),

            

#                     dbc.Col([
#                         html.Div(style={"height": "20px"}),
#                         html.P(f"Your Estimated Payment", style={"textAlign": "center"}),
#                         html.H4(f"${row['Estimate Payment']}", style={"color": "green"}),
#                         #html.P(f"Subtotal ${row['Hospital Fees'] + row['Physician Fees']}", style={"textAlign": "left"}),
#                         html.P([
#                         "Subtotal",
#                         html.Span(f"${row['Hospital Fees'] + row['Physician Fees']:.2f}",
#                         style={"display": "inline-block", "width": "100px", "text-align": "right",
#                         "paddingRight": '20px'})
#                         ], style={"margin": "0", "display": "flex", "justify-content": "space-between", "paddingTop":"40px"}),
#                         html.Hr(style={"width": "95%", "height": "2px", "borderWidth": "0", "color": "#add8e6",
#                         "backgroundColor": "#add8e6", "margin": "3px"}),
#                             html.P([
#                         "Discount",
#                         html.Span(f"${row['Discount'] :.2f}",
#                         style={"display": "inline-block", "width": "100px", "text-align": "right",
#                         "paddingRight": '20px'})
#                         ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
#                     ], width=True, style={"paddingLeft": "5px", "paddingTop": "10px"}),
                    
#                     dbc.Col([
#                         html.Div(style={"height": "20px"}), 
#                         html.P(f"Details", style={"text-align": "left"}),
#                         html.P(f"Estimated Charge ${row['Hospital Fees'] + row['Physician Fees']}"),
#                         html.P(f"Hospital Fees ${row['Hospital Fees']}"),
#                         html.P(f"Physician Fees ${row['Physician Fees']}"),
#                         #html.P(f"Discount ({((row['Discount']) / (row['Hospital Fees'] + row['Physician Fees'])) * 100:.1f}%) ${row['Discount']}", style = {"text-align": "left"}),
#                         html.P([
#                         f"Discount ({((row['Discount']) / (row['Hospital Fees'] + row['Physician Fees'])) * 100:.1f}%)",
#                         html.Span(f"${row['Discount'] :.2f}",
#                         style={"display": "inline-block", "width": "100px", "text-align": "right",
#                         "paddingRight": '20px'})
#                         ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
#                         html.Hr(style={"width": "90%", "height": "2px", "borderWidth": "0", "color": "#add8e6",
#             "backgroundColor": "#add8e6", "margin": "3px"}),
#                         html.P(f"Your Estimated Payment ${row['Hospital Fees'] + row['Physician Fees'] - row['Discount']}", style= {"color": "green"}),
#                     ], width=True, style={"paddingLeft": "5px", "borderRight": "1px solid #adcae6", "paddingTop": "10px"}),
                    
#                     dbc.Col([
#                         html.Div(style={"height": "70px"}),
#                         html.Div(generate_star_rating(row['Overall Star Rating'], "Overall Star")),
#                         #html.P(f"{row['Overall Star Rating']}", style={"text-align": "left"}),
#                         html.Div(generate_star_rating(row['Patient Survey Rating'], "Patient Survey")),
#                         #html.P(f"{row['Patient Survey Rating']}", style = {"text-align": "left"}),
#                         ], width=True, style={"paddingLeft": "5px", "paddingTop": "10px"}),

#                     dbc.Col([
#                         html.Button("Compare", id = {"type": "compare-button", "index": index}, n_clicks = 0, style={"display": "block", "marginBottom": "150px"})
#                     ], width="auto", style={"textAlign": "center", "display": "flex", "alignItems": "center", "justifyContent": "center"})
#                 ])
#             ),
#             style={"width": "98%", "margin": "10px", "display": "inline-block"}

                    
#         )
#         cards.append(card)

#     if any(n > 0 for n in n_clicks):
#         triggered = [i for i, n in enumerate(n_clicks) if n > 0]
#         for index in triggered:
#             print('index', index)
#             print('button_id', button_id)
#             ind_to_find = int(button_id[index]['index'])
#             print(ind_to_find)
#             hospital_data = nearby_hospitals.loc[ind_to_find]
#             hospital_data_dict = hospital_data.to_dict()
#             stored_hospital_data.append(hospital_data_dict)
#             print('stored_hospital_data', stored_hospital_data)

#     hospital_data_to_store_json = json.dumps(stored_hospital_data)

    
#     return dbc.Row(cards, justify="center"), hospital_data_to_store_json



# #input is compares_tool data output will be redirecting to compare url
# @callback(
#     Output('redirect', 'href', allow_duplicate=True),
#     Input('compare-store', 'data'),
#     #prevents from all callbacks being called
#     prevent_initial_call = True
# )

# def redirect_to_compare(compare_data):
#     if len(compare_data) > 500 and compare_data != '[]':
#         return f'/compare?data={quote(compare_data)}' 
#     return dash.no_update






############# new layout 2 starts here #########
import urllib.parse
import json
from dash import dcc, html, callback, Input, Output, State, no_update
from urllib.parse import quote, unquote
import dash
from dash import html, callback, Input, Output,dcc,State, ALL
from geopy.distance import geodesic
import pandas as pd
from geopy.geocoders import Nominatim
import pgeocode
import uuid
geocoder = pgeocode.Nominatim('us')

dash.register_page(__name__, path='/results')

layout = html.Div([html.Div(id='results-container', style={
    "padding": "40px",
    "backgroundColor": "white",
    "borderRadius": "10px",
    "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)",
    "minHeight": "635px",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "flexDirection": "column",
}),dcc.Store(id='compare-store', data=[], storage_type='memory'),
html.Div(id='hidden-store', style={'display': 'none'}),  # Hidden div to manage state,
# dcc.Location(id='url', refresh=False),
dcc.Location(id='compare-link', href='/compare',refresh=False),
dcc.Location(id='redirect', refresh=True),
# dcc.Link(id='compare-link2', href='/compare',refresh=False)

])

def extract_meta_information(file_path):
    df = pd.read_csv(file_path, nrows=2, encoding='cp1252')
    meta_info = df.iloc[0]
    hospital_name = meta_info.get('hospital_name', '').strip()
    hospital_address = meta_info.get('hospital_address', '').strip()
    hospital_zip = hospital_address.split(' ')[-1]
    return hospital_name, hospital_address, hospital_zip
#
def get_hospital_data():

    hospital_data = pd.read_csv(r"C:\Users\emgherghescu\OneDrive - Carilion\Documents\my_dash_app\data\PricingTransparency.csv")
    hospital_data.columns = hospital_data.columns.str.strip()
    hospital_data['Zip'] = hospital_data['Zip'].astype(str)
    hospital_data['CPT'] = hospital_data['CPT'].astype(str)
    if 'Hospital Type' not in hospital_data.columns:
        hospital_data['Hospital Type'] = 'N/A'
    if 'Provides Emergency Services?' not in hospital_data.columns:
        hospital_data['Provides Emergency Services?'] = 'N/A'
    print(hospital_data)
    return hospital_data

def get_lat_lon(zip_code, cache):
    if zip_code in cache:
        return cache[zip_code]

    location = geocoder.query_postal_code(zip_code)
    if location.latitude and location.longitude:
        coords = (location.latitude, location.longitude)
    else:
        coords = (None, None)

    cache[zip_code] = coords
    return coords


def get_nearby_hospitals(hospital_data, user_zip, service_code=None, service_description=None):
    cache = {}
    user_lat, user_lon = get_lat_lon(user_zip, cache)
    if user_lat is None or user_lon is None:
        raise ValueError("Invalid ZIP code. Unable to get location.")
    user_coords = (user_lat, user_lon)
    # print(hospital_data.columns)
    unique_zip_codes = hospital_data['Zip'].unique()
    zip_coords = {zip_code: get_lat_lon(zip_code, cache) for zip_code in unique_zip_codes}

    hospital_data['Latitude'] = hospital_data['Zip'].map(lambda zip: zip_coords[zip][0])
    hospital_data['Longitude'] = hospital_data['Zip'].map(lambda zip: zip_coords[zip][1])
    hospital_data['CPT'] = hospital_data['CPT'].astype(str).str.strip()
    hospital_data['Procedure Name'] = hospital_data['Procedure Name'].astype(str).str.strip()

    # Decode URL encoding for service_code and service_description

    if service_code:
        service_code = urllib.parse.unquote(service_code).strip()
        print(service_code)
    # if service_description:
    #     service_description = urllib.parse.unquote(service_description).strip()
    #     print(service_description)


    # Filter hospitals based on service_code or service_description
    if service_code:
        print('cpt')
        service_hospitals = hospital_data[hospital_data['CPT'] == str(service_code)]
        if service_hospitals.empty:
            print('No results found with CPT_Code. Checking Service_Description')
            service_hospitals = hospital_data[
                hospital_data['Procedure Name'].str.contains(service_code, case=False, na=False)]


    else:
        raise ValueError("Either CPT or Procedure Name must be provided.")

    if service_hospitals.empty:
        raise ValueError("No hospitals found with the specified CPT code or Procedure Name.")

    def calculate_distance(row):
        hospital_coords = (row['Latitude'], row['Longitude'])
        return geodesic(user_coords, hospital_coords).miles

    service_hospitals['Distance'] = service_hospitals.apply(calculate_distance, axis=1)
    nearby_hospitals = service_hospitals[service_hospitals['Distance'] <= 5]
    nearby_hospitals.drop_duplicates(subset=['Hospital Name', 'Zip','CPT','Procedure Name','Estimate Payment','Hospital Fees', 'Discount'], inplace=True)
    return nearby_hospitals.sort_values(by='Distance')

# def get_hospital_data():
#     hosp_data= pd.read_csv(r'C:\Users\shikh\Documents\Ella_dash_app\data\PricingTransparency_2.csv')
#     return hosp_data
# hospital_data = get_hospital_data()

def generate_star_rating(rating, pre):
    full_stars = int(rating)  # Number of full stars
    half_star = rating - full_stars  # Check for half star
    empty_stars = 5 - full_stars - (1 if half_star > 0 else 0)  # Remaining empty stars

    star_html = [
        html.Div(style={"height": "15px"}),  # Custom break space
        html.H5(f"{pre} Rating", style={"margin": "0", "textAlign": "center", "color": "#1C2337", "fontSize": "15px"})
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

def remove_hosp_duplicates(hospital_data_list):
    seen = set()
    unique_data = []
    for data_dict in hospital_data_list:
        # Convert dictionary to a frozenset for immutability and hashability
        frozen_dict = frozenset(data_dict.items())
        if frozen_dict not in seen:
            seen.add(frozen_dict)
            unique_data.append(data_dict)
    return unique_data

@callback(
    [Output('results-container', 'children'),
     Output('compare-store', 'data'),
     ],
    [Input('url', 'search'),
     Input({'type': 'compare-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'compare-button', 'index': ALL}, 'id'),
     State('compare-store', 'data')]
)
def display_results_and_manage_store(search, n_clicks, button_ids,stored_data):
    hospital_data = get_hospital_data()
    # Initialize empty variables
    cards = []
    hospital_data_to_store = []
    hospital_data_to_store_json = json.dumps([])  # Initialize with empty list
    stored_hospital_data = json.loads(stored_data) if stored_data else []
    # Handle search query
    if not search:
        return "No search query provided.", dash.no_update

    params = {k: v for k, v in (x.split('=') for x in search.lstrip('?').split('&'))}
    location = params.get('location')
    service = params.get('service')
    
    if not location or not service:
        return "Invalid search query.", dash.no_update

    try:
        nearby_hospitals = get_nearby_hospitals(hospital_data, location, service_code=service)
    except ValueError as e:
        return html.P(str(e), style={"textAlign": "center"}), dash.no_update

        # Create cards and handle button clicks
    for index, row in nearby_hospitals.iterrows():
        # Prepare data for the card
        address_parts = row['Address'].split(' ', 3)
        if len(address_parts) >= 3:
            address_line_1 = ' '.join(address_parts[:3])
            city_state_zip = address_parts[3]
            city_state_zip_parts = city_state_zip.rsplit(' ', 2)
            if len(city_state_zip_parts) == 3:
                city = city_state_zip_parts[0]
                state = city_state_zip_parts[1]
                zip_code = city_state_zip_parts[2]
            else:
                city = ''
                state = ''
                zip_code = ''
        else:
            address_line_1 = row['Address']
            city = ''
            state = ''
            zip_code = ''

        # Create HTML for the card
        miles_info = html.Div([
            html.Img(src='/assets/location.png', style={"height": "30px", "marginBottom": "10px"}),
            html.Div(style={"height": "5px"}),  # Custom break space
            html.P(f"{row['Distance']:.1f} Miles", style={"fontSize": "24px", "fontWeight": "bold"})
        ], style={"flex": "0 0 80px", "textAlign": "center", "padding": "10px"})

        hospital_info = html.Div([
            html.H5(row['Hospital Name'], style={"margin": "0", "marginLeft": "10px"}),
            html.Div(style={"height": "10px"}),  # Custom break space
            html.P(address_line_1, style={"margin": "0", "marginLeft": "10px"}),
            html.P(f"{city} {state} {zip_code}", style={"margin": "0", "marginLeft": "10px"}),
            html.Div(style={"height": "10px"}),  # Custom break space
        ], style={"flex": "1", "padding": "10px", "paddingLeft": "35px"})

        

        estimated_payment = html.Div([
            html.H5("Your Estimated Payment", style={"color": "#1C2337", "fontWeight": "bold", "margin": "0", 'textAlign': 'center'}),
            html.Div(style={"height": "10px"}),  # Custom break space
            html.P(f"${row['Hospital Fees'] + row['Physician Fees']- row['Discount']:.2f}",

                   style={"fontSize": "30px", "color": "green", "fontWeight": "bold", "margin": "0",
                          'textAlign': 'center'}),
            html.Div(style={"height": "35px"}),  # Custom break space
            html.P([
                "Subtotal",
                html.Span(f"${row['Hospital Fees'] + row['Physician Fees']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '20px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
            html.Hr(style={"width": "95%", "height": "2px", "borderWidth": "0", "color": "#add8e6",
                           "backgroundColor": "#add8e6", "margin": "3px"}),
            html.P([
                "Discount",
                html.Span(f"${row['Discount']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '20px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
        ], style={"padding": "10px", 'paddingLeft': '20px', "flex": "1"})

        details = html.Div([
            html.H5("Details", style={"fontWeight": "bold", "margin": "0"}),
            html.Div(style={"height": "20px"}),  # Custom break space
            html.P([
                "Estimated Charge:  ",
                html.Span(f"${row['Hospital Fees'] + row['Physician Fees']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '10px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
            html.P([
                "Hospital fees:  ",
                html.Span(f"${row['Hospital Fees']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '10px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between","marginLeft": '10px'}),
            html.P([
                "Physician fees:  ",
                html.Span(f"${row['Physician Fees']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '10px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between","marginLeft": '10px'}),
            html.P([
                f"Discount ({((row['Discount']) / (row['Hospital Fees'] + row['Physician Fees'])) * 100:.1f}%): ",
                html.Span(f"-${row['Discount']:.2f}",
                          style={"display": "inline-block", "width": "100px", "text-align": "right",
                                 "paddingRight": '10px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between"}),
            html.Hr(style={"width": "95%", "height": "2px", "borderWidth": "0", "color": "#add8e6",
                           "backgroundColor": "#add8e6", "margin": "3px"}),
            html.P([
                "Your Estimated Payment: ",
                html.Span(f"${row['Hospital Fees'] + row['Physician Fees'] - row['Discount']:.2f}",
                          style={"color": "green", "fontWeight": "bold", "display": "inline-block", "width": "100px",
                                 "text-align": "right", "paddingRight": '10px'})
            ], style={"margin": "0", "display": "flex", "justify-content": "space-between", "color": "green"})
        ], style={"padding": "10px", "paddingLeft": '20px', "flex": "1"})

        estimated_payment_and_details = html.Div([
            estimated_payment,
            details
        ], style={"display": "flex", "flex": "1", "padding": "10px", "borderRight": "1px solid #ddd"})

        ratings=html.Div([
    html.Div([
         generate_star_rating(row['Overall Star Rating'], "Overall Star"),
         generate_star_rating(row['Patient Survey Rating'], "Patient Survey"),
    ], style={"display": "inline-block", "verticalAlign": "top"}),])
        # overall_ratings = generate_star_rating(row['Overall Star Rating'], "Over Star")
        # patient_rating= generate_star_rating(row['Patient Survey Rating'],"Patient Survey")
        compare_button = html.Div([
            html.Button("Compare", id={'type': 'compare-button', 'index': index}, n_clicks=0,
                        style={"width": "100px", "height": "50px", "marginTop": "20px", "marginLeft": "10px","backgroundColor": "#adcae6",
                               "color": "#1C2337", "fontWeight": "bold",
                               "borderRadius": "10px", "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)"})
        ], style={"textAlign": "right", "marginTop": "20px"})
        ratings_and_button = html.Div([

            ratings,
            compare_button
        ], style={"display": "flex", "justify-content": "space-between", "align-items": "center", "padding": "10px"})

        card = html.Div([
            html.Div([
                miles_info,
                hospital_info
            ], style={"flex": "0 0 30%", "display": "flex", "borderRight": "1px solid #ddd", "padding": "10px"}),

            estimated_payment_and_details,

            html.Div([
                ratings_and_button
            ], style={"flex": "0 0 20%", "padding": "10px"})
        ], style={"display": "flex", "border": "1px solid #ddd", "borderRadius": "10px", "padding": "10px",
                  "marginBottom": "20px", "backgroundColor": "#f9f9f9"})

        cards.append(card)

    # Handle button clicks to update data
    if any(n > 0 for n in n_clicks):
        triggered = [i for i, n in enumerate(n_clicks) if n > 0]
        for index in triggered:
            print('index',index)
            print(button_ids[index])
            print('button_ids',button_ids[index]['index'])

            ind_to_find= int(button_ids[index]['index'])


            hospital_data = nearby_hospitals.loc[ind_to_find]
            hospital_data_dict = hospital_data.to_dict()

            stored_hospital_data.append(hospital_data_dict)

    stored_hospital_data = remove_hosp_duplicates(stored_hospital_data)

    # Convert list of hospital data to JSON string
    hospital_data_to_store_json = json.dumps(stored_hospital_data)
  
    return html.Div(className="row",
                    children=cards,
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "gap": "20px"
                    }), hospital_data_to_store_json

@callback(
        Output({'type': 'compare-button', 'index': ALL}, 'style'),
        Input({'type': 'compare-button', 'index': ALL}, 'n_clicks'),
        State({'type': 'compare-button', 'index': ALL}, 'style')
)
def update_button_color(n_clicks_list, current_styles):
    new_styles = []
    for n_clicks, current_styles in zip(n_clicks_list, current_styles):
        if n_clicks > 0:
            new_style = current_styles.copy()
            new_style['backgroundColor'] = 'green'
            new_styles.append(new_style)
        else:
            new_styles.append(current_styles)
    return new_styles




@callback(
    Output('redirect', 'href', allow_duplicate=True),
    [Input('compare-store', 'data')],
prevent_initial_call=True
)
def redirect_to_compare_page(compare_data):
    print(len(compare_data))
    if len(compare_data)>500 and compare_data != '[]':

        return f'/compare?data={quote(compare_data)}'
    return no_update
 