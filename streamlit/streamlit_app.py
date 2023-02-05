import streamlit as st
from pathlib import Path
import pandas as pd
import pydeck as pdk
import requests

st.set_page_config(layout='wide', page_title='Brewer Finder App')

# Title
st.markdown('# Brewery Finder App')
st.write('Find nearby breweries that match your desired features.')


def geocode(address):
    params = {'format': 'json',
              'addressdetails': 1,
              'q': address}
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
    headers = {'user-agent': user_agent}
    response = requests.get('http://nominatim.openstreetmap.org/search',
                            params=params, headers=headers)
    lat = response.json()[0]['lat']
    lon = response.json()[0]['lon']
    return lat, lon


def plot_map(df, lat=None, lon=None):
    # Remove locations with null lat/lon values
    df = df.dropna()

    if lat is None:
        view_state = pdk.data_utils.compute_view(
            df[['longitude', 'latitude']], 0.8)
    else:
        # view_state = pdk.ViewState(
        #     latitude=lat,
        #     longitude=lon,
        #     zoom=11,
        #     pitch=0)
        view_state = pdk.data_utils.compute_view(
            df[['longitude', 'latitude']], 0.8)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=500,
                pickable=True
            ),
        ],
        tooltip={"text": "{name}"},
    ))
    return


def load_df(outdoors, dogs):
    # raw df
    filepath = Path('./assets/ma_breweries_features.csv')
    df = pd.read_csv(filepath)
    if outdoors and not dogs:
        query_df = df.query('has_patio == 1')
    elif dogs and not outdoors:
        query_df = df.query('dog_friendly == 1')
    elif outdoors and dogs:
        query_df = df.query('has_patio == 1 & dog_friendly == 1')
    else:
        query_df = df
    return query_df


def display_map(query_df, address=None):
    if address:
        lat, lon = geocode(address)
    else:
        lat = None
        lon = None

    plot_map(query_df, lat, lon)
    return


def display_df(query_df):
    # clean df for display
    columns = ['name', 'city', 'street', 'has_food', 'has_patio']
    display_df = query_df[columns].sort_values(by='city')
    return display_df


# Sidebar address search
st.sidebar.subheader("""Find Nearby Breweries""")
address_input = st.sidebar.text_input("Enter address:", "Boston, MA")
find_button = st.sidebar.button("FIND")

if find_button:
    url = 'https://api.mapbox.com/geocoding/v5/{endpoint}/{search_text}.json'

# Sidebar filters
st.sidebar.subheader("""Filters""")
outdoor_box = st.sidebar.checkbox("Outdoor Seating")
dog_box = st.sidebar.checkbox("Dog Friendly")
food_box = st.sidebar.checkbox("Food Available")
tour_box = st.sidebar.checkbox("Tours Available")
group_box = st.sidebar.checkbox("Good for Large Groups")

# defaults
outdoors = False
dogs = False
address = None

if outdoor_box:
    outdoors = True
if dog_box:
    dogs = True
if tour_box:
    tours = True

if find_button:
    address = address_input

df = load_df(outdoors, dogs)
display_map(df, address)
st.dataframe(display_df(df))

st.subheader("About this app")
st.markdown("""
This app... <insert description>

You can see how this works in the my [Jupyter Notebooks](https://github.com/data-science-sandbox/nlp-brewer-finder/tree/main/notebooks) 
or [see all the code](https://github.com/data-science-sandbox/nlp-brewer-finder).
""")
