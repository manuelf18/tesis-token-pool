cd apps/tokens/solidity/
truffle compile
truffle migrate --reset
python migrate.py
rm -R ../../../static/json/
cp -R build/contracts ../../../static/json/