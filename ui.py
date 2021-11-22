import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import json
from web3 import Web3
import shelve
import utils.helper_functions as hf
from utils.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


def run():
    # Define and connect a new Web3 provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

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


    # Load the contract
    contract = load_contract()
    st.title("Art Registry Appraisal System")
    accounts = w3.eth.accounts
    address = st.sidebar.selectbox(
        label="Account", 
        options=accounts,
        help="Select a wallet address associated with your account",
    )
    st.write(f"{contract} \n {address}")


if __name__ == "__main__":
    load_dotenv()
    username = hf.get_username()
    if not Path('.env').is_file():
        hf.create_env()
    run()
