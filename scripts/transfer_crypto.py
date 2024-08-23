import os
import requests

def transfer_crypto(amount, bank_account):
    api_key = os.getenv('EXCHANGE_API_KEY')
    secret_key = os.getenv('EXCHANGE_SECRET_KEY')
    if not api_key or not secret_key:
        print("API key and Secret key must be provided via environment variables.")
        return

    # Placeholder URL and parameters; replace with actual API details
    url = 'https://api.exchange.com/v1/withdraw'
    params = {
        'api_key': api_key,
        'amount': amount,
        'bank_account': bank_account
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        print(f"Successfully transferred {amount} to bank account {bank_account}")
    else:
        print(f"Failed to transfer: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    transfer_crypto(10, 'your_bank_account')
