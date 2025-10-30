import account
import orders
import data

print(data.get_daily_history("AAPL",period="6mo",interval="1wk"))

print(data.get_latest_price("AAPL"))