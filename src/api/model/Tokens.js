function _randomFactor(min, max){
    return parseFloat((Math.random() * (min - max) + max).toFixed(3));
}

const Token = {
    Data: [],
    Methods: {
        getAll: function(){
            return Token.Data;
        },
        get: function(param){
            const key = Object.keys(param)[0];
            for(const element of Token.Data){
                if(element[key] === param[key]){
                    return element;
                }
            }
            return null;
        },
        insert: function(instance){
            Token.Data.push(instance);
        },
    },
    Utils: {
        updateValue: function(){
            for(const element of Token.Data){
                if(element.isStatic) continue;
                let randomFactor = _randomFactor(0.100, 0.300);
                let randomVariation;
                do{
                    randomVariation = _randomFactor(randomFactor * -1, randomFactor);
                }while(randomVariation + element.price <= 0);
                element.price += randomVariation;
            }
        },
    },
}



module.exports = Token;
