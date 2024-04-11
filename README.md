# DeFi - Lending Pool & Flash Loan

This project, led by Ayman Alklaqe, Princess Nwabulu, and Evan Grillo, explores decentralized finance (DeFi) through the creation of a lending pool and implementation of flash loans.

## Technologies

The project leverages various technologies including:

- Remix
- Ganache
- Solidity
- Python
- Streamlit
- Web3
- FlashLoanLib

## Summary

Continuing our exploration of blockchain and smart contracts with Solidity, we've developed a contract enabling users to contribute to and borrow from a lending pool. Additionally, we've integrated this contract with a Streamlit app and introduced a Flash Loan contract for executing arbitrage trades.

## Concept

This project serves as an illustration of how smart contracts can facilitate transactions in the decentralized finance landscape.

## Steps To Run The Flash Loan

1) Compile the flash loan and defi contracts.

2) In the "value" section, fund the MockDex contract with ETH. EX: 3eth. This is the amount the exchange will have. Set the token price to 1000000000000000,

3) Do the same as step 2 but set the toke price to 1200000000000000. Now you will have 2 MockDex contracts deployed.

4) Deploy the defi.sol contract.

5) In the "value" section enter an amount you want deposit, and in the defi contract, make a deposit using the "makeDeposit" function (This will be used as liquidity).

6) In the defi.sol contract, using the "flashLoan" function, enter the loan amount you want, and copy and paste the smart contract addresses of both dex's from steps 2 and 3 and click "transact".



## Next Steps

Transition to a Sepolia testnet and import a commercial-grade contract to further enhance the capabilities and robustness of the contract and trading features.
