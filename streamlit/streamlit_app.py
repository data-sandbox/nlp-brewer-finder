import streamlit as st
from pathlib import Path
import pandas as pd
import requests
from streamlit_folium import folium_static
import folium


st.set_page_config(layout='wide', page_title='Brewery Finder App 🍻')


# Initialization
if 'lat' not in st.session_state:
    st.session_state.lat = 42.3554334
if 'lon' not in st.session_state:
    st.session_state.lon = -71.060511
if 'zoom' not in st.session_state:
    st.session_state.zoom = 9

# Title
st.markdown('# Brewery Finder 🍻')
st.write('Find nearby breweries based on their offerings.')

# DEBUG
# st.write(st.session_state.lat1)
# st.write(st.session_state.lon1)


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


# def plot_map():

    view_state = pdk.data_utils.compute_view(
        filt_df[['longitude', 'latitude']], 0.8)
    # else:
    # lat = 42.3554334
    # lon = -71.060511
    # view_state = pdk.ViewState(latitude=lat, longitude=lon,
    #                            zoom=10, bearing=0, pitch=0)

    # t1 = st.session_state.lat1
    # t2 = st.session_state.lon1
    # t2 = -71.060511
    # if not st.session_state.new_address:
    #     print('yes')
    #     lat1 = lat1g
    #     lon1 = lon1g

    # view_state = pdk.ViewState(latitude=lat1, longitude=lon1,
    #                            zoom=10, bearing=0, pitch=0)
    # view_state = pdk.ViewState(latitude=st.session_state.lat1, longitude=st.session_state.lon1,
    #                            zoom=10, bearing=0, pitch=0)
    # view_state = pdk.data_utils.compute_view(
    #     df[['longitude', 'latitude']], 0.8)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        # api_keys={
        #     'mapbox': 'pk.eyJ1IjoiZHMtc2FuZGJveCIsImEiOiJjbGR5bGZtcm0wa3c1M3BwcmhpdHFyc2szIn0.60-2UTgzKoRIWLX_tVoDFw'},
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filt_df,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=500,
                pickable=True
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=inv_df,
                get_position='[longitude, latitude]',
                get_color='[150, 150, 150, 100]',
                get_radius=500,
                pickable=True
            ),
        ],
        tooltip={"text": "{name}\nTest"},
    ))
    return


@st.cache()
def load_df():
    # raw df
    filepath = Path('./assets/breweries_app.csv')
    df = pd.read_csv(filepath)
    return df


@st.cache()
def apply_filters(df):
    query = []
    buttons = [outdoor, food, dog, games, music, tour]
    # TODO generate the list of buttons and filters from one single list
    filt_columns = ['outdoor_', 'food_', 'dog_', 'games_', 'music_', 'tour_']
    for button, filter in zip(buttons, filt_columns):
        if button:
            query.append(f"{filter} != 'No'")
    if not query:
        query_df = df
        inverse_df = None
    else:
        query_df = df.query(" & ".join(query))
        inverse_df = pd.concat([df, query_df]).drop_duplicates(keep=False)
    if inverse_df is None:
        inverse_df = pd.DataFrame()
    return query_df, inverse_df


# def display_map(query_df, lat, lon):
#     # if address:
#     #     lat, lon = geocode(address)
#     # else:
#     #     lat = None
#     #     lon = None

#     plot_map(query_df)
#     return

# @st.cache_data
def display_df(query_df):
    # clean df for display
    columns = ['name', 'state', 'city', 'street'
               #    'outdoors', 'food', 'games', 'music', 'tours'
               ]
    display_df = query_df[columns].sort_values(by='city')
    # display_df.assign(hack='').set_index('hack')
    return display_df


# Sidebar address search
st.sidebar.subheader("""Find Nearby Breweries""")
address_input = st.sidebar.text_input("Enter address:", "Boston, MA")
# find_button = st.sidebar.button("FIND", key="new_address")
find_button = st.sidebar.button("FIND")

# Sidebar filters
st.sidebar.subheader("""Filters""")
outdoor = st.sidebar.checkbox("Outdoor Seating")
food = st.sidebar.checkbox("Food Served")
dog = st.sidebar.checkbox("Dog Friendly")
games = st.sidebar.checkbox("Games Available")
music = st.sidebar.checkbox("Live Music")
tour = st.sidebar.checkbox("Tours Offered")

if address_input:
    # lat, lon = geocode(address_input)
    st.session_state.lat, st.session_state.lon = geocode(address_input)
    # lat1g, lon1g = geocode(address_input)
    # lat1, lon1 = geocode(address_input)
    # try under enter button click
    # df, inv_df = load_df()
    # plot_map()

if find_button:
    st.session_state.zoom = 12

# if find_button:
    # Current location:
#     icon = folium.Icon(color='red')
#     current_loc = folium.Marker(location=[st.session_state.lat1,
#                                           st.session_state.lon1],
#                                 icon=icon,
#                                 tooltip="You are here.")
# else:
#     current_loc = None

df = load_df()
filt_df, inv_df = apply_filters(df)

m = folium.Map(location=[st.session_state.lat,
               st.session_state.lon],
               tiles="cartodbpositron",
               zoom_start=st.session_state.zoom)

# if current_loc:
#     current_loc.add_to(m)


def get_html(row):
    # Generate html string for popup
    html = f'''
        <a href={row.loc['website_url']} target="_blank"><b style="font-size:12px; ">{row.loc['name']}</b></a>
        <br>
        {row.loc['street']}, {row.loc['city']}
        <br>
        <br>
        Outdoor seating: <b>{row.loc['outdoor_']}</b>
        <br>
        Food: <b>{row.loc['food_']}</b>
        <br>
        Dog friendly: <b>{row.loc['dog_']}</b>
        <br>
        Games: <b>{row.loc['games_']}</b>
        <br>
        Live music: <b>{row.loc['music_']}</b>
        <br>
        Tours: <b>{row.loc['tour_']}</b>
        '''
    return html


# popup width
min_width = 180
max_width = 180

for index, row in filt_df.iterrows():
    icon = folium.Icon(color='blue', icon='light fa-check', prefix='fa')
    popup = folium.Popup(
        get_html(row), min_width=min_width, max_width=max_width)
    folium.Marker(location=[row.loc['latitude'], row.loc['longitude']],
                  icon=icon,
                  #   popup=f"{row.loc['name']} {row.loc['street']}",
                  popup=popup,
                  tooltip=row.loc['name']).add_to(m)

if not inv_df.empty:
    for index, row in inv_df.iterrows():
        icon = folium.Icon(color='lightgray',
                           icon='light fa-xmark', prefix='fa')
        popup = folium.Popup(
            get_html(row), min_width=min_width, max_width=max_width)
        folium.Marker(location=[row.loc['latitude'], row.loc['longitude']],
                      icon=icon,
                      popup=popup,
                      tooltip=row.loc['name']).add_to(m)

folium_static(m)

# st.dataframe(display_df(filt_df))


st.subheader("About this app")
st.markdown("""
This app uses webscraped brewery reviews from Tripadvisor and a Natural Languaging Processing (NLP) model
to identify what offerings are available at each brewery. 

You can see how this works in my
[Jupyter Notebooks](https://github.com/data-science-sandbox/nlp-brewer-finder/tree/main/notebooks)
or [see all the code](https://github.com/data-science-sandbox/nlp-brewer-finder).

Credit to [Open Brewery DB](https://www.openbrewerydb.org/) for compiling the brewery list.
""")
