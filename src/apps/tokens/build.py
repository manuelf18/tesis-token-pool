import os
import subprocess

# subprocess.call('cd {}/solidity && sudo truffle compile && sudo truffle migrate --reset'.format(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), shell=True)


def install():
    subprocess.call('su - && \
                     cd {}/solidity && \
                     truffle compile && \
                     truffle migrate --reset'
                    .format(os.path.dirname(os.path.realpath(__file__))),
                    shell=True)
