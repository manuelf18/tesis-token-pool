cd src/apps/tokens/solidity/
truffle compile
truffle migrate --reset --network development_local
rm -R ../../../static/json/
cp -R build/contracts ../../../static/json/