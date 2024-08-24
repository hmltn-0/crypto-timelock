import os
import requests
import hmac
import hashlib
import time

def buy_crypto(api_key, secret_key, amount, currency):
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    
    params = {
        'symbol': f'{currency}USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': amount,
        'timestamp': timestamp
    }
    
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature
    
    headers = {
        'X-MBX-APIKEY': api_key
    }
    
    response = requests.post(base_url + endpoint, params=params, headers=headers)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    if api_key and secret_key:
        buy_crypto(api_key, secret_key, 0.001, 'BTC')
    else:
        print("API key and Secret key must be set in environment variables.")
