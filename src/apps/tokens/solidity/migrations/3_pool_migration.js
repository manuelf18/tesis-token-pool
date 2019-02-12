var Pool = artifacts.require("./PoolManager.sol");
var fs = require("fs");
var path = require('path');

module.exports = function(deployer) {
    /*
    The params for the Pool contract are:
    (string memory _name, string memory _tokenName, address _contract)
    */
    // const file = fs.readFileSync(`${path.basename(__dirname)}/data/pool.json`);
    // const data = JSON.parse(file);
    // const params = {
    //     name: data['name'] || 'SuperPool',
    //     tokenName: data['token'] || 'MyNewToken',
    //     contract: '0x186b0cb8d89A32cce82d8522092a7df601558480' // This is the address of the StandardToken
    // }
    deployer.deploy(Pool);
};
