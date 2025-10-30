import yfinance as yf
import pandas as pd

def get_latest_price(symbol):
    data = yf.download(symbol, period="1d", interval="1m", auto_adjust=True)
    return float(data["Close"].iloc[-1].item())

def get_daily_history(symbol, period="1mo", interval="1d"):
    data = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    data = data.reset_index()
    data['time'] = data['Date'].dt.strftime("%m/%d/%Y %I:%M %p")
    return data[['time','Open','High','Low','Close','Volume']]

def get_history(symbol, period="5d", interval="1m"):
    data = yf.download(symbol, period=period, interval=interval)
    data = data.reset_index()
    data['time'] = data['Datetime'].dt.strftime("%m/%d/%Y %I:%M %p")
    return data[['time','Open','High','Low','Close','Volume']]