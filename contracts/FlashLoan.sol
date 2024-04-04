// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";

//- From Medium article: https://medium.com/coinmonks/21dayssoliditychallenge-day-12-flash-loans-unleashed-building-your-own-flash-loan-contract-bdbe760931a3
contract FlashLoanContract {

    address public owner;
    IERC20 public dai; // The DAI token contract

    constructor(address _daiAddress) {
        owner = msg.sender;
        dai = IERC20(_daiAddress);
    }
    function flashLoan(uint256 amount) view  external {
        require(msg.sender == owner, "Only the contract owner can initiate a flash loan");
        uint256 balanceBefore = dai.balanceOf(address(this));
        require(balanceBefore >= amount, "Not enough DAI in the contract");
        // Execute custom logic here (e.g., arbitrage, liquidation)
        uint256 balanceAfter = dai.balanceOf(address(this));
        require(balanceAfter >= balanceBefore, "Flash loan repayment failed");
    }
}


// still testing

// Created an ERC2020 token

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken","MTK") {
        _mint(msg.sender, initialSupply);
    }
}

// start of the flashLoan

contract flashLoans  {

    MyToken public token;

    constructor(address tokenAddress) {
        token = MyToken(tokenAddress);
    }

    function executeFlashLoans(uint256 amount) external {
        
        // We will just transfer the tokens back to the contract
        token.transferFrom(msg.sender, address(this), amount);

        // Perform arbitrage logic here.

        // repay the loan
        token.transfer(msg.sender, amount);

        // emit an event to signal completion of the flash laon
    }
}