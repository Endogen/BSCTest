import list_bsc
import requests
import json
import secrets

from web3 import Web3
from eth_account import Account


# Generate address
private_key = "0x" + secrets.token_hex(32)
print("Privkey:", private_key)
acct = Account.from_key(private_key)
print("Address:", acct.address)

# Connect with network
bsc = "https://bsc-dataseed.binance.org/"
#bsc_testnet = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

# Check balance
my_address = "0x82daF05Ffd9dcAC6Ab05EE07ce61b9593E3d04d3"
balance = web3.eth.get_balance(my_address)
print(balance)

result = web3.fromWei(balance, "ether")
print(result)

# Check Tokens Balance
TokenAddress = "0x231cF6F78620e42Fe00D0c5C3088b427F355d01c"

# 1. Get ABI from BSCscan
url_eth = "https://api.bscscan.com/api"
contract_address = web3.toChecksumAddress(TokenAddress)
API_ENDPOINT = url_eth + "?module=contract&action=getabi&address=" + str(contract_address)
r = requests.get(url=API_ENDPOINT)
response = r.json()
abi = json.loads(response["result"])

# 2. Call contract
contract = web3.eth.contract(address=contract_address, abi=abi)
totalSupply = contract.functions.totalSupply().call()
print(totalSupply)
print(contract.functions.name().call())
print(contract.functions.symbol().call())
address = web3.toChecksumAddress(my_address)
balance = contract.functions.balanceOf(address).call()
print(web3.fromWei(balance, "ether"))


# Get price from DEX
def getPrice(factory, pair):
    AMM = list_bsc.module['AMM'][factory]['Factory']
    x = pair.split('/')
    Tokens1 = list_bsc.module['Tokens'][x[0]]
    Tokens2 = list_bsc.module['Tokens'][x[1]]

    Tokens1 = web3.toChecksumAddress(Tokens1)
    Tokens2 = web3.toChecksumAddress(Tokens2)
    Factory_Address = web3.toChecksumAddress(AMM)

    # ABI Contract factory
    with open('src/factory.json', 'r') as abi_definition:
        abi = json.load(abi_definition)

    # ABI Contract Pancake Pair
    with open('src/pair.json', 'r') as abi_definition:
        parsed_pair = json.load(abi_definition)

    contract = web3.eth.contract(address=Factory_Address, abi=abi)
    pair_address = contract.functions.getPair(Tokens1, Tokens2).call()
    pair1 = web3.eth.contract(abi=parsed_pair, address=pair_address)

    reserves = pair1.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]

    print(f'The current {pair} price on {factory} is : ${reserve1/reserve0}')


getPrice(factory="Twindex", pair="DOP/BUSD")
getPrice(factory="Pancake", pair="DOP/BUSD")


# Send tx
transaction = {
        'chainId': 97,  # 97: Testnet. 56: main.
        'to': '0xmyaddress',
        'value': 1,
        'gas': 2000000,
        'gasPrice': 13,
        'nonce': 0,
    }

signed = web3.eth.account.signTransaction(transaction, my_address)
web3.eth.sendRawTransaction(signed.rawTransaction)
