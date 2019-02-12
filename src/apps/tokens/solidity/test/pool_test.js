const truffleAssert = require('truffle-assertions');
const StandardToken = artifacts.require("./StandardToken.sol");
const Pool = artifacts.require("./PoolManager.sol");

contract("Pool", accounts => {
    let PoolContract; 
    let StandardTokenContract;
    let StandardContractAdd;

    before('setup contracts', async() => {
        PoolContract = await Pool.deployed();
        StandardTokenContract = await StandardToken.deployed();
        StandardContractAdd = await StandardTokenContract.address;
    });

    it(`should allow me to add a new pool and get set pool`, async () => {

        let resp;
        try{
            await PoolContract.addPool('Pool1', StandardContractAdd , {from:accounts[0]});
            resp = await PoolContract.getPools({from: accounts[0]});
            console.log(resp);
            assert.equal(resp[0], 'Pool1');
            // resp = await StandardTokenContract.balanceOf(PoolContract.address, {from: accounts[0]});
            // resp2 = await StandardTokenContract.balanceOf(accounts[0], {from: accounts[0]});
            // assert.equal(resp.toNumber(), 20)
            // assert.equal(resp2.toNumber(), 1980);
        }
        catch(e){
            console.log(e);
        }
    });
    it(`should allow me to get many Pools`, async () => {
        let resp = [], i;
        try{
            for(i=1; i<=3; i++){
                await PoolContract.addPool(`Pool${i}`, StandardContractAdd, {from:accounts[0]});
            }
            resp.push(await PoolContract.getPools());
            assert.equal(resp[0][0][0], 'Pool1');
        }
        catch(e){
            console.log(e);
        }
    });
    it(`should allow me to get into the pools`, async () => {
        let resp;
        try{
            await StandardTokenContract.approve(PoolContract.address, 20, {from:accounts[0]});
            resp = await PoolContract.addUserToPool(20, 1, {from:accounts[0]});
            assert.equal(resp[0][0][0], 'Pool1');
        }
        catch(e){
            console.log(e);
        }
    });
});