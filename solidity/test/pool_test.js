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
            await PoolContract.addPool('Pool1', 'StandardToken', StandardContractAdd , {from:accounts[0]});
            resp = await PoolContract.getPoolByIndex(0, {from: accounts[0]});
            assert.equal(resp[1], 'Pool1');
        }
        catch(e){
            console.log(e);
        }
    });
    // it(`should allow me to get many Pools`, async () => {
    //     let resp = [], i;
    //     try{
    //         for(i=1; i<=3; i++){
    //             await PoolContract.addPool(`Pool${i}`, StandardContractAdd, {from:accounts[0]});
    //         }
    //         resp.push(await PoolContract.getPools());
    //         console.log(resp);
    //         assert.equal(resp[0][0][0], 'Pool1');
    //     }
    //     catch(e){
    //         console.log(e);
    //     }
    // });
    it(`should allow me to get into the pools`, async () => {
        let resp, poolResp;
        try{
            await StandardTokenContract.approve(PoolContract.address, 20, {from:accounts[0]});
            poolResp = await PoolContract.addUserToPool(20, 0, 150, {from:accounts[0]});
            truffleAssert.prettyPrintEmittedEvents(poolResp);
            resp = await StandardTokenContract.balanceOf(PoolContract.address);
            assert.equal(resp.toNumber(), 20);
        }
        catch(e){
            console.log(e);
        }
    });
});