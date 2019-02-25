pragma solidity >=0.4.10 <0.6.0;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    event UserIndex (uint);
    struct UserCommit { address userA; uint amount; uint value; }
    UserCommit[] UsersAdding;
    UserCommit[] UsersWithdrawing;
    mapping(address => uint) userAdded;

    string[] poolName;
    address[] tokenAddress;
    mapping(address => string) tokenName;
    uint[] poolAmount;

    
    modifier poolExists(address _tokenAddress){
        require(keccak256(abi.encode(tokenName[_tokenAddress])) != keccak256(""), "");
        _;
    }

    function addPool(string memory _poolName, string memory _tokenName, address _tokenAddress) public poolExists(_tokenAddress) {
        poolName.push(_poolName);
        tokenAddress.push(_tokenAddress);
        tokenName[_tokenAddress] = _tokenName;
        poolAmount.push(0);
    }

    function addUserToPool(uint _amount, uint _poolIndex, uint _value) public {
        // UserCommit memory user;
        UserCommit memory user;
        address tokenContract = tokenAddress[_poolIndex];
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
        poolAmount[_poolIndex] += _amount;
        if (userAdded[msg.sender] == 0) {
            user.userA = msg.sender;
            user.amount = _amount;
            user.value = _value;
            userAdded[msg.sender] = UsersAdding.push(user);
            emit UserIndex(userAdded[msg.sender]);
        }
        else {
            UsersAdding[userAdded[msg.sender] - 1].amount += _amount;
        }
    }

    function commitToken(uint _amount, uint _value) public {
        UserCommit memory user;
        user.userA = msg.sender;
        user.amount = _amount;
        user.value = _value;
        UsersWithdrawing.push(user);
    }

    function getUsersAddingLength() public view returns (uint) {
        return UsersAdding.length;
    }

    function getUsersAddingByIndex(uint index) public view returns(address, uint, uint) {
        UserCommit memory user = UsersAdding[index];
        return (user.userA, user.amount, user.value);
    }

    function getPoolsLength() public view returns (uint) {
        return tokenAddress.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, string memory, uint, address) {
        return (tokenName[tokenAddress[index]], poolName[index], poolAmount[index], tokenAddress[index]);
    }
}