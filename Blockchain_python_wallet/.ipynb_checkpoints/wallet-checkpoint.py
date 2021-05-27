# Import dependencies
import subprocess
import json
from decimal import Decimal
from dotenv import load_dotenv
import os
import bit
from bit import wif_to_key
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

import warnings
warnings.filterwarnings("ignore")

# Load and set environment variables
load_dotenv("api_keys.env")
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Create a function called `derive_wallets`
def derive_wallets(coin, mnemonic, numderive, cols="address,index,path,privkey,pubkey"):
    
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols={cols} --coin={coin} --numderive={numderive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {ETH: derive_wallets(coin=ETH, mnemonic=mnemonic, numderive=3),
         BTCTEST: derive_wallets(coin=BTCTEST, mnemonic=mnemonic, numderive=3)}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    #print(priv_key)
    if coin.upper() == 'ETH':
        account =  Account.from_key(priv_key)
    elif coin.upper() == 'BTCTEST':
        account = wif_to_key(priv_key)
        print(account)
        
    return account
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recepient, amount):
    ## Transform the amount from Ether to wei
        
    if coin == ETH: 
        ## estimating Gas fees
        amount = w3.toWei(Decimal(amount), 'ether')
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recepient, "value": amount}
        )
        
        return {
            "from": account.address,
            "to": recepient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId": 1943 # Add to the instructions
        }
    
    elif coin.upper() == 'BTCTEST':
        print(account.prepare_transaction(account.address, [(recepient, amount, BTC)]))
        return account.prepare_transaction(account.address, [(recepient, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recepient, amount):
    tx = create_tx(coin, account, recepient, amount)
    print(tx)
    if coin.upper() == 'ETH':
        signed_tx = account.sign_transaction(tx)
        print(signed_tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
        return result
    elif coin.upper() == 'BTCTEST':
        signed_tx = account.sign_transaction(tx)
        result = bit.network.NetworkAPI.broadcast_tx_testnet(signed_tx)
        return result

    

