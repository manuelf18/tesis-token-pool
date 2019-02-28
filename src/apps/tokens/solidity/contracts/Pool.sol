pragma solidity >=0.4.10 <0.6.0;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    address owner = msg.sender;
    event createUserIndex (uint);
    event superAmount(uint x);
    struct User { address userAddress; uint amount; }
    mapping(uint => mapping(address => uint) ) userIndex;

    struct Pool {
        string poolName; string tokenName; address tokenAddress; uint amount; uint value; 
        mapping(uint => User) Users; uint usersLength;
    }
    Pool[] PoolsArr;
    mapping(address => uint) poolIndex;

    modifier poolExists(address _tokenAddress){
        require(_tokenAddress != address(0x0), "Address already assigned");
        _;
    }

    modifier ownable(){
        require(owner == msg.sender, "El usuario no es el dueño del contrato");
        _;
    }

    function addPool(string memory _poolName, string memory _tokenName, address _tokenAddress, uint _value) public poolExists(_tokenAddress) {
        Pool memory pool;
        pool.poolName = _poolName;
        pool.tokenName = _tokenName;
        pool.tokenAddress = _tokenAddress;
        pool.value = _value;
        PoolsArr.push(pool);
    }

    function addUserToPool(uint _amount, uint _poolIndex) public {
        User memory user;
        Pool storage pool = PoolsArr[_poolIndex];
        address tokenContract = pool.tokenAddress;
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
        pool.amount += _amount;
        if (userIndex[_poolIndex][msg.sender] == 0) {
            user.userAddress = msg.sender;
            user.amount = _amount;
            pool.usersLength++;
            pool.Users[pool.usersLength] = user;
            userIndex[_poolIndex][msg.sender] = pool.usersLength;
            emit createUserIndex(userIndex[_poolIndex][msg.sender]);
        }
        else {
            pool.Users[userIndex[_poolIndex][msg.sender]].amount += _amount;
        }
    }

    function getTokens(uint _amount, uint _poolIndex /*, address _payTokenAddress */) public {
        Pool memory pool = PoolsArr[_poolIndex];
        require(pool.amount >= _amount, "No hay suficientes tokens");
        address tokenContract = pool.tokenAddress;
        ERC20(tokenContract).transfer(msg.sender, _amount);
        // ERC20(_payTokenAddress).transferFrom(msg.sender, address(this), _amount);
        pool.amount -= _amount;
        PoolsArr[_poolIndex] = pool;
        // TODO: implement payment to other users.
    }

    function getPoolsLength() public view returns (uint) {
        return PoolsArr.length;
    }

    function getPoolByIndex(uint index) public view returns(string memory, string memory, uint, address, uint) {
        Pool memory pool = PoolsArr[index];
        return (pool.tokenName, pool.poolName, pool.amount, pool.tokenAddress, pool.value);
    }
    
    function getAmountOfUsersInPool(uint _poolIndex) public view returns (uint){
        return PoolsArr[_poolIndex].usersLength;
    }

    function getUserFromPool(uint _poolIndex) public view returns (address, uint) {
        User memory user = PoolsArr[_poolIndex].Users[userIndex[_poolIndex][msg.sender]];
        return (user.userAddress, user.amount);
    }

    function getUserFromPool(uint _poolIndex, uint _userIndex) public view returns (address, uint) {
        User memory user = PoolsArr[_poolIndex].Users[_userIndex + 1];
        return (user.userAddress, user.amount);
    }

    function updateUserAmount(uint _poolIndex, uint _userIndex, uint _amount, bool add) public ownable(){
        User memory user = PoolsArr[_poolIndex].Users[_userIndex + 1];
        if (add)
            user.amount += _amount;
        else
            user.amount -= _amount;
        emit superAmount(user.amount);
        PoolsArr[_poolIndex].Users[_userIndex] = user;
    }

    function payUser(address _tokenAddress, address _userAddress, uint _amount) public ownable(){
        address tokenContract = _tokenAddress;
        ERC20(tokenContract).transfer(_userAddress, _amount);
    }
}