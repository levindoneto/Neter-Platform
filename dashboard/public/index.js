var express = require('express');
var app = express();
app.use(express.static('./'));
app.get('/', (req, res, next) => {
 res.redirect('/');
});
app.listen(8087, '0.0.0.0');
console.log('SERVER UP');

