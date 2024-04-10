import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
import math

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

# Load the contract
contract = load_contract()

tab1, tab2, tab3 = st.tabs(["Account View", "Status", "Actions", ])

# Accounts
network_accounts = w3.eth.accounts
with tab1:
    st.markdown("# Account View")
    st.divider()
    Account_list= ("0x13defbfBd9a110e13B35e1f6596819244A129012", "0x2F77D271ce43ad0ADdE0992450fE73734e11169E")
    accountId = st.selectbox("Select a Account", Account_list)

    st.markdown(f"**Account Selected**: {accountId}")

    # Get Account Balance
    balance_wei = w3.eth.get_balance(accountId)
    balance_ether = w3.from_wei(balance_wei, 'ether')
    st.markdown(f"**Total Ether**: {round(balance_ether, 2)}")
    st.markdown(f"**Amount Contributed to Lending Pool**: {w3.from_wei(contract.functions.fundOwners(accountId).call()[1], 'ether')} ETH")
    st.markdown(f"**Amount Owed to Lending Pool**: {contract.functions.accounts(accountId).call()[1]} ETH")
    

with tab2:
    st.markdown(f"### Loan Stats")
    account_data = contract.functions.accounts(accountId).call()
    # st.markdown(f"**Addresss**: {account_data[0]}")
    # st.markdown(f"**Balance**: {account_data[1]}")
    # Function to get current timestamp
    def get_current_timestamp():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    st.markdown(f"**Last Payment Date**: {get_current_timestamp()}")
    payment_amount= st.markdown(f"**Last Payment Amount**: {w3.from_wei(account_data[3], 'ether')} ETH")
    st.markdown(f"**Is Active**: {account_data[4]}")
    st.markdown(f"**Loan Count**: {account_data[5]}")
    st.divider()

    st.markdown(f"### Pool Stats")
    owner_data = contract.functions.fundOwners(accountId).call()
    st.markdown(f"**Addresss**: {owner_data[0]}")
    st.markdown(f"**Balance**: {owner_data[1]}")
    st.markdown(f"**Is Active**: {owner_data[2]}")
    

with tab3:
    st.markdown(f"# Actions")

    #create Deposit button
    deposit_amount = st.number_input("Enter the amount of ETH to deposit:", min_value=0.01)
    if st.button("Deposit ETH"):
        wei_amount = w3.to_wei(deposit_amount, 'ether')
        from_account = accountId
        private_key = os.getenv(accountId)
        tx = contract.functions.makeDeposit().build_transaction({
            'from': from_account,
            'value': wei_amount,
            'nonce': w3.eth.get_transaction_count(from_account),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price
        })
        st.success(f"Deposit made! ")
        st.balloons()

    loan_amount = st.number_input("Enter the amount of ETH to Borrow:", min_value=0.01)
    if st.button('Get Loan'):
        try: 
            wei_amount = w3.to_wei(loan_amount, 'ether')
            from_account = accountId
            private_key = os.getenv(accountId)
            tx = contract.functions.getLoan(wei_amount).build_transaction({
                'from': from_account,
                'value': wei_amount,
                'nonce': w3.eth.get_transaction_count(from_account),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price
            })
            st.success(f"Deposit made! ")
            st.balloons()
        except Exception as e:
            st.error(str(e))

    pay_amount = st.number_input("Enter an ETH Payment Amount:", min_value=0.01)
    if st.button('Pay off Loan'):
        try: 
            wei_amount = w3.to_wei(pay_amount, 'ether')
            from_account = accountId
            private_key = os.getenv(accountId)
            tx = contract.functions.makePayment(account_data[5], wei_amount).build_transaction({
                'from': from_account,
                'nonce': w3.eth.get_transaction_count(from_account),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price
            })
            #signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            #tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            #st.success(f"Payment made. Transaction hash: {tx_hash.hex()}")
            timestamp = get_current_timestamp()
            payment_amount.markdown(f"**Last Payment Amount**: {pay_amount} ETH")
            st.success(f"You have paid off: {pay_amount} Ether")
            st.balloons()
        except Exception as e:
            st.error(str(e))


# Contract Stats
st.sidebar.markdown(f"# Contract Stats")
st.sidebar.markdown(f"**Lending Pool Amount in ETH**: {w3.from_wei(contract.functions.fundAmount().call(), 'ether')}")
st.sidebar.markdown(f"**Current Gas Price**: {w3.eth.gas_price}")
st.sidebar.markdown(f"**Contract Primary Owner**: {contract.functions.primaryOwner.address}")
st.sidebar.markdown(f"**Contract Address**: {contract.functions.address}")
st.sidebar.markdown(f"**Number of Owners**: {contract.functions.ownerCount().call()}")
st.sidebar.markdown(f"**Number of Accounts**: {contract.functions.accountCount().call()}")