class Contract {
    // Please make sure to have jQuery enabled when importing this class in the browser
    constructor($, contractName, networkId){
        this.$ = $;
        this.web3 = new Web3(Web3.givenProvider || new Web3.providers.HttpProvider('http://127.0.0.1:7545'));
        this.contractName = contractName;
        this.networkId = networkId || '5777';
    }
    async setContract(){
        try{
            this.accounts = await this.web3.eth.getAccounts();
            this.abi = await this.getDeployedContractObject(this.contractName, ['abi']);
            this.address = await this.getDeployedContractObject(this.contractName, ['networks', this.networkId, 'address'])
            this.web3.eth.defaultAccount = this.accounts[0];
            this.contract = new this.web3.eth.Contract(this.abi, this.address);
        }
        catch(e) {
            console.log(e);
            throw new Error(e);
        }
    }
    async getDeployedContractJSON(contractName){
        // returns the address of a deployed contract
        try{
            let json = await this.$.ajax({ url:`http://localhost:8000/static/json/${contractName}.json` , method: "GET"});
            return json;
        }
        catch(e) {
            console.log(e);
            throw new Error(e);
        }
    }
    /**
        * Gets a very specific Object of a Contract
        * @param {string} contractName the name of the contract whose JSON you want. 
        * @param {array} arr The array of parameters that will be indexed from the JSON, for example (abi) will find the [abi] in the JSON contract defined.
    */
    async getDeployedContractObject(contractName, arr){
        try{
            let i, x = arr.splice(0,1), obj, json = await this.getDeployedContractJSON(contractName);
            obj = json[x];
            if (arr.length === 1)
                return obj;
            let sub = arr.length;
            for(i=1; i<=sub; i++){
                x = arr.splice(0,1);
                obj = obj[x];
            }
            return obj;
        }
        catch(e) {
            console.log(e);
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
    constructor($, networkId){
        super($, 'PoolManager', networkId);
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
    async getPoolsLength(){
        try{
            const pools = await this.contract.methods.getPoolsLength().call({from:this.accounts[0]});
            return pools;
        }
        catch(e){
            console.log('error in method getPools: '+ e);
            throw new Error(e);
        }
    }
    async getPool(index){
        try{
            return await this.contract.methods.getPoolByIndex(index).call({from:this.accounts[0]});
        }
        catch(e){
            console.log('error in method getPool: '+ e);
            throw new Error(e);
        }
    }
    async getAllPools(amount){
        try{
            let pools = [], i;
            for(i=0; i < amount; i++)
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