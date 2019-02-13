(async function($){
    class Contract {
        constructor(contractName){
            this.web3 = new Web3(Web3.givenProvider || new Web3.providers.HttpProvider('http://127.0.0.1:7545'));
            this.contractName = contractName;
        }
        async setContract(){
            try{
                this.accounts = await this.web3.eth.getAccounts();
                console.log(this.accounts);
                let json = await $.ajax({ url:`http://localhost:8000/static/json/${this.contractName}.json` , method: "GET"});
                this.web3.eth.defaultAccount = this.accounts[0];
                this.contract = new this.web3.eth.Contract(json['abi'], '0xb1c4480a6664Aa5E84D9e72B40103afDB8d0e2d9');
            }
            catch(e) {
                console.log(e);
            }
        }
    }

    class PoolContract extends Contract {
        constructor(){
            super('PoolManager');
        }
        async addPool(){
            try{
                console.log(this.accounts[0]);
                await this.contract.methods.addPool('new Pool', '0xcb1514DA0236d254127bF1f10141967325F7693d').send({from:this.accounts[0]});
            }
            catch(e){
                console.log('error in method addPools: '+ e);
            }
        }
        async getPools(){
            try{
                const pools = await this.contract.methods.getPools().call();
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