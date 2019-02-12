var StandardToken = artifacts.require("./StandardToken.sol");

module.exports = function(deployer) {
    /*
    The params for the StandardToken contract are:
    (string memory name, string memory symbol, uint8 decimals, uint256 totalSupply)
    */
    const params = {
        name: 'MyNewToken',
        symbol: 'MNT',
        decimals: 2,
        totalSupply: 2000
    }
    deployer.deploy(StandardToken, params.name, params.symbol, params.decimals, params.totalSupply);
};
