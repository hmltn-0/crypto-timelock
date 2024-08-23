import requests
import hmac
import hashlib
import time

def buy_crypto(api_key, secret_key, amount, currency):
    timestamp = int(time.time() * 1000)
    query_string = f"symbol={currency}USDT&side=BUY&type=MARKET&quantity={amount}&timestamp={timestamp}"
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    url = f"https://api.binance.com/api/v3/order?{query_string}&signature={signature}"
    headers = {'X-MBX-APIKEY': api_key}

    response = requests.post(url, headers=headers)
    print(response.json())

if __name__ == "__main__":
    # Fetch your API keys from a secure location
    api_key = 'your_api_key'
    secret_key = 'your_secret_key'
    buy_crypto(api_key, secret_key, 0.001, 'BTC')
