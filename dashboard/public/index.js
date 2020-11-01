var express = require('express');
var app = express();
app.use(express.static('.'));
app.get('/', function (req, res, next) {
 res.redirect('/'); 
});
app.listen(8085, 'localhost');
console.log('Server is Listening on port 8087');