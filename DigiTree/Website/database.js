const mysql = require('mysql');
var connection = mysql.createConnection({
    host : 'localhost',
    database : 'ie',
    user : 'root',
    password : ''
});

connection.connect(function(error) {
    if (error) {
        throw error;
    }
    else {
        console.log('MySQL Database is connected Successfully');
    }
});

module.exports = connection;