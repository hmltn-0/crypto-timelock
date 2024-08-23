import os
import requests
import hmac
import hashlib
import time
import logging

logging.basicConfig(level=logging.INFO)

def buy_crypto(amount, currency):
    api_key = os.getenv('BINANCE_API_KEY')
    secret_key = os.getenv('BINANCE_SECRET_KEY')
    if not api_key or not secret_key:
        logging.error("API key and Secret key must be provided via environment variables.")
        return

    try:
        timestamp = int(time.time() * 1000)
        query_string = f"symbol={currency}USDT&side=BUY&type=MARKET&quantity={amount}&timestamp={timestamp}"
        signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        url = f"https://api.binance.com/api/v3/order?{query_string}&signature={signature}"
        headers = {'X-MBX-APIKEY': api_key}

        response = requests.post(url, headers=headers)
        response.raise_for_status()
        logging.info(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")

if __name__ == "__main__":
    buy_crypto(0.001, 'BTC')
