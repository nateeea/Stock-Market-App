from alpaca_trade_api import REST
import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

api_key = os.getenv("api_key")
secret_key = os.getenv("secret_key")
base_url = os.getenv("base_url")

# Create Alpaca client
api = REST(api_key, secret_key, base_url)