var StandardToken = artifacts.require("./TrueToken.sol");
const fs = require("fs");
const path = require('path');

module.exports = function(deployer) {
    const file = fs.readFileSync(path.resolve(__dirname, "../build/contracts/PoolManager.json"));
    const data = JSON.parse(file);
    const address = data['networks']['5777']['address'];
    /*
    The params for the StandardToken contract are:
    (string memory name, string memory symbol, uint8 decimals, uint256 totalSupply)
    */
    const params = {
        name: 'True Token',
        symbol: 'TRU',
        decimals: 2,
        totalSupply: 200000000,
        poolAddress: address,
    }
    deployer.deploy(StandardToken, params.name, params.symbol, params.decimals, params.totalSupply, params.poolAddress);
};
