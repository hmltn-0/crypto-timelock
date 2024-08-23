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
