# Crypto Timelock

This project enables automated cryptocurrency purchases and fund lock-up using a smart contract.

## Setup

### Dependencies

Install the necessary dependencies:

\`\`\`sh
pip install -r requirements.txt
npm install ethers
\`\`\`

### Smart Contract

Deploy the smart contract:

1. Compile \`Timelock.sol\` using Remix, Truffle, or Hardhat.
2. Deploy the compiled contract to the Ethereum network with \`deploy.js\`.

### Running Scripts

Automate cryptocurrency purchases and transfers.

\`\`\`sh
python scripts/buy_crypto.py
python scripts/transfer_crypto.py
\`\`\`

## Testing

To run tests:

\`\`\`sh
python -m unittest discover -s tests
\`\`\`

## License

MIT License
