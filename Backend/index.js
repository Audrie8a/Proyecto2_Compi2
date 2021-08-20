
var express = require('express');
const ejs=require('ejs');
const morgan=require('morgan');
const bodyParser = require('body-parser');
const path = require('path');

var app = express();
const http=require('http').Server(app);
const io=require("socket.io")(http,{
  cors:{
    origin:true,
    credentials: true,
    methods:["GET","POST"]
  }
})
const cors = require('cors');
const port = 3000



app.use(morgan('dev'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended: true}))
app.use(cors());

//Rutas
app.get('/', function(req,res){
res.send("Bienvenido!")
});






http.listen(port, function () {
  console.log('Listening on port',port);
});