const truffleAssert = require('truffle-assertions');
const StandardToken = artifacts.require("./StandardToken.sol");

contract("StandardToken", accounts => {
    it(`should allow me to transfer to another accounts.`, async () => {
        const Contract = await StandardToken.deployed();
        let resp, amount;
        try{
            await Contract.transfer(accounts[1], 100, { from: accounts[0] });
            resp = await Contract.balanceOf(accounts[1], { from: accounts[i] });
            amount = resp.toNumber();
            assert.equal(amount, 100);
        }
        catch(e){
            console.log(`there was an error ${e}`);
        }
    });
});