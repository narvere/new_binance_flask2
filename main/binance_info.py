import os

from binance.client import Client
import dotenv

dotenv.load_dotenv('.env')

api_key = os.environ['api_key']             # binance api_key
api_secret = os.environ['api_secret']       # binance api_secret

# pip install python-binance


client = Client(api_key, api_secret)

status = client.get_system_status()
info = client.get_account()
balances = info.get('balances')
orders = client.get_open_orders()
exchange_info = client.get_exchange_info()
