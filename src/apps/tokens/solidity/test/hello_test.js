const truffleAssert = require('truffle-assertions');
const HelloWorld = artifacts.require("./HelloWorld.sol");

contract("HelloWorld", accounts => {
  it("should store the string 'Hey there!'", async () => {
    const helloWorld = await HelloWorld.deployed();

    // Set myString to "Hey there!"
    const resp = await helloWorld.set("Hey there!", { from: accounts[0] });
    truffleAssert.prettyPrintEmittedEvents(resp);

    // Get myString from public variable getter
    const storedString = await helloWorld.myString.call();

    assert.equal(storedString, "Hey there!", "The string was not stored");
  });
});