// SPDX-License-Identifier: MIT
pragma solidity  ^0.8.20;

contract DeFi {

    constructor() {
        primaryOwner = msg.sender;
        //- TODO how to calculate interest rate?
        interestRate = 5;
    }

    address public primaryOwner;
    uint public interestRate;
    uint public fundAmount;
    

    mapping(address => FundOwner) public fundOwners;
    uint256 public ownerCount;

    mapping(address => Account) public accounts;
    uint256 public accountCount;

    event OwnerCreated(address key);
    event FundDeposit(address key, uint amount);

    event CustomerCreated(address key);
    event LoanIssued(address key, uint amount);
    event PaymentMade(address key, uint256 loanId, uint amount);

    modifier onlyPrimaryOwner() {
        require(msg.sender == primaryOwner, "You are not authorized to do this.");
        _;
    }

    modifier canOwnerWithdraw() {
        require(fundOwners[msg.sender].balance >= msg.value, "Your balance is too low to withdraw this amount.");
        _;
    }

    modifier canIssueLoan() {
        require((fundAmount-msg.value) >= 0, "Unable to issue loan.");
        require(accounts[msg.sender].balance == 0, "Account has a balance to pay.");
        _;
    }

    struct FundOwner {
        address key;
        uint balance;
        bool isActive;
        bool exists;
    }

    struct Loan {
        uint amount;
        uint interestRate;
        uint balance;
        bool isActive;
    }

    struct Account {
        address key;
        uint balance;
        uint256 lastPaymentDate;
        uint lastPaymentAmount;
        bool isActive;
        mapping(uint => Loan) loans;
        uint256 loanCount;
        //- No practical way to check if account already exists in mapping
        bool exists;
    }

    function makeDeposit() public payable {

        require(msg.value > 0, "Amount must be greater than zero.");
        require(address(msg.sender).balance >= msg.value, "Insufficient funds.");

        // Add the deposited amount to the fundAmount
        fundAmount += msg.value;

        // Check if the sender is already a fund owner; if not, initialize their account
        FundOwner storage fundOwner = fundOwners[msg.sender];
        if (!fundOwner.exists) {
            fundOwner.key = msg.sender;
            fundOwner.exists = true;
            ownerCount++;
            emit OwnerCreated(msg.sender);
        }
        fundOwner.isActive = true;
        fundOwner.balance += msg.value;

        emit FundDeposit(msg.sender, msg.value);

    }

    function getLoan(uint amount) public payable canIssueLoan {
        Account storage account = accounts[msg.sender];
        uint interest = (amount * interestRate) / 100;
        if (!account.exists) {
            account.key = msg.sender;
            account.exists = true;
            account.isActive = true;
            account.balance = amount + interest;
            account.loanCount = 1;
            accountCount++;
            emit CustomerCreated(msg.sender);
        } else {
            account.isActive = true;
            account.balance += amount + interest;
            account.loanCount++;
        }

        Loan storage newLoan = account.loans[account.loanCount];
        newLoan.amount = amount;
        newLoan.interestRate = interestRate;
        newLoan.balance = amount + interest;
        newLoan.isActive = true;

        emit LoanIssued(msg.sender, msg.value);
    }

    function makePayment(uint256 loanId, uint amount) public {
        Account storage account = accounts[msg.sender];
        Loan storage loan = account.loans[loanId];
        require(msg.sender == account.key, "Only the account holder can make payments");
        require(loan.balance > 0, "Loan is already paid off");
        require(amount <= loan.balance, "Cannot pay more than the loan balance");

        loan.balance -= amount;
        account.balance -= amount;
        account.lastPaymentDate = block.timestamp;
        account.lastPaymentAmount = amount;

        emit PaymentMade(msg.sender, loanId, amount);
    }

    // TODO create a cronjob with primaryOwner account to update the interest rate at interval
    function setInterestRate(uint _interestRate) public onlyPrimaryOwner {
        interestRate = _interestRate;
    }

}