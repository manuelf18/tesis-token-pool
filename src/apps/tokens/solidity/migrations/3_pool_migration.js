var Pool = artifacts.require("./Pool.sol");

module.exports = function(deployer) {
    /*
    The params for the Pool contract are:
    (string memory _name, string memory _tokenName, address _contract)
    */
    const params = {
        name: 'SuperPool',
        tokenName: 'MyNewToken',
        contract: '0xc8909cb3a47B0A6c34aC01f60b396F6A9d94F8d7'
    }
    deployer.deploy(Pool, params.name, params.tokenName, params.contract);
};
