const router = require('express').Router();
const Token = require('../model/Tokens');


router.get('/tokens', (req, res, next) => {
    const elems = Token.Methods.getAll();
    res.json({ data: elems });
});


router.get('/tokens/:address', (req, res, next) => {
    const { address } = req.params;
    const elem = Token.Methods.get({address});
    res.json({ data: elem });
});


module.exports = router;