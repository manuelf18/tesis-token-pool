pragma solidity >=0.4.10 <0.6.0;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    address owner = msg.sender;
    
    struct Pool {
        string name; string tokenName; address tokenAddress;
    }

    struct UserReceipt {
        // required
        address userAddress;
        string poolKey;
        uint valueWhenAdded;
        uint decimals;

        // info purposes only
        string userName;
        string userEmail;
    }

    Pool[] pools;

    mapping(string => uint) keyPool;

    modifier poolExists(address _tokenAddress){
        require(_tokenAddress != address(0x0), "Address already assigned");
        _;
    }

    modifier ownable(){
        require(owner == msg.sender, "El usuario no es el dueño del contrato");
        _;
    }

    function verifyUniqueKey(string memory _key) public view {
        if (keyPool[_key] != 0 || keyOffer[_key] != 0)
            return false;
        return true;
    }

    modifier keyIsUnique(string memory _key){
        require(verifyUniqueKey(_key) == true, 'This key is already in use');
        _;
    }

    function createPool(string memory _poolName, string memory _tokenName, address _tokenAddress, string memory _key)
        public
        ownable()
        keyIsUnique(_key)
    {
        Pool memory pool;
        pool.name = _poolName;
        pool.tokenName = _tokenName;
        pool.tokenAddress = _tokenAddress;
        pools.push(pool);
        keyPool[_key] = pools.length - 1;
    }

    function addTokenToPool()