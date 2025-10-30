from config import api

def get_account_info():
    account = api.get_account()
    return {
        "id": account.id,
        "cash": account.cash,
        "portfolio_value": account.portfolio_value,
        "buying_power": account.buying_power,
        "status": account.status
    }

def get_account_element(element):
    account = api.get_account()
    return getattr(account, element, None)

def print_account_summary():
    info = get_account_info()
    print("Account Summary:")
    for key, value in info.items():
        print(f"{key.capitalize()}: {value}")