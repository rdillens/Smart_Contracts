# Art NFT Marketplace
![](https://i.guim.co.uk/img/media/8ff0a1b159384d1c849f1b74a17d63f5b4e2a716/0_539_4000_2400/master/4000.jpg?width=620&quality=85&auto=format&fit=max&s=e338f8a728f6975789d6ea84c3a96dd9)

# Description
A decentralized application (dApp) is an application built on a decentralized network that combines a smart contract and a frontend user interface. On Ethereum, smart contracts are accessible and transparent – like open APIs – so your dApp can even include a smart contract that someone else has written.

This project demonstrates how to build decentralized applications (dApps) and decentralized storage for non-fungible token (NFT) contracts.  We do this by building our (dApp) smart contract on the the ERC-721 Non-Fungible Token Standard defined in the Ethereum Improvement Proposal (EIP)–721.

We use this ERC-721 Non-Fungible Token Standard contract to demostrate how users can buy or sell artwork NFTs in a decentralized marketplace. Users are able to select their accounts and register new artwork tokens through a web interface. Users will also be able to display the tokens for their accounts so that they can display the artwork on the webpage.


# Initial SetUp

### Prerequisites

- [Git](https://git-scm.com/downloads) 
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remix-Etherium IDE](https://remix.ethereum.org/) 
- [Ganace](https://www.trufflesuite.com/ganache/)
- [Metamask](https://metamask.io/)
- [Pinata (Create a Token)](https://www.pinata.cloud/)

### Clone
Clone a copy of the repo:

```bash
git clone https://github.com/rdillens/Smart_Contracts.git
```

Change to the SDK's directory:

```bash
cd Smart_Contracts
```

### Create virtual environment: 

Create new environment in conde with depenencies:

```bash
conda create  --name SmartContracts_env python=3.7 --file requirements.txt
```
# Getting Started

## Step 1: Run Ganache

Choose Quickstart

![](/images/ganache-quickstart.PNG)


Ganache provides a local development blockchain for our app.

![](/images/ganache-open.PNG)

## Step 2: Open Remix
![Open Remix](/images/remix-open.PNG)


## Step 3: Import Repo Into Remix using dGit

## Step 4: Deploy Contract 

## Step 5: Copy Contract Address Into .env File

## Step 6: Copy Ganache URI to .env file
![](/images/ganache-open_rpc-server-highlighted.PNG)

Sample .env file that includes our app to use the WEB3 Provider to connect to our local block chain using the Ganache RPC Server URL


```bash
PINATA_API_KEY=
PINATA_SECRET_API_KEY=
WEB3_PROVIDER_URI=http://127.0.0.1:7545
SMART_CONTRACT_ADDRESS= [Address of Deployed Contract]
```


## Step 7:  Streamlit App

```bash
streamlit run app.py
```

## Contributors
- Chafic Charafeddine
- Remy Dillenseger
- Gregory Douglas
- Jose Medina