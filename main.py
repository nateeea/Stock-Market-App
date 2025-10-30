import account
import orders
import data
import plotting
print(data.get_daily_history("AAPL",period="6mo",interval="1wk"))
print(data.get_daily_history("AAPL",period="6mo",interval="1wk"))

print(data.get_latest_price("AAPL"))

plotting.plot_stock(data.get_daily_history("AAPL",period="6mo",interval="1wk"))