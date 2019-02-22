pragma solidity >=0.4.10 <0.6.0;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    struct User {
        address userA;
        uint amount;      
    }

    string[] name;
    address[] tokenAddress;
    uint[] poolAmount;

    uint[] usersIndex;
    
    mapping(uint => User) users;
    mapping(address => bool) poolExists;

    modifier onlyOnePool(address _tokenAddress){
        require(poolExists[_tokenAddress] == false, "");
        _;
    }

    function addPool(string memory _name, address _tokenAddress) public onlyOnePool(_tokenAddress){
        name.push(_name);
        tokenAddress.push(_tokenAddress);
        poolAmount.push(0);
        poolExists[_tokenAddress] = true;
    }

    function addUserToPool(uint _amount, uint _poolIndex) public{
        address tokenContract = tokenAddress[_poolIndex];
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
        poolAmount[_poolIndex] += _amount;
    }

    function getPoolsLength() public view returns (uint) {
        if (name.length > tokenAddress.length)
            return name.length;
        return tokenAddress.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, uint, address) {
        return (name[index], poolAmount[index], tokenAddress[index]);
    }
}