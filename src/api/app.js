const app = require('express')();
const Token = require('./model/Tokens');

app.use('/api', require('./controllers/router'));

app.listen(3000, () => {
    Token.Methods.insert({ name: 'UTPToken', address: '0x247FDF7474eE30F3127d095449d10d02DD0C1137', price: 0.50, isStatic: false});
    Token.Methods.insert({ name: 'TrueToken', address: '0x66A32B96036C08aD3554d87428af417EF4831B43', price: 1, isStatic: true});
    const minutes = 5;
    setInterval(() => {
        console.log('Cambiando valor de los tokens....');
        Token.Utils.updateValue();
    }, minutes * 60 * 1000);
    console.log('Escuchando en el puerto 3000');
});