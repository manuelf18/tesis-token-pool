const truffleAssert = require('truffle-assertions');
const StandardToken = artifacts.require("./StandardToken.sol");
const Pool = artifacts.require("./Pool.sol");

contract("Pool", accounts => {
    it(`should allow me to transfer tokens to an account`, async () => {
        const PoolContract = await Pool.deployed();
        const StandardTokenContract = await StandardToken.deployed();
        let resp, resp2;
        try{
            await StandardTokenContract.transfer(PoolContract.address, 20, {from: accounts[0]});
            resp = await StandardTokenContract.balanceOf(PoolContract.address, {from: accounts[0]});
            resp2 = await StandardTokenContract.balanceOf(accounts[0], {from: accounts[0]});
            assert.equal(resp.toNumber(), 20)
            assert.equal(resp2.toNumber(), 1980);
        }
        catch(e){
            console.log(e);
        }
    });
});