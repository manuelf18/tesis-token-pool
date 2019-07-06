class Contract {
    // Please make sure to have jQuery enabled when importing this class in the browser
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
    constructor($, nameOfTokenContract ,networkId){
        super($, nameOfTokenContract, networkId);
    }
    async approve(address, amount){
        try{
            return await this.contract.methods.approve(address, amount).send({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in approve: ' + e);
        }
    }
}


class PoolContract extends Contract {
    constructor(abi, networkId, address){
        super(abi, networkId, address);
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
    async addUserToPool(amount, tokenName, tokenIndex){
        try{
            const tokenContractObj = new TokenContract(this.$, tokenName || 'StandardToken', this.networkId);
            await tokenContractObj.setContract();
            await tokenContractObj.approve(this.address, amount);
            await this.contract.methods.addUserToPool(amount, tokenIndex).send({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in method addUserToToken: ' + e);
            throw Error(e);
        }
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
            throw new Error(e);
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