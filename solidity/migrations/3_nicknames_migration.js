var Nickname = artifacts.require("./Nickname.sol");

module.exports = function(deployer) {
  deployer.deploy(Nickname);
};
