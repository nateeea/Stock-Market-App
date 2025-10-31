import yfinance as yf
import asciichartpy as asciichart

def plot_stock(symbol, period="1mo", interval="1d"):
# Parameters

    chart_width = 80  # constant width
    #Returned String of Graph
    finalstring = ""

    # Get historical data
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    df = df.reset_index()
    df['Date'] = df['Date'].dt.strftime("%m/%d/%y")

    prices = [p.item() for p in df['Close'].values]
    dates = df['Date'].tolist()

    factor = len(prices) / chart_width
    sampled_prices = []
    sampled_dates = []
    for i in range(chart_width):
        idx = int(i * factor)
        sampled_prices.append(prices[idx])
        sampled_dates.append(dates[idx])


    # Plot chart
    config = {
        'colors': [asciichart.green],
        'height': 15,
        'format': '{:8.2f}',
        'offset': 3
    }
    chart_lines = asciichart.plot(sampled_prices, config).split('\n')

    # Print chart with dates below
    finalstring += (symbol + " " + period + " Chart:\n")
    for line in chart_lines:
        finalstring += line + "\n"

    #Sets the right number of spaces before the date labels
    label_line = ""
    for i in range (chart_lines[-1].find("┤")):
        label_line += " "
    #Strip off extra spaces to align with chart width
    label_line = label_line[:-round(chart_width/11)]

    # Print dates at roughly equal intervals under the chart
    num_labels = 5  # how many dates to show
    step = max(1, int(chart_width) // num_labels)
    for i in range(chart_width):
        if i % step == 0:
            label_line += sampled_dates[i][:5].center(step)  # first 5 chars (MM/DD)
        else:
            label_line += ''
        if i == chart_width - 1:
            label_line += sampled_dates[i][:5].center(step)
    finalstring += label_line
    print(finalstring)