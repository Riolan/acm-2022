#!/usr/bin/env node 
var express = require('express'); 
var bodyParser = require('body-parser'); 
var app = express(); 


app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false })); 
app.set("view engine", "ejs");


app.get("/", (req,res) => {
    console.log("Someone connected to the server, page '\'.");
    var spawn = require('child_process').spawn;
    var process = spawn('python', './index.py');
    process.stdout.on('data', function(data) {
        res.send(data.toString());
    });
    //res.render("index", {data: ""});
});
/*
app.post("/", (req, res) => { 
    var data = req.body.question;
    console.log(data);
}); 
 */
app.listen(3000, function() {
    console.log("Logged");
}); 