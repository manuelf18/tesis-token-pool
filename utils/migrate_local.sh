cd src/apps/tokens/solidity/
truffle compile
truffle migrate --reset --network development_local
python3 ../../../manage.py shell < ../migrate.py
rm -R ../../../static/json/
cp -R build/contracts ../../../static/json/