# Crypto Timelock

This project enables automated cryptocurrency purchases and fund lock-up using a smart contract.

## Setup

### Dependencies

Install the necessary dependencies:

```sh
pip install -r requirements.txt
npm install ethers
```

### Smart Contract

Deploy the smart contract:

1. Compile `Timelock.sol` using Remix, Truffle, or Hardhat.
2. Deploy the compiled contract to the Ethereum network with `deploy.js`.

### Environment Variables

Set up your environment variables for API keys:

```sh
export BINANCE_API_KEY="your_api_key"
export BINANCE_SECRET_KEY="your_secret_key"
export EXCHANGE_API_KEY="your_exchange_api_key"
export EXCHANGE_SECRET_KEY="your_exchange_secret_key"
```

### Running Scripts

Automate cryptocurrency purchases and transfers.

```sh
python scripts/buy_crypto.py
python scripts/transfer_crypto.py
```

## Testing

To run tests:

```sh
python -m unittest discover -s tests
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

MIT License

## Example Usage

The following example demonstrates how to use the Timelock smart contract and related scripts:

1. Deploy the `Timelock.sol` contract to your preferred Ethereum network.
2. Use `deploy.js` to deploy the contract and get the contract address.
3. Send cryptocurrency to the smart contract using the `deposit` function.
4. Purchase cryptocurrency using `buy_crypto.py`.
5. Transfer profits using `transfer_crypto.py`.

For detailed instructions and guidelines, please refer to the documentation and examples provided in the repository.
