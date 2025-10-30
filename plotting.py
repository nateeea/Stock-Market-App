import yfinance as yf
import asciichartpy as asciichart
import math
import util

# Parameters
symbol = "TSLA"
period = "1mo"
interval = "1d"
chart_width = 70  # constant width

# Get historical data
df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
df = df.reset_index()
df['Date'] = df['Date'].dt.strftime("%m/%d/%y")

prices = df['Close'].values
prices = [float(p) for p in prices]
dates = df['Date'].tolist()

# Resample prices to fit the fixed width
if len(prices) > chart_width:
    factor = len(prices) / chart_width
    sampled_prices = []
    sampled_dates = []
    for i in range(chart_width):
        idx = int(i * factor)
        sampled_prices.append(prices[idx])
        sampled_dates.append(dates[idx])
else:
    sampled_prices = prices
    sampled_dates = dates
    chart_width = len(prices)

# Plot chart
config = {
    'colors': [asciichart.green],
    'height': 15,
    'format': '{:8.2f}',
    'offset': 3
}
chart_lines = asciichart.plot(sampled_prices, config).split('\n')

util.clear()
# Print chart with dates below
print("\n" + symbol,period + " Chart:" )
for line in chart_lines:
    print(line)

# Print dates at roughly equal intervals under the chart
num_labels = 5  # how many dates to show
step = max(1, int(chart_width) // num_labels)
label_line = "   "
for i in range(chart_width):
    if i % step == 0:
        label_line += sampled_dates[i][:5].center(step)  # first 5 chars (MM/DD)
    else:
        label_line += ''
    if i == chart_width - 1:
        label_line += sampled_dates[i][:5].center(step)
print(label_line)
