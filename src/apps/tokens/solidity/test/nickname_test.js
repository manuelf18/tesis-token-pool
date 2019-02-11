const truffleAssert = require('truffle-assertions');
const Nicknames = artifacts.require("./Nickname.sol");

contract("Nicknames", accounts => {
  let myNickname = "Osito";
  it(`should store the nickname ${myNickname}`, async () => {
    const Contract = await Nicknames.deployed();

    // Set nickname
    try{
        const resp = await Contract.setNicknameByUser(myNickname, { from: accounts[0] });
        truffleAssert.eventEmitted(resp, 'Setter');
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

  it(`should allow me to change the nickname ${myNickname}`, async () => {
    const Contract = await Nicknames.deployed();
    const newNickname = `Ranguliao`;
    let oldNick;
    // Set nickname
    try{
        oldNick = await Contract.getNicknameByUser({from: accounts[0]});
        const resp = await Contract.setNicknameByUser(newNickname, { from: accounts[0] });
        truffleAssert.eventEmitted(resp, 'Setter');
    }
    catch(e){
        console.log(`there was an error ${e}`);
    }

    // Get myString from public function getNicknameByUser
    const nickname = await Contract.getNicknameByUser({from: accounts[0]});
    assert.notEqual(oldNick, nickname);
  });

  it(`should allow me to delete my nickname`, async () => {
    const Contract = await Nicknames.deployed();
    try{
        const resp = await Contract.deleteNicknameByUser({from: accounts[0]});
        truffleAssert.eventEmitted(resp, 'Deleter');
        await truffleAssert.reverts(
          Contract.getNicknameByUser({ from: accounts[0] }),
          "The user doenst have a nickname"
      );
    }
    catch(e){
        console.log(`there was an error ${e}`);
    }
  });

  it(`should return the amount of nicknames`, async () => {
    const Contract = await Nicknames.deployed();
    let respArr = {
      valid: null,
      deleted: null
    }
    try{
        respArr.valid = await Contract.getValidNicknames({from: accounts[0]});
        respArr.deleted = await Contract.getDeletedNicknames({from: accounts[0]});
        console.log(respArr);
    }
    catch(e){
        console.log(`there was an error ${e}`);
    }
  });


});