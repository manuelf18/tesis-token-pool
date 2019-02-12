import json
import os
import subprocess


def install(name, token_name):
    data = {
        'name': name,
        'token': token_name
    }
    where_am_i = os.path.dirname(os.path.realpath(__file__))
    with open('{}/solidity/migrations/data/pool.json'.format(where_am_i), 'w') as outfile:
        json.dump(data, outfile)
    subprocess.call('su - && \
                     cd {}/solidity && \
                     truffle compile && \
                     truffle migrate --reset'
                    .format(where_am_i),
                    shell=True)
