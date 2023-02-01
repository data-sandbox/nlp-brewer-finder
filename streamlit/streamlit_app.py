"""Small example streamlit application."""
import streamlit as st
import pandas as pd
import altair as alt
import requests
import config


def app():
    """Define main application entry point."""
    st.title("Hello World!")
    # And write the rest of the app inside this function!
    st.markdown("Here is where you can insert more text.")
    st.markdown("""Streamlit works more on the basis of 
\"insert things and let Streamlit figure out how to render 
them\".  If you want more flexibility for how to render
the markdown and other elements on your webpage, 
you may want to consider
[Flask](https://flask.palletsprojects.com/).""")

    # get stock data
    API_URL = "https://www.alphavantage.co/query"
    data = {"function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": selected_stock,
            "outputsize": "full",
            "datatype": "json",
            "apikey": config.api_key}

    response = requests.get(API_URL, data)
    response_json = response.json()  # maybe redundant
    data = pd.DataFrame.from_dict(
        response_json['Time Series (Daily)'], orient='index', dtype='float').sort_index(axis=1)
    data = data.reset_index()
    data = data.rename(columns={'index': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low',
                       '4. close': 'Close', '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
    data['Date'] = pd.to_datetime(data['Date'])

    # base plot
    alt.data_transformers.enable('json')
    plot = alt.Chart(data).mark_line().encode(
        x='Date', y='Close')

    # filters in sidebar
    st.sidebar.subheader("""Additional Information""")
    high = st.sidebar.checkbox("High")
    low = st.sidebar.checkbox("Low")

    # complete plot
    st.altair_chart(plot, use_container_width=True)


# ticker search widget in sidebar
st.sidebar.subheader("""Stock Search App""")
selected_stock = st.sidebar.text_input("Enter stock ticker symbol:", "AAPL")
button_clicked = st.sidebar.button("GO")
if button_clicked == "GO":
    app()

if __name__ == '__main__':
    app()
