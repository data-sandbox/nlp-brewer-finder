import streamlit as st
import pandas as pd
import requests
from streamlit_folium import folium_static
import folium


st.set_page_config(layout='wide', page_title='Brewery Finder 🍻')


# Initialization
if 'lat' not in st.session_state:
    st.session_state.lat = 42.3554334
if 'lon' not in st.session_state:
    st.session_state.lon = -71.060511
if 'zoom' not in st.session_state:
    st.session_state.zoom = 9

# Title
st.markdown('# Brewery Finder 🍻')
st.write('Find the best brewery for you!')

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


@st.cache()
def load_df():
    df = pd.read_csv('./streamlit/breweries_app.csv')
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


def display_df(query_df):
    # clean df for display
    columns = ['name', 'state', 'city', 'street']
    display_df = query_df[columns].sort_values(by='city')
    return display_df


# Sidebar address search
st.sidebar.subheader("""Find Nearby Breweries""")
address_input = st.sidebar.text_input("Enter address:", "Boston, MA")
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
    st.session_state.lat, st.session_state.lon = geocode(address_input)

if find_button:
    st.session_state.zoom = 11

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
               zoom_start=st.session_state.zoom,
               )

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
to identify the offerings at each brewery. 

You can see how this works in my
[Jupyter Notebooks](https://github.com/data-science-sandbox/nlp-brewer-finder/tree/main/notebooks)
or [see all the code](https://github.com/data-science-sandbox/nlp-brewer-finder).

Many thanks to [Open Brewery DB](https://www.openbrewerydb.org/) for compiling the brewery list.
""")
