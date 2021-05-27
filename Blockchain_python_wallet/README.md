**Background******

Your new startup is focusing on building a portfolio management system that supports not only traditional assets
like gold, silver, stocks, etc, but crypto-assets as well! The problem is, there are so many coins out there! It's
a good thing you understand how HD wallets work, since you'll need to build out a system that can create them.
You're in a race to get to the market. There aren't as many tools available in Python for this sort of thing, yet.
Thankfully, you've found a command line tool, hd-wallet-derive that supports not only BIP32, BIP39, and BIP44, but
also supports non-standard derivation paths for the most popular wallets out there today! However, you need to integrate
the script into your backend with your dear old friend, Python.
Once you've integrated this "universal" wallet, you can begin to manage billions of addresses across 300+ coins, giving
you a serious edge against the competition.
In this assignment, however, you will only need to get 2 coins working: Ethereum and Bitcoin Testnet.
Ethereum keys are the same format on any network, so the Ethereum keys should work with your custom networks or testnets.

**Dependencies: **
  PHP must be installed on your operating system.
  You will need to clone the hd-wallet-derive tool.
  bit Python Bitcoin library.
  web3.py Python Ethereum library.

Project setup
  - Created a project directory called **Blockchain_python_wallet** and cloned the hd-wallet-derive tool into this folder and install it using the HD Wallet Derive Installation Guide
  - Followed the instructions of Homework to do following 
  -   1. Setup constants
  -   2. Genreate a mnemonic  and BIP39   tool generate wallet addresses for BIT Coin network and Ethereum network
  -   3. Created Wallet.py and wallet.ipynb files to derive wallet keys. 
  -   4. Linking the transaction signing libraries - Using Bit and Web3.py created following 3 functions: 
          - priv_key_to_account: This function will convert the privkey string in a child key to an account object that bit or web3.py can use to transact.
          - create_tx: This function will create the raw, unsigned transaction that contains all metadata needed to transact.
          - send_tx : This function will call create_tx, sign the transaction, then send it to the designated network.
  -   5. Finally sent some transactions for BTCTEST coin and ETH coin. 
  -     Screen shots are saved on Screenshots folder as asked in HW. 
  -     
