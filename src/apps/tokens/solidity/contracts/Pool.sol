pragma solidity >=0.4.10 <0.6.0;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    event createUserIndex (uint);
    struct User { address userAddress; uint amount; }
    User[] UsersArr;
    mapping(address => uint) userIndex;

    struct Pool { string poolName; string tokenName; address tokenAddress; uint amount; uint value; }
    Pool[] PoolsArr;
    mapping(address => uint) poolIndex;
    // string[] poolName;
    // address[] tokenAddress;
    // mapping(address => string) tokenName;
    // uint[] poolAmount;

    
    modifier poolExists(address _tokenAddress){
        require(_tokenAddress != address(0x0), "Address already assigned");
        _;
    }

    function addPool(string memory _poolName, string memory _tokenName, address _tokenAddress, uint _value) public poolExists(_tokenAddress) {
        Pool memory pool;
        pool.poolName = _poolName;
        pool.tokenName = _tokenName;
        pool.tokenAddress = _tokenAddress;
        pool.value = _value;
        pool.amount = 0;
        PoolsArr.push(pool);
    }

    function addUserToPool(uint _amount, uint _poolIndex) public {
        // UserCommit memory user;
        User memory user;
        Pool memory pool = PoolsArr[_poolIndex];
        address tokenContract = pool.tokenAddress;
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
        pool.amount += _amount;
        if (userIndex[msg.sender] == 0) {
            user.userAddress = msg.sender;
            user.amount = _amount;
            userIndex[msg.sender] = UsersArr.push(user);
            emit createUserIndex(userIndex[msg.sender]);
        }
        else {
            UsersArr[userIndex[msg.sender] - 1].amount += _amount;
        }
        PoolsArr[_poolIndex] = pool;
    }

    function getTokens(uint _amount, uint _poolIndex) public {
        Pool memory pool = PoolsArr[_poolIndex];
        require(pool.amount >= _amount, "No hay suficientes tokens");
        address tokenContract = pool.tokenAddress;
        // ERC20(tokenContract).approve(msg.sender, _amount);
        ERC20(tokenContract).transfer(msg.sender, _amount);
        pool.amount -= _amount;
        PoolsArr[_poolIndex] = pool;
        // TODO: implement payment to other users.
    }

    function getUsersLength() public view returns (uint) {
        return UsersArr.length;
    }

    function getUserByIndex(uint index) public view returns(address, uint) {
        User memory user = UsersArr[index];
        return (user.userAddress, user.amount);
    }

    function getPoolsLength() public view returns (uint) {
        return PoolsArr.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, string memory, uint, address, uint) {
        Pool memory pool = PoolsArr[index];
        return (pool.tokenName, pool.poolName, pool.amount, pool.tokenAddress, pool.value);
    }
}