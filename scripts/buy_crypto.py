import os
import requests
import time
import hmac
import hashlib
import base64

def buy_crypto(api_key, secret_key, passphrase, amount, product_id):
    base_url = 'https://api.pro.coinbase.com'
    endpoint = '/orders'
    url = f'{base_url}{endpoint}'
    method = 'POST'
    timestamp = str(time.time())

    body = {
        "type": "market",
        "side": "buy",
        "product_id": product_id,
        "funds": amount
    }

    message = timestamp + method + endpoint + str(body)
    signature = hmac.new(base64.b64decode(secret_key), message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode()

    headers = {
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    api_key = os.getenv('COINBASE_API_KEY')
    secret_key = os.getenv('COINBASE_SECRET_KEY')
    passphrase = os.getenv('COINBASE_PASSPHRASE')
    if api_key and secret_key and passphrase:
        buy_crypto(api_key, secret_key, passphrase, '100', 'BTC-USD')
    else:
        print("API key, Secret key, and Passphrase must be set in environment variables.")
