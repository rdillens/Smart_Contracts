import os
import streamlit as st
from streamlit_pages.streamlit_pages import MultiPage
from pathlib import Path
from dotenv import load_dotenv
import json
from web3 import Web3
import shelve
import utils.helper_functions as hf
from utils.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open(Path('./contracts/compiled/artregistry_abi_ipfs.json')) as f:
        contract_abi = json.load(f)
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract


def home():
    st.write(f"{contract} \n {address}")


def about():
    st.write("Welcome to about page")
    if st.button("Click about"):
        st.write("Welcome to About page")


def contact():
    st.write("Welcome to contact page")
    if st.button("Click Contact"):
        st.write("Welcome to contact page")


if __name__ == "__main__":
    # Check that shelf file exists, if not it is created
    hf.check_for_shelf()
    # Define and connect a new Web3 provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

    # Load the contract
    contract = load_contract()
    st.title("Art Registry Appraisal System")

    # Get username
    username = hf.get_username()
    st.sidebar.header(f"Hello {username}!")

    # Account address sidebar selectbox
    accounts = w3.eth.accounts
    address = st.sidebar.selectbox(
        label="Account", 
        options=accounts,
        help="Select a wallet address associated with your account",
    )


    # Define the multipage app
    app = MultiPage()
    # Add pages to the app
    app.add_page("Home",home)
    app.add_page("About",about)
    app.add_page("Contact",contact)
    # Run the multipage app
    app.run()