var StandardToken = artifacts.require("./UTPToken.sol");

module.exports = function(deployer) {
    /*
    The params for the StandardToken contract are:
    (string memory name, string memory symbol, uint8 decimals, uint256 totalSupply)
    */
    const params = {
        name: 'UTP Token',
        symbol: 'UTP',
        decimals: 2,
        totalSupply: 10000000
    }
    deployer.deploy(StandardToken, params.name, params.symbol, params.decimals, params.totalSupply);
};
