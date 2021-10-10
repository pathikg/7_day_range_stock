from nsetools import Nse
import yfinance as yf
import datetime as dt
from tqdm import tqdm
from utils import *
import streamlit as st
import plotly.graph_objects as go

start, end = get_last_7_days()

nse = Nse()
stock_codes = nse.get_stock_codes()

symbols = list(stock_codes.keys())[1:]
symbol = st.selectbox('Select Symbol', symbols)
ticker = yf.Ticker(f"{symbol}.ns")
df = ticker.history(start=start, end=end)
df.index.name = "Date"

if len(df) > 1:  # since there are some exceptions in data idk why only start date is coming for some stocks

    df = df[::-1]
    df = get_range(df)
    df = df[["Open", "Close", "High", "Low", "Range"]]
    st.write(f"Last 7 days data for {stock_codes[symbol]}")
    df.index = df.index.strftime("%Y-%m-%d")
    st.dataframe(df)
    range = df['Range']

    last_7_day_mean = range[1:].mean()
    current_range = range[0]

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df["Open"], high=df["High"],
                                         low=df["Low"], close=df["Close"])])
    fig.update_layout(
        title=f"Last 7 day performance for {stock_codes[symbol]} : ",
        xaxis_title="Date",
        yaxis_title="Price",
        font=dict(
            size=13,
        ),
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig)
    st.markdown(f"* **Previous Range** = {current_range}")
    st.markdown(
        f"* **Last 7 day average range**  = {last_7_day_mean}")


else:
    st.text("Symbol not found")
