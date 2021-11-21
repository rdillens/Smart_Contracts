import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

st.title("NFT Browser")
st.write("Choose an account")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")


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
# total_supply = contract.functions.totalSupply().transact({'from': address, "gas": 1000000})

token_list = range(contract.functions.balanceOf(address).call())
token_selected = st.selectbox("Token ID", token_list)
# st.write(contract.functions.balanceOf(address).call())
token_address = contract.functions.tokenOfOwnerByIndex(address, token_selected).call()
token_uri = contract.functions.tokenURI(token_address).call()
# st.write(token_address)
# st.write(token_uri)
url_prefix = "https://ipfs.io/ipfs/"
url= url_prefix + f"{token_uri[7:]}"
# st.markdown(f"[Artwork IPFS Gateway Link]({url})")
resp = requests.get(url).content
parsed_resp = json.loads(resp)
# st.write(resp)
# st.write(parsed_resp)
# st.write(parsed_resp['image'])
image_url = url_prefix + parsed_resp['image']
# st.write(image_url)
st.image(requests.get(image_url).content)
