sudo rm -R build/contracts
sudo truffle compile
sudo truffle migrate --reset --network development_local
sudo truffle test  --network development_local
