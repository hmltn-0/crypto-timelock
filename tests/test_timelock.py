import unittest
from web3 import Web3

class TestTimeLock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup blockchain connection, deploy contract, etc.
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
        cls.unlock_time = int(time.time()) + 60  # Unlock time: 1 minute from now
        tx_hash = TimeLock.constructor(cls.unlock_time).transact()
        tx_receipt = cls.web3.eth.wait_for_transaction_receipt(tx_hash)
        cls.contract = cls.web3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )

    def test_unlock_time(self):
        self.assertEqual(self.contract.functions.unlockTime().call(), self.unlock_time)

    def test_deposit_and_release(self):
        self.contract.functions.deposit().transact({'from': self.web3.eth.accounts[0], 'value': self.web3.toWei(1, 'ether')})
        with self.assertRaises(Exception):
            self.contract.functions.release().transact()

        self.web3.provider.make_request("evm_increaseTime", [61])
        self.web3.provider.make_request("evm_mine", [])
        self.contract.functions.release().transact()

if __name__ == '__main__':
    unittest.main()
