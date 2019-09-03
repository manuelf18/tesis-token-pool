pragma solidity >=0.4.10 <0.6.0;
pragma experimental ABIEncoderV2;

import "./lib/ERC20.sol";
contract PoolManager{
    // these are the structs
    address owner = msg.sender;

    struct Pool {
        string poolName;
        string tokenName;
        address tokenAddress;
        uint openedDate;
        bool open;
    }

    struct Offer {
        // required
        address userAddress;
        string poolKey;
        uint amount;
        uint decimals;
        uint value;

        // info purposes only
        string userEmail;
        uint createdAt;
    }

    Pool[] pools;
    Offer[] offers;

    string[] poolKeys;

    mapping(string => bool) keyUsed;
    mapping(string => uint) keyPool;
    mapping(address => string) openContractForToken;

    modifier ownable(){
        require(owner == msg.sender, "User doesn't own contract");
        _;
    }

    function keyIsNotUsed(string memory _key) public view returns (bool){
        return keyUsed[_key];
    }

    modifier keyIsUnique(string memory _key){
        require(keyIsNotUsed(_key) == false, 'This key is already in use');
        _;
    }

    modifier poolWithKeyExists(string memory _key){
        require(keyIsNotUsed(_key) == true, 'Theres no pool with that key');
        _;
    }

    function createPool(string memory _poolName, string memory _tokenName, address _tokenAddress, string memory _key, uint _openedDate)
        public
        ownable()
        keyIsUnique(_key)
    {
        Pool memory pool;
        pool.poolName = _poolName;
        pool.tokenName = _tokenName;
        pool.tokenAddress = _tokenAddress;
        pool.openedDate = _openedDate;
        pool.open = true;
        pools.push(pool);
        keyPool[_key] = pools.length - 1;
        keyUsed[_key] = true;
        poolKeys.push(_key);
    }

    function createOffer(string memory _pKey, uint _amount, uint _decimals, uint _value, string memory _uEmail,
                         uint _cAt, address tokenContract)
        public
        poolWithKeyExists(_pKey)
    {
        ERC20(tokenContract).transferFrom(msg.sender, address(this), _amount);
        Offer memory offer;
        offer.userAddress = msg.sender;
        offer.poolKey = _pKey;
        offer.amount = _amount;
        offer.decimals = _decimals;
        offer.value = _value;
        offer.userEmail = _uEmail;
        offer.createdAt = _cAt;
        offers.push(offer);
    }

    function getPoolByIndex(uint _index)
        private
        view
        returns(string memory, string memory, address, uint, bool)
    {
        Pool memory pool = pools[_index];
        return(
            pool.poolName,
            pool.tokenName,
            pool.tokenAddress,
            pool.openedDate,
            pool.open
        );
    }

    function getPoolByKey(string memory _key)
        public
        view
        poolWithKeyExists(_key)
        returns(string memory, string memory, address, uint, bool)
    {
        uint index = keyPool[_key];
        return getPoolByIndex(index);
    }

    function getAmountOfPools()
        public
        view
        returns (uint)
    {
        return pools.length;
    }

    function getPoolKeys()
        public
        view
        ownable()
        returns (string[] memory)
    {
        return poolKeys;
    }

    function getAmountOfOffers()
        public
        view
        returns (uint)
    {
        return offers.length;
    }

    function getOfferByIndex(uint index)
        public
        view
        returns (address, string memory, uint, uint, uint, string memory, uint)
    {
       Offer memory offer = offers[index];
       return(
            offer.userAddress,
            offer.poolKey,
            offer.amount,
            offer.decimals,
            offer.value,
            offer.userEmail,
            offer.createdAt
       );
    }
}