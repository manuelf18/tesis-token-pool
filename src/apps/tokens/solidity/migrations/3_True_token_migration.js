var StandardToken = artifacts.require("./TrueToken.sol");

module.exports = function(deployer) {
    /*
    The params for the StandardToken contract are:
    (string memory name, string memory symbol, uint8 decimals, uint256 totalSupply)
    */
    const params = {
        name: 'True Token',
        symbol: 'TRU',
        decimals: 4,
        totalSupply: 200000000
    }
    deployer.deploy(StandardToken, params.name, params.symbol, params.decimals, params.totalSupply);
};
