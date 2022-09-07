from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()


with open("./SmartContractPrac.sol", "r") as file:
    smartContract= file.read()

compiled_sol= compile_standard(
    {
        "language":"Solidity",
        "sources":{"SmartContractPrac.sol":{"content":smartContract}},
        "settings":{"outputSelection":{
            "*":{
                "*":["abi","metadata","evm.bytecode","evm.sourceMap"]
            }
        }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_SmartContract.json", "w") as file:
    json.dump(compiled_sol, file)

# made the compiled smartContract... 
bytecode= compiled_sol["contracts"]["SmartContractPrac.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi= compiled_sol["contracts"]["SmartContractPrac.sol"]["SimpleStorage"]["abi"]

# connection block...
# FOR ganache gui
# w3= Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# chain_Id= 1337
# my_address= "0x496c1469e78342a86b92fEff0c6fAcfAaC5d957A"
# private_key= os.getenv("PRIVATE_KEY")
# FOR testnet
w3= Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/f70414b7e92847879e71d560763840bc"))
chain_Id= 4
my_address= "0x3A41745999ad4D2c4F62e006E744Dea5CFFc1415"
private_key= os.getenv("PRIVATE_KEY_RINKEBY")

# 2lines -making smartContract from holi ritual n nonce
smart_contract= w3.eth.contract(abi= abi, bytecode= bytecode)
nonce= w3.eth.getTransactionCount(my_address)

# build transaction
# sign transaction
# send transaction
# wait transaction
txn1= smart_contract.constructor().buildTransaction(
    {
    "from":my_address, "nonce":nonce, "chainId":chain_Id, 
    "gas": 1728712, "gasPrice": w3.toWei("21","gwei")
    }
)

sign_txn= w3.eth.account.sign_transaction(txn1, private_key= private_key)
sndTxn= w3.eth.send_raw_transaction(sign_txn.rawTransaction)
txnReceipt= w3.eth.wait_for_transaction_receipt(sndTxn)

# interact with on-chain smart contract
onChainContract= w3.eth.contract(address= txnReceipt.contractAddress, abi=abi)

print(onChainContract.functions.retrieve().call())

txn2= onChainContract.functions.store(21).buildTransaction(
    {
    "from":my_address, "nonce":nonce +1, "chainId":chain_Id,
    "gas":1728712, "gasPrice":w3.toWei("21","gwei")
    }
)
sign_txn2= w3.eth.account.sign_transaction(txn2, private_key= private_key)
sndTxn2= w3.eth.send_raw_transaction(sign_txn2.rawTransaction)
txnReceipt2= w3.eth.wait_for_transaction_receipt(sndTxn2)

print(onChainContract.functions.retrieve().call())
# 