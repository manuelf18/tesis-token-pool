cd apps/tokens/solidity/
truffle compile
truffle migrate --reset
rm -R ../../../static/json/
cp -R build/contracts ../../../static/json/