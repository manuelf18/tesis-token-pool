(async function($){
    class Contract {
        constructor(contractName, networkId){
            this.web3 = new Web3(Web3.givenProvider || new Web3.providers.HttpProvider('http://127.0.0.1:7545'));
            this.contractName = contractName;
            this.networkId = networkId || '5777';
        }
        async setContract(){
            try{
                this.accounts = await this.web3.eth.getAccounts();
                const jsonObject = {
                    abi: await this.getDeployedContractObject(this.contractName, ['abi']),
                    address: await this.getDeployedContractObject(this.contractName, ['networks', this.networkId, 'address'])
                }
                this.web3.eth.defaultAccount = this.accounts[0];
                this.contract = new this.web3.eth.Contract(jsonObject.abi, jsonObject.address);
            }
            catch(e) {
                console.log(e);
            }
        }
        async getDeployedContractJSON(contractName){
            // returns the address of a deployed contract
            try{
                let json = await $.ajax({ url:`http://localhost:8000/static/json/${contractName}.json` , method: "GET"});
                return json;
            }
            catch(e) {
                console.log(e);
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

    class PoolContract extends Contract {
        constructor(){
            super('PoolManager', '1550195851854');
        }
        async addPool(){
            try{
                const tokenContractAddress = await this.getDeployedContractObject('StandardToken', ['networks', this.networkId, 'address']);
                await this.contract.methods.addPool('new Pool', tokenContractAddress).send({from:this.accounts[0]});
            }
            catch(e){
                console.log('error in method addPool: '+ e);
            }
        }
        async getPools(){
            try{
                const pools = await this.contract.methods.getPools().call({from:this.accounts[0]});
                return pools;
            }
            catch(e){
                console.log('error in method getPools: '+ e);
            }
        }
    }

    main = async () => {
        let obj = new PoolContract();
        await obj.setContract();
        await obj.addPool();
        let xpools = await obj.getPools();
        console.log(xpools);
    }
    main();
})(jQuery);