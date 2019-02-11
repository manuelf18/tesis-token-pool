pragma solidity >=0.4.10 <0.6.0;


contract Pool{
    string name;

    // This is a mapping to the type of token the pool is hosting
    mapping(string => address) typeOf;


    constructor(string memory _name, string memory _tokenName, address _contract) public{
        name = _name;
        typeOf[_tokenName] = _contract;
    }
}