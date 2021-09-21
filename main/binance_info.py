from binance.client import Client

# pip install python-binance
api_key = 'xf1nSACZEAiVbsgmYZjsglEE0jnbxITQ2vNYrRRd6vufcNsiC0UfIu1zZIaaeLBf'
api_secret = 'k0T8k2CqEtH7H4YLBdmWhPkcbDFOMw2brTWo01LPd0xtkpiP715BrP4ZIQXOW71l'

client = Client(api_key, api_secret)

status = client.get_system_status()
info = client.get_account()
balances = info.get('balances')
orders = client.get_open_orders()
