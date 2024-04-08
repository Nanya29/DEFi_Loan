// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IDex {
    function buyToken(uint256 tokensToBuy) external payable;
    function sellToken(
        uint256 amount,
        address payable _seller
    ) external returns (uint256 totalProceeds);
    function getTokenPrice() external view returns (uint256);
}

contract MockDex {
    uint tokenPrice; // Token price in wei
    uint totalTokens = 1000000000; // Amount of tokens held by DEX

    event TokenBought(address indexed buyer, uint256 tokenCount);
    event TokenSold(address indexed seller, uint256 tokenCount);

    constructor(uint256 _tokenPrice) payable {
        tokenPrice = _tokenPrice;
    }

    function buyToken(uint256 tokensToBuy) external payable {
        require(msg.value > 0, "Invalid purchase amount");

        // Update the token balance
        totalTokens -= tokensToBuy;

        // Emit an event to indicate the token purchase
        emit TokenBought(msg.sender, tokensToBuy);
    }

    function sellToken(
        uint256 tokensToSell,
        address payable _seller
    ) external returns (uint256 totalProceeds) {
        require(tokensToSell > 0, "Invalid sale amount");
        require(totalTokens >= tokensToSell, "Insufficient token balance");

        // Calculate the sale proceeds based on the token price
        uint256 saleProceeds = tokensToSell * tokenPrice;

        // Update the token balance
        totalTokens += tokensToSell;

        // Transfer the sale proceeds to the seller
        (bool success, ) = _seller.call{value: saleProceeds}("");
        require(success, "Failed to transfer proceeds to seller");

        // Emit an event to indicate the token sale
        emit TokenSold(_seller, tokensToSell);

        return saleProceeds;
    }

    function getTokenPrice() external view returns (uint256) {
        return tokenPrice;
    }
}

// Dex funding 3eth: 3000000000000000000
// DexA token price 0.0010eth: 1000000000000000
// DexB token price 0.0012eth: 1200000000000000
// Contract funding 2eth: 2000000000000000000
// Loan amount 1eth: 1000000000000000000
