const truffleAssert = require('truffle-assertions');
const StandardToken = artifacts.require("./StandardToken.sol");

contract("StandardToken", accounts => {
    it(`should allow me to transfer to various accounts.`, async () => {
        const Contract = await StandardToken.deployed();
        let resp, amount;
        try{
            for(i=1; i<=5; i++){
                await Contract.transfer(accounts[i], 100, { from: accounts[0] });
                resp = await Contract.balanceOf(accounts[i], { from: accounts[i] });
                amount = resp.toNumber();
                console.log(amount)
                assert.equal(amount, 100);
            }
        }
        catch(e){
            console.log(`there was an error ${e}`);
        }
    });
});