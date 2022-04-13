from web3 import Web3

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

address = "0x82daF05Ffd9dcAC6Ab05EE07ce61b9593E3d04d3"
balance = web3.eth.get_balance(address)
print(balance)

result = web3.fromWei(balance, "ether")
print(result)


