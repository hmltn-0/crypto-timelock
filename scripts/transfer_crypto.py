import os
import requests
import time
import hmac
import hashlib
import base64

def transfer_crypto(api_key, secret_key, passphrase, amount, address):
    base_url = 'https://api.pro.coinbase.com'
    endpoint = '/withdrawals/crypto'
    url = f'{base_url}{endpoint}'
    method = 'POST'
    timestamp = str(time.time())

    body = {
        "crypto_address": address,
        "amount": amount,
        "currency": "BTC"
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
    address = os.getenv('WITHDRAW_ADDRESS')
    if api_key and secret_key and passphrase and address:
        transfer_crypto(api_key, secret_key, passphrase, '10', address)
    else:
        print("API key, Secret key, Passphrase, and Withdraw address must be set in environment variables.")
