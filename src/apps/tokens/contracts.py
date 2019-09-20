import datetime
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

    def get_current_token_value(self, token_address):
        r = requests.get('http://express:3000/api/tokens/{}'.format(token_address))
        price = r.json()['data']['price']
        return float("{0:.2f}".format(price))

    def get_payment_token_address(self):
        return '0x66A32B96036C08aD3554d87428af417EF4831B43'


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

    def get_current_token_value(self):
        return super().get_current_token_value(self.address)

    def get_pool_by_address(self):
        pc = PoolContract()
        return pc.get_pool_by_address(self.address)

    @classmethod
    def get_pool_address(cls):
        pool = cls('PoolManager')
        return pool.address


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

    def get_offer_by_index(self, index):
        offers = self.get_all_offers()
        return self.offer_map(offers[index])

    def get_all_pools(self):
        keys = self.get_pool_keys()
        pools = []
        for key in keys:
            pool = self.get_pool_by_key(key, mapped=True)
            if pool['open']:
                pools.append(pool)
        return pools

    def get_pool_by_key(self, key, mapped=False):
        pool = self.contract.functions.getPoolByKey(key).call()
        pool.append(key)
        pool.append(len(self.get_offers_by_key(key)))
        if mapped:
            pool = self.pool_map(pool)
        return pool

    def get_pool_by_address(self, address):
        pools = self.get_all_pools()
        for pool in pools:
            if pool['tokenAddress'] == address:
                return pool
        return None

    def pool_map(self, pool):
        return {
            'poolName': pool[0],
            'tokenName': pool[1],
            'tokenAddress': pool[2],
            'startDate': datetime.datetime.fromtimestamp(pool[3]).strftime('%d/%m/%Y'),
            'open': pool[4],
            'key': pool[5],
            'amountOfOffers': pool[6],
            'tokenValue': self.get_current_token_value(pool[2])
        }

    def offer_map(self, offer):
        return {
            'index': offer[0],
            'userAddress': offer[1],
            'poolKey': offer[2],
            'offeredAmount': int(offer[3]) * (10 ** -int(offer[4])),
            'offeredDecimals': int(offer[4]),
            'offeredValue': int(offer[5]) * 10 ** -2,
            'userEmail': offer[6],
            'createdAt': datetime.datetime.fromtimestamp(offer[7]).strftime('%d/%m/%Y'),
            'recentlyCreated': True if int(datetime.datetime.now().strftime('%d')) - int(datetime.datetime.fromtimestamp(offer[7]).strftime('%d')) <= 1 else False
        }

    def get_offers_clean(self, key):
        offers = self.get_offers_by_key(key)
        pool = self.get_pool_by_key(key, mapped=True)
        current_value = self.get_current_token_value(pool['tokenAddress'])
        for offer in offers:
            if offer['offeredValue'] <= current_value:
                offer['offeredValue'] = (0.05 * current_value + current_value)
            else:
                offer['offeredValue'] *= (0.10 * current_value + current_value)
        return offers

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

    def create_offer(self, key, email, amount, decimals, account, value, address):
        offer_value = int(value * 10 ** 2)
        payment_address = self.get_payment_token_address()
        return self.contract.functions.createOffer(key, int(amount), decimals, offer_value, email, int(time.time()), address, account, payment_address).transact()

    def withdraw_from_offer(self, offer_id, amount, token_address, user_address):
        return self.contract.functions.withdrawFromOffer(offer_id, amount, token_address, user_address).transact()

    def close_pool(self, key):
        return self.contract.functions.closePool(key).transact()
