pragma solidity >=0.4.10 <0.6.0;

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
    mapping(address => bool) poolExists;

    modifier onlyOnePool(address _tokenA){
        require(poolExists[_tokenA] == false, "");
        _;
    }

    function addPool(string memory _name, address _tokenA) public onlyOnePool(_tokenA){
        name.push(_name);
        tokenA.push(_tokenA);
        poolExists[_tokenA] = true;
    }

    function addUserToPool(uint _amount, uint _poolIndex) public{
        address tokenContract = tokenA[_poolIndex];
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
    }

    function getPoolsLength() public view returns (uint) {
        if (name.length > tokenA.length)
            return name.length;
        return tokenA.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, address) {
        return (name[index], tokenA[index]);
    }
}