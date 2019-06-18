import json
import os
from web3 import Web3, HTTPProvider
from .models import Network


class Contract:
    def __init__(self, contract_name, *args, **kwargs):
        try:
            self.network_id = Network.objects.get(connected=True).port
        except Network.DoesNotExist:
            self.network_id = '5777'
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


class TokenContract(Contract):
    def __init__(self, token_name):
        super().__init__(token_name)

    def balance(self):
        return self.contract.functions.balanceOf(self.web3.eth.defaultAccount).call()

    def approve(self, user_address, amount):
        return self.contract.functions.approve(user_address, amount).transact()

    def transfer(self, user_address, amount):
        return self.contract.functions.transfer(user_address, amount).transact()

    def allowance(self, user_address):
        return self.contract.functions.allowance(self.web3.eth.defaultAccount, user_address).call()

    def transferFrom(self, _from, to, amount):
        return self.contract.functions.transferFrom(_from, to, amount).transact()


class PoolContract(Contract):
    def __init__(self):
        super().__init__('PoolManager')

    def create_pool(self, pool_name, token_name, token_value):
        json_data = self.get_contract_json(token_name)
        token_address = self.get_address_from_json(json_data)
        try:
            return self.contract.functions.addPool(pool_name, token_name, token_address, token_value).transact()
        except Exception as e:
            print(e)

    def pay(self, pool_index, tokens_qty):
        try:
            total = self.contract.functions.getPoolByIndex(pool_index).call()[2] + tokens_qty
            amount = self.contract.functions.getAmountOfUsersInPool(pool_index).call()
            json_data = self.get_contract_json('TrueToken')
            token_address = self.get_address_from_json(json_data)
            tc = TokenContract('TrueToken')
            for i in range(amount):
                [user_address, user_amount] = self.contract.functions.getUserFromPool(pool_index, i).call()
                to_pay = int((user_amount / total) * tokens_qty)
                self.contract.functions.updateUserAmount(pool_index, i, to_pay, False).transact()
                self.contract.functions.payUser(token_address, user_address, to_pay).transact()
        except Exception as e:
            print(e)
