import streamlit as st
from pathlib import Path
import shelve


shelf_path = './resources/shelf'


def check_for_shelf():
    if not Path(shelf_path).is_dir():
        Path(shelf_path).mkdir(parents=True, exist_ok=True)   


check_for_shelf()


def get_username():
    user_box = st.empty()
    with shelve.open(shelf_path + '/shelf') as sh:
        if 'username' in sh:
            username = sh['username']
        else:
            with user_box.container():
                with user_box.form("add_user_form", clear_on_submit=False):
                    username = st.text_input("Enter username")
                    user_submit = st.form_submit_button("Add User")
                    if user_submit:
                        sh['username'] = username
        user_box.header(f"Hello {sh['username']}!")
    return username


def create_env():
    key_string_list = []
    input_box = st.empty()
    with input_box.form(key="env_input_form", clear_on_submit=False):
        web3_provider = st.text_input(
            label="Web3 Provider", 
            value="HTTP://127.0.0.1:7545",
            help="Enter your Web3 provider here, copied from Ganache."
        )
        contract_address = st.text_input(
            label="Smart Contract Address", 
            help="Enter your smart contract address here, copied from the Remix IDE"
        )
        pinata_api_key = st.text_input(
            label="Pinata API Key", 
            help="Paste your API key here"
        )
        pinata_secret_api_key = st.text_input(
            label="Pinata Secret API Key", 
            help="Paste your Pinata API secret here"
        )

        key_submit = st.form_submit_button("Submit")
        if key_submit:
            key_string_list.append("WEB3_PROVIDER_URI="+web3_provider)
            key_string_list.append("SMART_CONTRACT_ADDRESS="+contract_address)
            key_string_list.append("PINATA_API_KEY="+pinata_api_key)
            key_string_list.append("PINATA_SECRET_API_KEY="+pinata_secret_api_key)
            with open('.env', 'a') as f:
                for key_str in key_string_list:
                    f.writelines(key_str+"\n")
            input_box.empty()

