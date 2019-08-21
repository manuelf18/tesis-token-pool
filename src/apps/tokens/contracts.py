import json
import os
import time

import requests
from web3 import HTTPProvider, Web3

from ..core.utils import create_hash


class Contract:
    def __init__(self, contract_name, *args, **kwargs):
        from .models import Network
        try:
            self.network_id = Network.objects.get(connected=True).port
        except Network.DoesNotExist:
            self.network_id = '5777'
        web3 = Web3(HTTPProvider('http://ganache:8545'))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        json_data = self.get_contract_json(contract_name)
        self.abi = json_data['abi']
        self.address = json_data['networks'][self.network_id]['address']
        self.bytecode = json_data['bytecode']
        self.contract = web3.eth.contract(abi=self.abi, address=self.address, bytecode=self.bytecode)

    def get_contract_json(self, contract_name):
        r = requests.get('http://localhost:8000/static/json/{}.json'.format(contract_name))
        return r.json()


class TokenContract(Contract):
    def __init__(self, token_name):
        super().__init__(token_name)

    def balanceOf(self, address=None):
        if not address:
            address = self.account
        return self.contract.functions.balanceOf(address).call()

    def approve(self, user_address, amount):
        return self.contract.functions.approve(user_address, amount).transact()

    def transfer(self, user_address, amount):
        return self.contract.functions.transfer(user_address, amount).transact()

    def allowance(self, user_address):
        return self.contract.functions.allowance(self.account, user_address).call()

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

    def __generateKey(self):
        flag = True
        tries = 0
        while(flag):
            tries += 1
            try:
                key = create_hash()
                response = self.contract.functions.keyIsNotUsed(key).call()
                if tries >= 10:
                    raise Exception('There was an error generating the key')
                if (response is False):
                    return key
            except Exception as e:
                print(e)
                raise e

    def create_pool(self, pool_name, token_name):
        key = self.__generateKey()
        json_data = self.get_contract_json(token_name)
        token_address = json_data['networks'][self.network_id]['address']
        unix_time = int(time.time())
        return self.contract.functions.createPool(pool_name, token_name, token_address, key, unix_time).transact()

    def get_pool_keys(self):
        return self.contract.functions.getPoolKeys().call()

    def get_balance_of(self, token_name):
        json_data = self.get_contract_json(token_name)
        token_address = self.get_address_from_json(json_data)
        return self.contract.functions.getBalanceOf(token_address).call()
