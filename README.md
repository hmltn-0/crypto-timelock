# Crypto TimeLock

## Overview
Crypto TimeLock is an application designed to automate cryptocurrency purchases and manage funds using smart contracts and exchange APIs like Kraken. It allows users to lock their cryptocurrency until a specified unlock time, after which the funds can be automatically transferred or accessed.

## Repository Structure
```
crypto-timelock/
├── contracts/
│   └── TimeLock.sol                 # Smart contract for Ethereum
├── scripts/
│   ├── buy_crypto.py                # Script to automate cryptocurrency purchases
│   ├── transfer_crypto.py           # Script to automate the transfer process
│   └── test_credentials.py          # Script to test API credentials
├── tests/
│   └── test_timelock.py             # Test suite for the smart contract
├── README.md                        # Documentation
├── requirements.txt                 # Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions for CI/CD
├── LICENSE                          # License file for the project
└── .gitignore                       # Git ignore file
```

## Detailed Documentation

### Smart Contract: TimeLock.sol
This Solidity contract is designed to lock funds until a specified unlock time. Here’s a breakdown of its components:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLock {
    address public owner;
    uint256 public unlockTime;

    constructor(uint256 _unlockTime) {
        require(_unlockTime > block.timestamp, "Unlock time should be in the future");
        owner = msg.sender;
        unlockTime = _unlockTime;
    }

    function release() public {
        require(block.timestamp >= unlockTime, "Current time is before unlock time");
        require(msg.sender == owner, "Caller is not the owner");
        payable(owner).transfer(address(this).balance);
    }

    function deposit() public payable {}
}
```
The contract has:
- `owner`: Address of the contract deployer.
- `unlockTime`: Time when funds can be released.
- `constructor`: Sets the unlock time and owner.
- `release`: Allows the owner to release funds if the current time is past the unlock time.
- `deposit`: Enables the owner to deposit funds into the contract.

### Scripts
#### buy_crypto.py
Automates cryptocurrency purchases using Kraken API.
```python
import os
import requests
import time
import hmac
import hashlib

def buy_crypto(api_key, secret_key, amount, pair):
    url = 'https://api.kraken.com/0/private/AddOrder'
    nonce = str(int(1000 * time.time()))
    body = {
        'nonce': nonce,
        'ordertype': 'market',
        'type': 'buy',
        'volume': amount,
        'pair': pair
    }
    post_data = '&'.join([f"{k}={v}" for k, v in body.items()])
    data = '/0/private/AddOrder' + hashlib.sha256(nonce.encode() + post_data.encode()).digest()
    signature = hmac.new(base64.b64decode(secret_key), data, hashlib.sha512).digest()
    headers = {
        'API-Key': api_key,
        'API-Sign': base64.b64encode(signature).decode()
    }

    response = requests.post(url, headers=headers, data=body)
    print(response.json())

if __name__ == "__main__":
    api_key = os.getenv('KRAKEN_API_KEY')
    secret_key = os.getenv('KRAKEN_SECRET_KEY')
    if api_key and secret_key:
        buy_crypto(api_key, secret_key, '0.001', 'XXBTZUSD')
    else:
        print("API key and Secret key must be set in environment variables.")
```

#### transfer_crypto.py
Automates the transfer of cryptocurrency profits back to a bank account using Kraken API.
```python
import os
import requests
import time
import hmac
import hashlib

def transfer_crypto(api_key, secret_key, amount, address):
    url = 'https://api.kraken.com/0/private/Withdraw'
    nonce = str(int(1000 * time.time()))
    body = {
        'nonce': nonce,
        'asset': 'XBT',
        'key': address,
        'amount': amount
    }
    post_data = '&'.join([f"{k}={v}" for k, v in body.items()])
    data = '/0/private/Withdraw' + hashlib.sha256(nonce.encode() + post_data.encode()).digest()
    signature = hmac.new(base64.b64decode(secret_key), data, hashlib.sha512).digest()
    headers = {
        'API-Key': api_key,
        'API-Sign': base64.b64encode(signature).decode()
    }

    response = requests.post(url, headers=headers, data=body)
    print(response.json())

if __name__ == "__main__":
    api_key = os.getenv('KRAKEN_API_KEY')
    secret_key = os.getenv('KRAKEN_SECRET_KEY')
    address = os.getenv('WITHDRAW_ADDRESS')
    if api_key and secret_key and address:
        transfer_crypto(api_key, secret_key, 10, address)
    else:
        print("API key, Secret key, and Withdraw address must be set in environment variables.")
```

#### test_credentials.py
Verifies the API credentials for Kraken.
```python
import os
import requests
import time
import hmac
import hashlib

def verify_kraken_credentials(api_key, secret_key):
    url = 'https://api.kraken.com/0/private/Balance'
    nonce = str(int(1000*time.time()))
    body = {
        'nonce': nonce,
    }
    post_data = '&'.join([f"{k}={v}" for k, v in body.items()])
    data = '/0/private/Balance' + hashlib.sha256(nonce.encode() + post_data.encode()).digest()
    signature = hmac.new(base64.b64decode(secret_key), data, hashlib.sha512).digest()
    headers = {
        'API-Key': api_key,
        'API-Sign': base64.b64encode(signature).decode()
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}. Ensure your API key details are correct, and the key has the necessary permissions.")

if __name__ == "__main__":
    api_key = os.getenv('KRAKEN_API_KEY')
    secret_key = os.getenv('KRAKEN_SECRET_KEY')
    if api_key and secret_key:
        verify_kraken_credentials(api_key, secret_key)
    else:
        print("API key and Secret key must be set in environment variables.")
```

### Tests
The test suite in `tests/test_timelock.py` verifies the functionality of the smart contract.
```python
import unittest
import time
from web3 import Web3
from solcx import compile_source, set_solc_version

class TestTimeLock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_solc_version("0.8.0")
        cls.web3 = Web3(Web3.EthereumTesterProvider())
        cls.web3.eth.default_account = cls.web3.eth.accounts[0]
        compiled_sol = compile_source('''
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;
        contract TimeLock {
            address public owner;
            uint256 public unlockTime;
            constructor(uint256 _unlockTime) {
                require(_unlockTime > block.timestamp, "Unlock time should be in the future");
                owner = msg.sender;
                unlockTime = _unlockTime;
            }
            function release() public {
                require(block.timestamp >= unlockTime, "Current time is before unlock time");
                require(msg.sender == owner, "Caller is not the owner");
                payable(owner).transfer(address(this).balance);
            }
            function deposit() public payable {}
        }
        ''')
        contract_interface = compiled_sol['<stdin>:TimeLock']
        TimeLock = cls.web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        cls.unlock_time = int(time.time()) + 60
        tx_hash = TimeLock.constructor(cls.unlock_time).transact()
        tx_receipt = cls.web3.eth.wait_for_transaction_receipt(tx_hash)
        cls.contract = cls.web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )
        cls.snapshot_id = cls.web3.testing.snapshot()
    @classmethod
    def tearDownClass(cls):
        cls.web3.testing.revert(cls.snapshot_id)
    def test_unlock_time(self):
        self.assertEqual(self.contract.functions.unlockTime().call(), self.unlock_time)
    def test_deposit_and_release(self):
        self.contract.functions.deposit().transact({'from': self.web3.eth.accounts[0], 'value': self.web3.to_wei(1, 'ether')})
        with self.assertRaises(Exception):
            self.contract.functions.release().transact()
        self.web3.provider.make_request("evm_increaseTime", [10000])
        self.web3.provider.make_request("evm_mine", [])
        while self.web3.eth.get_block('latest')['timestamp'] < self.unlock_time:
            self.web3.provider.make_request("evm_mine", [])
        self.contract.functions.release().transact()

if __name__ == '__main__':
    unittest.main()
```

### Roadmap
1. **API Integration**: Ensure the integration works flawlessly with the supported exchange APIs.
2. **Security Audits**: Perform thorough security audits of the smart contract and scripts.
3. **Edge Case Handling**: Extend test cases to cover various edge scenarios.
4. **User Interface**: Consider adding a user interface to manage and monitor cryptocurrency investments.
5. **Community Engagement**: Engage with the community for feedback and contributions.

### Current State of Development
The Crypto TimeLock project is in an intermediate stage of development. The main functionality is implemented and tested. Further refinements and enhancements are planned, focusing on security and user experience.

### Next Steps
- Integrate the real API calls with validation checks.
- Perform testing using real accounts and scenarios.
- Gather feedback from early users.
- Implement additional features based on the roadmap.

## Conclusion
The Crypto TimeLock project aims to provide a reliable solution for managing cryptocurrency investments with automated scripts and smart contracts. This documentation intends to assist new developers in understanding and contributing to the project.

For further assistance, please raise a GitHub issue or contact project maintainers.

### License
This project is licensed under the MIT License.
