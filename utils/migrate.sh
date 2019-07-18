cd apps/tokens/solidity/
if [ -d "build/contracts" ] ; then
    rm -R build/contracts
fi

if [ -d "../../../static/json/" ] ; then
    rm -R ../../../static/json/
fi
cp -R build/contracts ../../../static/json/