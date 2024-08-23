const ethers = require('ethers');

async function main() {
    const provider = new ethers.providers.JsonRpcProvider('your_rpc_url');
    const wallet = new ethers.Wallet('your_private_key', provider);

    const abi = [
        "constructor(uint256 _unlockTime)",
        "function release()",
        "function deposit() payable"
    ];
    const bytecode = 'your_bytecode';

    const factory = new ethers.ContractFactory(abi, bytecode, wallet);
    const unlockTime = Math.floor(Date.now() / 1000) + (365 * 24 * 60 * 60); // Unlock time: 1 year from now

    const contract = await factory.deploy(unlockTime);
    console.log(`Contract deployed at address: ${contract.address}`);
}

main().catch(console.error);
