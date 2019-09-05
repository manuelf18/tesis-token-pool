import json
import os
import time
import datetime

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

    def get_amount_of_offers(self):
        return self.contract.functions.getAmountOfOffers().call()

    def get_all_offers(self):
        amount = self.get_amount_of_offers()
        offers = []
        for i in range(amount):
            offers.append(self.contract.functions.getOfferByIndex(i).call())
        return offers

    def get_offers_by_key(self, key):
        offers = self.get_all_offers()
        offers_for_key = []
        if(len(offers) is 0):
            return offers_for_key
        for offer in offers:
            offer_mapped = self.offer_map(offer)
            if offer_mapped['poolKey'] == key:
                offers_for_key.append(offer_mapped)
        return offers_for_key

    def get_all_pools(self):
        keys = self.get_pool_keys()
        pools = []
        for key in keys:
            pool = self.get_pool_by_key(key, mapped=True)
            pools.append(pool)
        return pools

    def get_pool_by_key(self, key, mapped=False):
        pool = self.contract.functions.getPoolByKey(key).call()
        pool.append(key)
        pool.append(len(self.get_offers_by_key(key)))
        if mapped:
            pool = self.pool_map(pool)
        return pool

    def pool_map(self, pool):
        return {
            'poolName': pool[0],
            'tokenName': pool[1],
            'tokenAddress': pool[2],
            'startDate': datetime.datetime.fromtimestamp(pool[3]).strftime('%d/%m/%Y'),
            'open': pool[4],
            'key': pool[5],
            'amountOfOffers': pool[6],
        }

    def offer_map(self, offer):
        return {
            'index': offer[0],
            'userAddress': offer[1],
            'poolKey': offer[2],
            'offeredAmount': int(offer[3]) * (10 ** -int(offer[4])),
            'offeredValue': int(offer[5]) * 10 ** -2,
            'userEmail': offer[6],
            'createdAt': datetime.datetime.fromtimestamp(offer[7]).strftime('%d/%m/%Y'),
            'recentlyCreated': True if int(datetime.datetime.now().strftime('%d')) - int(datetime.datetime.fromtimestamp(offer[7]).strftime('%d')) <= 1 else False
        }

    def get_offer_statistics(self, offers=[], key=None):
        if len(offers) is 0 and key is None:
            raise Exception('You have to provide the offers or a key')
        elif len(offers) is 0 and key is not None:
            offers = self.get_offers_by_key(key)

        lowest_offer = {'value': offers[0]['offeredValue'], 'qty': offers[0]['offeredAmount']}
        total = 0
        for offer in offers:
            value = offer['offeredValue']
            if value < lowest_offer['value']:
                lowest_offer['value'] = value
                lowest_offer['qty'] = offer['offeredAmount']
            total += value
        return {
            'lowest_offer': lowest_offer,
            'average': total/len(offers),
        }

    def withdraw_from_offer(self, offer_id, amount, token_address, user_address):
        return self.contract.functions.withdrawFromOffer(offer_id, amount, token_address, user_address).transact()
