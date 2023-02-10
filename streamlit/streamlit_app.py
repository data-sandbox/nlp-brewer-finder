import streamlit as st
from pathlib import Path
import pandas as pd
import pydeck as pdk
import requests

st.set_page_config(layout='wide', page_title='Brewery Finder App 🍻')

# Title
st.markdown('# Brewery Finder 🍻')
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
    # if lat is None:
    #     view_state = pdk.data_utils.compute_view(
    #         df[['longitude', 'latitude']], 0.8)
    # else:
    # view_state = pdk.ViewState(latitude=lat, longitude=lon,
    #                            zoom=10, bearing=0, pitch=0)
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


def load_df():
    # raw df
    filepath = Path('./assets/breweries_app.csv')
    df = pd.read_csv(filepath)
    query = []
    if outdoors:
        query.append('outdoors == 1')
    if food:
        query.append('food == 1')
    if dogs:
        query.append('dogs == 1')
    if music:
        query.append('music == 1')
    if games:
        query.append('games == 1')
    if tours:
        query.append('tours == 1')
    if not query:
        query_df = df
    else:
        query_df = df.query(" & ".join(query))
    return query_df


def display_map(query_df, lat, lon):
    # if address:
    #     lat, lon = geocode(address)
    # else:
    #     lat = None
    #     lon = None

    plot_map(query_df)
    return


def display_df(query_df):
    # clean df for display
    columns = ['name', 'state', 'city', 'street',
               #    'outdoors', 'food', 'games', 'music', 'tours'
               ]
    display_df = query_df[columns].sort_values(by='city')
    return display_df


# Sidebar address search
st.sidebar.subheader("""Find Nearby Breweries""")
address_input = st.sidebar.text_input("Enter address:", "Boston, MA")
find_button = st.sidebar.button("FIND")

# Sidebar filters
st.sidebar.subheader("""Filters""")
outdoors = st.sidebar.checkbox("Outdoor Seating")
food = st.sidebar.checkbox("Food Served")
dogs = st.sidebar.checkbox("Dog Friendly")
games = st.sidebar.checkbox("Games Available")
music = st.sidebar.checkbox("Live Music")
tours = st.sidebar.checkbox("Tours Offered")


if find_button:
    lat, lon = geocode(address_input)
    st.write(lat, lon)

df = load_df()
# display_map(df, lat, lon)
plot_map(df)
st.dataframe(display_df(df))

st.subheader("About this app")
st.markdown("""
This app... <insert description>

You can see how this works in the my [Jupyter Notebooks](https://github.com/data-science-sandbox/nlp-brewer-finder/tree/main/notebooks)
or [see all the code](https://github.com/data-science-sandbox/nlp-brewer-finder).
""")
