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
