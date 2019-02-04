import json
from web3 import Web3, HTTPProvider


class Contract:
    def __init__(self, contract='./solidity/build/contracts/HelloWorld.json', *args, **kwargs):
        self.web3 = Web3(HTTPProvider('http://ganache:8545'))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        data = open(contract).read()
        self.json_data = json.loads(data)

    def set_contract(self, *args, **kwargs):
        return self.web3.eth.contract(
            abi=self.json_data['abi'],
            bytecode=self.json_data['bytecode']
        )

    def deploy_contract(self, *args, **kwargs):
        tx_deploy = self.set_contract().constructor().transact()
        return self.web3.eth.waitForTransactionReceipt(tx_deploy)

    def set_instance(self, *args, **kwargs):
        self.instance = self.web3.eth.contract(
            address=self.deploy_contract().contractAddress,
            abi=self.json_data['abi']
        )

    def send_to_contract(self, message=None, *args, **kwargs):
        if message is None:
            return  # this should be an exception
        self.set_instance()
        self.instance.functions.set(message).transact()
        response = self.instance.functions.myString().call()
        print(response)
        return response
