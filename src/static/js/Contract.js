const web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:8545'));
const jsonInterface = new FileReader('./Nickname.json');
console.log(web3.version);
const contract = web3.eth.contract(jsonInterface);
console.log(web3);
console.log(contract);