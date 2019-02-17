import json
import os
from web3 import Web3, HTTPProvider


class Contract:
    def __init__(self, network_id, contract_name, *args, **kwargs):
        self.network_id = network_id
        self.web3 = Web3(HTTPProvider('http://ganache:8545'))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        json_data = self.get_contract_json(contract_name)
        self.contract = self.set_contract(json_data)

    def get_contract_json(self, contract_name):
        where_am_i = os.path.dirname(os.path.realpath(__file__))
        fn = '{}/solidity/build/contracts/{}.json'.format(where_am_i, contract_name)
        data = open(fn).read()
        return json.loads(data)

    def set_contract(self, json_data, *args, **kwargs):
        """ sets the contract """
        return self.web3.eth.contract(
            abi=json_data['abi'],
            address=self.get_address_from_json(json_data),
            bytecode=json_data['bytecode']
        )

    def get_address_from_json(self, json_data):
        return json_data['networks'][self.network_id]['address']


class PoolContract(Contract):
    def __init__(self, network_id):
        super().__init__(network_id, 'PoolManager')

    def create_pool(self, name, token_name):
        json_data = self.get_contract_json(token_name)
        token_address = self.get_address_from_json(json_data)
        self.contract.functions.addPool(name, token_address).transact()
