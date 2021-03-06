class Contract {
    constructor(abi, networkId, address){
        this.web3 = new Web3(Web3.givenProvider || new Web3.providers.HttpProvider('http://127.0.0.1:7545'));
        this.abi = abi;
        this.networkId = networkId || '5777';
        this.address = address;
    }
    async setContract(){
        try{
            this.accounts = await this.web3.eth.getAccounts();
            this.web3.eth.defaultAccount = this.accounts[0];
            this.contract = new this.web3.eth.Contract(this.abi, this.address);
        }
        catch(e) {
            console.log(e);
            throw new Error(e);
        }
    }
}

class TokenContract extends Contract {
    constructor(abi, networkId, address){
        super(abi, networkId, address);
    }
    approve(address, amount){
        return this.contract.methods.approve(address, amount).send({from:this.accounts[0]});
    }
    balanceOf(address){
        if(!address) address=this.accounts[0];
        console.log(address);
        return this.contract.methods.balanceOf(address).call({from: this.accounts[0]});
    }
    getDecimals(){
        return this.contract.methods.decimals().call({from: this.accounts[0]});
    }
}


class PoolContract extends Contract {
    /*
    Index map:
    0 -> Token name
    1 -> Pool name
    2 -> Amount of tokens in pool
    3 -> Token address
    4 -> Token value
    5 -> Pool is closed
    6 -> User (msg.sender) has tokens in pool
    7 -> Sold tokens
    */
    constructor(abi, networkId, address){
        super(abi, networkId, address);
        // TODO: Token Map
        this.map = ['tokenName', '']
    }
    /**
        * Handles money conversion with an Eth Contract
        * @param {number} number a number representing a money value.
        * @param {boolean} up if the number is being sent [true] or being received [false] by the contract, defaults to [true]
    */
    _moneyChanger(number, up = true){
        if(up === true)
            return number * 100;
        return number / 100;
    }
    async addPool(tokenName, networkId, poolName){
        try{
            const tokenContractAddress = await this.getDeployedContractObject(tokenName, ['networks', networkId || this.networkId, 'address']);
            await this.contract.methods.addPool(poolName, tokenContractAddress).send({from:this.accounts[0]});
            return true;
        }
        catch(e){
            console.log('error in method addPool: '+ e);
            throw new Error(e);
        }
    }
    addUserToPool(amount, tokenIndex){
        return this.contract.methods.addUserToPool(amount, tokenIndex).send({from:this.accounts[0]});
    }
    getPoolsLength(){
        return this.contract.methods.getPoolsLength().call({from:this.accounts[0]});
    }

    getPool(index){
        return this.contract.methods.getPoolByIndex(index).call({from:this.accounts[0]});
    }

    async getAllPools(){
        try{
            const poolAmount = await this.getPoolsLength();
            if ( poolAmount < 1 ) throw new Error(`There aren't any pools`);
            let pools = [], i;
            for(i=0; i < poolAmount; i++)
                pools.push(await this.getPool(i));
            return pools;
        }
        catch(e){
            console.log('error in method getAllPools: '+ e);
            throw e;
        }
    }
    async getTokens(amount, poolIndex){
        try{
            let pool = parseInt(await this.getPool(poolIndex)[2]);
            if (amount > pool)
                throw new Error('La cantidad de Tokens solicitados es mayor a la disponible');
            await this.contract.methods.getTokens(amount, poolIndex).send({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in method getTokens: '+ e);
            throw new Error(e);
        }
    }
    async getAmountOfUsersInPool(){
        try{
            return await this.contract.methods.getAmountOfUsersInPool().call({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in method getAmountOfUsers ' + e);
        }
    }
    async getUserFromPool(poolIndex) {
        try{
            return await this.contract.methods.getUserFromPool(poolIndex).call({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in method getAmountOfUsers ' + e);
        }
    }
}


class PoolContractV2 extends Contract{
    constructor(abi, networkId, address){
        super(abi, networkId, address);
    }

    getAmountOfPools(){
        return this.contract.methods.getAmountOfPools().call({from:this.accounts[0]});
    }

    getAmountOfOffers(){
        return this.contract.methods.getAmountOfOffers().call({from:this.accounts[0]});
    }

    async getAllPools(keys){
        let poolsArr = [];
        let pool;
        for(const key of keys){
            try {
                pool = await this.contract.methods.getPoolByKey(key).call({from:this.accounts[0]});
                pool.offers = await this.getOffersByKey(key); 
            } catch (error) {
                console.log(`There was an error getting the pool with key ${key}: ${error}`);
                pool = {};
            }
            poolsArr.push(pool);
        }
        return poolsArr;
    }

    async getAllOffers(){
        try {
            const total = await this.getAmountOfOffers();
            const offers = [];
            for(let index=0; index < total; index++){
                offers.push(await this.contract.methods.getOfferByIndex(index).call({from:this.accounts[0]}));
            }
            return offers;
        } catch (error) {
            console.log(error);
            throw error;
        }   
    }


    async getOffersByKey(key, offers=null){
        try{
            if(!offers)
                offers = await this.getAllOffers();
            if(offers.length === 0) return 0;
            const offerArr = [];
            for(const offer of offers){
                if (offer[1] === key)
                    offerArr.push(offer);
            }
            return offerArr;
        } catch (error) {
            throw error;
        }   
    }

    async createOffer(poolKey, amount, decimals, value, email, tokenAddress){
        try {
            const now = Math.floor(Date.now() / 1000);
            return this.contract.methods.createOffer(poolKey, amount, decimals, value, email, now, tokenAddress).send({from:this.accounts[0]});
        } catch (error) {
            throw error;
        }
    }

    getPoolByIndex(index){
        return this.contract.methods.getPoolByIndex(index).call({from:this.accounts[0]});
    }

}