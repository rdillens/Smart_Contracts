import os
import streamlit as st
from streamlit_pages.streamlit_pages import MultiPage
from pathlib import Path
from dotenv import load_dotenv
import json
from web3 import Web3
import shelve
import utils.helper_functions as hf
import requests
from utils.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open(Path('./contracts/compiled/artregistry_abi.json')) as f:
        contract_abi = json.load(f)
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract


def register():
    st.markdown("## Register New Artwork")
    artwork_name = st.text_input("Enter the name of the artwork")
    artist_name = st.text_input("Enter the artist name")
    initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
    file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
    if st.button("Register Artwork"):
        # Use the `pin_artwork` helper function to pin the file to IPFS
        artwork_ipfs_hash =  hf.pin_artwork(artwork_name, file)
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"
        tx_hash = contract.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            int(initial_appraisal_value),
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.markdown("---")


def appraise():
    st.markdown("## Appraise Artwork")
    tokens = contract.functions.totalSupply().call()
    token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
    new_appraisal_value = st.text_input("Enter the new appraisal amount")
    appraisal_report_content = st.text_area("Enter details for the Appraisal Report")
    if st.button("Appraise Artwork"):

        # Use the `pin_appraisal_report` helper function
        # to pin an appraisal report for the report URI
        appraisal_report_ipfs_hash =  hf.pin_appraisal_report(appraisal_report_content)
        report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

        # Use the token_id and the report_uri to record the appraisal
        tx_hash = contract.functions.newAppraisal(
            token_id,
            int(new_appraisal_value),
            report_uri
        ).transact({"from": w3.eth.accounts[0]})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(receipt)
    st.markdown("---")


def exchange():
    st.markdown("## Exchange")
    for token_id in range(contract.functions.totalSupply().call()):
        try:
            st.write(f"Token ID: {token_id}")
            token_uri = contract.functions.tokenURI(token_id).call()
            st.image(get_ipfs_image(token_uri))
        except AttributeError:
            pass    
        
    if st.button("Purchase"):
        st.write("Purchase is currently not avaliable")


def get_ipfs_image(token_uri):
    url_prefix = "https://ipfs.io/ipfs/"
    url= url_prefix + f"{token_uri[7:]}"
    resp = requests.get(url).content
    parsed_resp = json.loads(resp)
    image_url = url_prefix + parsed_resp['image']
    return requests.get(image_url).content

def browse():
    token_selected = st.selectbox("Token ID", range(contract.functions.balanceOf(address).call()))
    try:
        token_address = contract.functions.tokenOfOwnerByIndex(address, token_selected).call()
        token_uri = contract.functions.tokenURI(token_address).call()
        url_prefix = "https://ipfs.io/ipfs/"
        url= url_prefix + f"{token_uri[7:]}"
        resp = requests.get(url).content
        parsed_resp = json.loads(resp)
    except:
        pass
    else:
        image_url = url_prefix + parsed_resp['image']
        st.image(requests.get(image_url).content)

if __name__ == "__main__":
    # Define and connect a new Web3 provider
    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

    # Load the contract
    contract = load_contract()
    st.title("Art Registry Appraisal System")

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
    app.add_page("Collection", browse)
    app.add_page("Register Artwork", register)
    app.add_page("Appraise", appraise)
    app.add_page("Exchange", exchange)
    # Run the multipage app
    app.run()