import os
import requests
import hmac
import hashlib
import time

def transfer_crypto(api_key, secret_key, amount, address):
    base_url = 'https://api.binance.com'
    endpoint = '/wapi/v3/withdraw.html'
    timestamp = int(time.time() * 1000)
    
    params = {
        'asset': 'USDT',
        'address': address,
        'amount': amount,
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
    address = os.getenv('WITHDRAW_ADDRESS')
    if api_key and secret_key and address:
        transfer_crypto(api_key, secret_key, 10, address)
    else:
        print("API key, Secret key, and Withdraw address must be set in environment variables.")
