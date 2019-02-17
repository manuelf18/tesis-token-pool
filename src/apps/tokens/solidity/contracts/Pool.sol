pragma solidity >=0.4.10 <0.6.0;
pragma experimental ABIEncoderV2;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    struct User {
        address userA;
        uint amount;      
    }

    string[] name;
    address[] tokenA;

    uint[] usersIndex;
    
    mapping(uint => User) users;

    function addPool(string memory _name, address _tokenA) public{
        name.push(_name);
        tokenA.push(_tokenA);
    }

    function addUserToPool(uint _amount, uint _poolIndex) public{
        address tokenContract = tokenA[_poolIndex];
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
    }

    function getPools() public view returns (string[] memory, address[] memory){
        return (name, tokenA);
    }

    function getPoolsLength() public view returns (uint) {
        return name.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, address) {
        return (name[index], tokenA[index]);
    }


    // function getUsersByIndex(uint _indexP, uint _indexU) public view returns(address, uint amount){
    //     return (pools[_indexP].users[_indexU].userA, pools[_indexP].users[_indexU].amount);
    // }
}