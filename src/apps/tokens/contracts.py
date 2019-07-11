import json
import os
from web3 import Web3, HTTPProvider


class Contract:
    def __init__(self, contract_name, *args, **kwargs):
        from .models import Network
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
    """
    Index map:
    0 -> Token name
    1 -> Pool name
    2 -> Amount of tokens in pool
    3 -> Token address
    4 -> Token value
    5 -> Pool is closed
    """
    def __init__(self):
        super().__init__('PoolManager')

    def create_pool(self, pool_name, token_name, token_value):
        json_data = self.get_contract_json(token_name)
        token_address = self.get_address_from_json(json_data)
        return self.contract.functions.addPool(pool_name, token_name, token_address, token_value).transact()

    def pay_user_for_withdrawing_pool(self, pool_index, tokens_qty, user_address):
        try:
            resp = self.contract.functions.payUserFromPool(pool_index, user_address, tokens_qty).transact()
        except Exception as e:
            print(e)
            raise e

    def pay_user_for_joining_pool(self, user_address, tokens_qty):
        try:
            token_address = self.get_address_from_json(self.get_contract_json('TrueToken'))
            resp = self.contract.functions.payUser(token_address, user_address, tokens_qty).transact()
            print(self.get_balance_of('TrueToken'))
        except Exception as e:
            print(e)
            raise e

    def get_balance_of(self, token_name):
        json_data = self.get_contract_json(token_name)
        token_address = self.get_address_from_json(json_data)
        return self.contract.functions.getBalanceOf(token_address).call()
