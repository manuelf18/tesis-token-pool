(async function($){
    const web3 = new Web3(Web3.givenProvider || new Web3.providers.HttpProvider('http://127.0.0.1:8545'));
    let accounts = await web3.eth.getAccounts();
    web3.eth.defaultAccount = accounts[0];
    var json = await $.ajax({ url:'http://localhost:8000/static/js/Nickname.json' , method: "GET"});
    const contract = new web3.eth.Contract(json['abi'], '0xb1c4480a6664Aa5E84D9e72B40103afDB8d0e2d9');
    console.log(contract.methods);
    try{   
        await contract.methods.setNicknameByUser('superOsito').send({from:accounts[0]});
        const resp = await contract.methods.getNicknameByUser().call();
        console.log(resp);
    }
    catch(e){
        console.log(e);
    }

})(jQuery);