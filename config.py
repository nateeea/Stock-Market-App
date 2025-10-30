from alpaca_trade_api import REST
import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
base_url = os.getenv("base_url")

# Create Alpaca client
api = REST(api_key, api_secret, base_url)