cd apps/tokens/solidity/
rm -R build/contracts
truffle compile
truffle migrate --reset
rm -R ../../../static/json/
cp -R build/contracts ../../../static/json/