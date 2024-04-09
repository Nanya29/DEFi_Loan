import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
#from streamlit_extras.app_logo import add_logo

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
abi_path = Path('./contracts/compiled/certificate_abi.json')
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")


# Cache the contract on load
@st.cache_resource()
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with abi_path.open() as f:
        certificate_abi = json.load(f)    

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )

    # Return the contract from the function
    return contract
   
    

# Write welcome messgae
st.markdown("# LOAN SUMMARY")


# Load the contract
contract = load_contract()

st.markdown(f"**Lending Pool Amount in Wei**: {contract.functions.fundAmount().call()}")

st.markdown(f"**Contract Primary Owner**: {contract.functions.primaryOwner.address}")
st.markdown(f"**Contract Address**: {contract.functions.address}")

st.markdown(f"**Number of Owners**: {contract.functions.ownerCount().call()}")

st.markdown(f"**Number of Accounts**: {contract.functions.accountCount().call()}")

# Accounts
network_accounts = w3.eth.accounts
accountId = st.selectbox("Select a Network Address", options=network_accounts)

st.write(accountId)

if st.button('Is address a customer?'):
    account_data = contract.functions.accounts(accountId).call()
    st.markdown(f"**Addresss**: {account_data[0]}")
    st.markdown(f"**Balance**: {account_data[1]}")
    st.markdown(f"**Last Payment Date**: {account_data[2]}")
    st.markdown(f"**Last Payment Amount**: {account_data[3]}")
    st.markdown(f"**Is Active**: {account_data[4]}")
    st.markdown(f"**Loan Count**: {account_data[5]}")

if st.button('Is address an owner?'):
    owner_data = contract.functions.fundOwners(accountId).call()
    st.markdown(f"**Addresss**: {owner_data[0]}")
    st.markdown(f"**Balance**: {owner_data[1]}")
    st.markdown(f"**Is Active**: {owner_data[2]}")



# Subject to change after loan is disbursed
st.sidebar.markdown("## Account Balance")
#st.write(Account.balance)

# Create an input field to record the loan amount
loan_amt = st.sidebar.number_input("Loan Amount")

# Create an input field to record the fee amount
fee_amt = loan_amt * 0.03
st.sidebar.markdown("Fee Amount")
st.sidebar.write(fee_amt)

#create an input field for repay Amount
st.sidebar.markdown("## Total Amount Due ")
repay_amt= loan_amt+ fee_amt
st.sidebar.write("Due Amount", repay_amt)


#create Deposit button
if st.sidebar.button("makeDeposit"):
    # Transacton = contract.functions.makeDeposit(msg.value, msg.sender)
    st.balloons()
    
# ConnectionAbortedError