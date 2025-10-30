from config import api

# Function to place a market order
def place_market_order(symbol, qty, side):
    # Example usage:
    # place_order('AAPL', 1, 'buy')

    order = api.submit_order(
        #Ticker symbol
        symbol=symbol,
        #Quantity to buy or sell
        qty=qty,
        #Buy or sell
        side=side,
        #Order type: market or limit
        type='market',
        #How long the order remains active
        time_in_force='gtc'
    )
    print(f"Order submitted: {side.upper()} {qty} {symbol}")
    return order

def place_limit_order(symbol, qty, side, limit_price):
    # Example usage:
    # place_order('AAPL', 1, 'buy', 150.00)

    order = api.submit_order(
        #Ticker symbol
        symbol=symbol,
        #Quantity to buy or sell
        qty=qty,
        #Buy or sell
        side=side,
        #Order type: market or limit
        type='limit',
        #How long the order remains active
        time_in_force='gtc',
        #Limit price for limit orders
        limit_price=limit_price
    )
    print(f"Order submitted: {side.upper()} {qty} {symbol}")
    return order

def get_open_orders():
    orders = api.list_orders(status="open")
    print("Open Orders:")
    for o in orders:
        print(f"{o.side.upper()} {o.qty} {o.symbol} - TYPE: {o.type.upper()} - {o.status}")
    return orders