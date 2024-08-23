import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def transfer_crypto(amount, bank_account):
    api_key = os.getenv('EXCHANGE_API_KEY')
    secret_key = os.getenv('EXCHANGE_SECRET_KEY')
    if not api_key or not secret_key:
        logging.error("API key and Secret key must be provided via environment variables.")
        return

    try:
        # Placeholder URL and parameters; replace with actual API details
        url = 'https://api.exchange.com/v1/withdraw'
        params = {
            'api_key': api_key,
            'amount': amount,
            'bank_account': bank_account
        }
        response = requests.post(url, json=params)
        response.raise_for_status()
        logging.info(f"Successfully transferred {amount} to bank account {bank_account}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to transfer: {e}")

if __name__ == "__main__":
    transfer_crypto(10, 'your_bank_account')
