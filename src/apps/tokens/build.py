import os
import subprocess


def install():
    subprocess.call('su - && \
                     cd {}/solidity && \
                     truffle compile && \
                     truffle migrate --reset'
                    .format(os.path.dirname(os.path.realpath(__file__))),
                    shell=True)
