
**Running POA Blockchain: **

To do this, you will create and submit four deliverables:

Set up your custom testnet blockchain: 
  1. Created Blockchain network- **poablkchain** using ./puppeth with proof of authority seclection
  2. Node3 & Node 4 were created. Node 3 was set to be minning Node.  

Aftger following the steps reccomended in Resources folder, test transaction was sent. 
The Nodes were added to MyCrypto (screenshots saved in Screenshots_(PoA) folder

Create a repository: Created POA_Blockchain repo 
**All the Screenshots are saved in ./Blockchain-Tools/Screenshots_(PoA) folder.**



******************* =================================== ***********************

** Steps followed to Set up and run Proof of Authority Blockchain: **

The Proof of Authority (PoA) algorithm is typically used for private blockchain networks as it requires pre-approval of, or voting in of, the account addresses that can approve transactions (seal blocks).

Because the accounts must be approved, we will generate two new nodes with new account addresses that will serve as our pre-approved sealer addresses.

Create accounts for two nodes for the network with a separate datadir for each using geth.
./geth --datadir node1 account new
./geth --datadir node2 account new

Next, generate your genesis block.

Run puppeth, name your network, and select the option to configure a new genesis block.
Choose the Clique (Proof of Authority) consensus algorithm.
Paste both account addresses from the first step one at a time into the list of accounts to seal.
Paste them again in the list of accounts to pre-fund. There are no block rewards in PoA, so you'll need to pre-fund.
You can choose no for pre-funding the pre-compiled accounts (0x1 .. 0xff) with wei. This keeps the genesis cleaner.
Complete the rest of the prompts, and when you are back at the main menu, choose the "Manage existing genesis" option.
Export genesis configurations. This will fail to create two of the files, but you only need networkname.json.

With the genesis block creation completed, we will now initialize the nodes with the genesis' json file.
Using geth, initialize each node with the new networkname.json.

./geth --datadir node1 init networkname.json
./geth --datadir node2 init networkname.json

Now the nodes can be used to begin mining blocks.
Run the nodes in separate terminal windows with the commands:
./geth --datadir node1 --unlock "SEALER_ONE_ADDRESS" --mine --rpc --allow-insecure-unlock
./geth --datadir node2 --unlock "SEALER_TWO_ADDRESS" --mine --port 30304 --bootnodes "enode://SEALER_ONE_ENODE_ADDRESS@127.0.0.1:30303" --ipcdisable --allow-insecure-unlock

NOTE: Type your password and hit enter - even if you can't see it visually!

Your private PoA blockchain should now be running!

With both nodes up and running, the blockchain can be added to MyCrypto for testing.

All the Screenshots are saved in ./Blockchain-Tools/Screenshots_(PoA) folder.
