import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly


def initial_config():
    st.set_page_config(
        page_title="The Crypto Clairvoyant",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="assets/crypto_logo.png",
    )

	# Set a start data for the yahoo finance data
    start = "2016-01-01"
    today = date.today().strftime("%Y-%m-%d")

    coins = ("BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD")
    return start, today, coins


def cc_sidebar(coins):
	# Using streamlit's built-in sidebar we ask the user for a coin pair and a time period 
	# for making the forecast
    st.sidebar.image(image="assets/crypto_logo.png", width=32)
    st.sidebar.header("The Crypto Clairvoyant")
    st.sidebar.caption(
        "A cryptocurrency price forecast web-app made using Streamlit for the front-end and Facebook Prophet for the actual time series forcasting algorithm."
    )

    selected_coins = st.sidebar.selectbox("Select coin pair for forecast", coins)
    years = st.sidebar.slider("Years of prediction:", 1, 4)
    st.sidebar.caption("Disclaimer: Not to be taken as financial advice")
    return selected_coins, years


@st.cache
def load_data(ticker, start, today):
	# Download data from yahoo finance API and store them in cache so as to load webpage faster
    data = yf.download(ticker, start, today)
    data.reset_index(inplace=True)
    return data


def get_formatted_value(dataframe, column):
	# Helper function to display stock price metrics such as highest price, median price
	# Gets the item at location -1 (the last) at the specified column and formats it accordingly
    data = dataframe.iloc[-1].at[column]
    return str(round(data, 2)) + "$"


def get_percentage_delta(current, past, column):
	# Helper function to display predicted gain/loss percentage
	# Get the current price from the "forecast" and the curent price from the 
	# "data" dataframe from yfinance and establish delta  
    data = current.iloc[-1].at[column] / past.iloc[-1].at["Close"] * 100
    return str(round(data, 2)) + "%"


def insert_spacers(container, lines):
	# As Streamlit is a more Machine-Learning and Data Science oriented framework,
	# its front-end capabilities are weak so this function insert a certain number of white spaces
    for x in range(lines):
        container.write("#")


def cc_body(m, forecast, years, data):
    col1, col2 = st.columns([3, 1])

	# Plot using the model and the forecast we got from fbprophet
    col1.subheader(f'Forecast plot for {years} {"year" if years == 1 else "years"}')
    fig1 = plot_plotly(m, forecast, xlabel=None, ylabel=None)

	# Front-end settings
    fig1.update_layout(
        margin=dict(t=10, l=0),
        height=500,
    )
    col1.plotly_chart(figure_or_data=fig1, use_container_width=True)

	# Metrics that show the highest, median and lowest predicted price
    col2.subheader("Predicted prices")
    insert_spacers(col2, 1)
    col2.metric(
        label="Highest Price",
        value=get_formatted_value(forecast, "trend_upper"),
        delta=get_percentage_delta(forecast, data, "trend_upper"),
    )
    insert_spacers(col2, 1)
    col2.metric(
        label="Median Price",
        value=get_formatted_value(forecast, "trend"),
        delta=get_percentage_delta(forecast, data, "trend"),
    )
    insert_spacers(col2, 1)
    col2.metric(
        label="Lowest Price",
        value=get_formatted_value(forecast, "trend_lower"),
        delta=get_percentage_delta(forecast, data, "trend_lower"),
    )

    st.subheader("Forecast data")
    st.write(forecast.tail())
    insert_spacers(st, 1)

    col3, col4 = st.columns([1, 3])
    col3.subheader("Interpretation")
    insert_spacers(col3, 2)

	# Again, Streamlit's capabilities are limited when it comes to front-end so 
	# we use html markdown to establish an h5 heading using the 5 "#" symbols
    col3.markdown(
        "##### The overall upward/downward momentum of a coin is seen in this graph."
    )
    insert_spacers(col3, 5)
    col3.markdown("##### This graph shows the average delta for every day of the week.")
    insert_spacers(col3, 5)
    col3.markdown("##### The yearly cycle of a coin's price is depicted on the right.")

    col4.subheader("Forecast components")
    insert_spacers(col4, 1)
    col4.write(m.plot_components(forecast))


def predict_price(selected_coins, start, today, years):
	# This function uses the fbprophet module for forecasting data based on past values
	# First we grab the data from the yfinance api and establish a number of days for which 
	# we want to make the prediction
	data = load_data(selected_coins, start, today)
	periods = years * 365

	# Then we prepare the dataframe for manipulation (it needs the date column to be named "ds")
	# and the values column to be named "y"
	df_train = data[["Date", "Close"]]
	df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

	# We fit the model and use the built-in method "make_future_dataframe" to extend it {period}
	# days into the future
	m = Prophet()
	m.fit(df_train)
	future = m.make_future_dataframe(periods=periods)
	forecast = m.predict(future)

	return m, forecast


def main():
    start, today, coins = initial_config()
    selected_coins, years = cc_sidebar(coins)
    m, forecast = predict_price(selected_coins, start, today, years)
    data = load_data(selected_coins, start, today)
    cc_body(m, forecast, years, data)


if __name__ == "__main__":
    main()
