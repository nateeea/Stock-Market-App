import yfinance as yf
import pandas as pd

#Get the latest price for a given symbol
def get_latest_price(symbol):
    try:
        # Use Ticker.history which can be more reliable for single-symbol queries
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="1m", auto_adjust=True)
        if df is None or df.empty:
            # fallback to download
            df = yf.download(symbol, period="1d", interval="1m", auto_adjust=True)
        if df is None or df.empty:
            return None
        # get the latest close price
        latest = df["Close"].iloc[-1]
        return float(latest)
    except Exception:
        return None

#Get daily historical data for a given symbol
def get_daily_history(symbol, period="1mo", interval="1d"):
    data = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    data = data.reset_index()
    data['time'] = data['Date'].dt.strftime("%m/%d/%Y %I:%M %p")
    return data[['time','Open','High','Low','Close','Volume']]

#Get historical data for a given symbol with shorter intervals
def get_history(symbol, period="5d", interval="1m"):
    data = yf.download(symbol, period=period, interval=interval)
    data = data.reset_index()
    data['time'] = data['Datetime'].dt.strftime("%m/%d/%Y %I:%M %p")
    return data[['time','Open','High','Low','Close','Volume']]