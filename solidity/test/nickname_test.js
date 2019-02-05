const truffleAssert = require('truffle-assertions');
const Nicknames = artifacts.require("./Nickname.sol");

contract("Nicknames", accounts => {
  let myNickname = "Osito";
  it(`should store the nickname ${myNickname}`, async () => {
    const Contract = await Nicknames.deployed();

    // Set nickname
    try{
        const resp = await Contract.setNicknameByUser(myNickname, { from: accounts[0] });
        truffleAssert.prettyPrintEmittedEvents(resp);
    }
    catch(e){
        console.log(`there was an error ${e}`);
    }

    // Get myString from public function getNicknameByUser
    const nickname = await Contract.getNicknameByUser({from: accounts[0]});
    assert.equal(myNickname, nickname);
  });

  it(`shouldnt allow any other user to use the nickname ${myNickname}`, async () => {
    const Contract = await Nicknames.deployed();
    await truffleAssert.reverts(
        Contract.setNicknameByUser(myNickname, { from: accounts[1] }),
        "The nickname exists"
    );
  });


});