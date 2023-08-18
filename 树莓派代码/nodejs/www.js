const express = require('express')
// var bodyParser = require('body-parser')
var request=require('request')
const http =require('http')
const app = express();
pucnt=0;
autime='0分0秒';
armflag=false;
puflag=false;

app.use(function (req, res, next) {
	var date = new Date();
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var day = date.getDate();
	var hour = date.getHours();
	var minute = date.getMinutes();
	var second = date.getSeconds();
	var Msecond = date.getMilliseconds();
	console.log(year + 'y ' + month + 'm ' + day + 'd ' + hour + 'h ' + minute + 'm ' + second + 's ' + Msecond + '’', '  ', req.headers['x-forwarded-for'], '  ', req.ip, req.url, '  ',checkPC(req), '  ');
	next();
});

app.get('/', function (req, res) {
    if(checkPC(req))
    {
        res.sendFile(__dirname + "/pc/" + "index.html");
    }else{
        res.sendFile(__dirname + "/ph/" + "index.html");
    }
	
})
app.post('/PU',function(req,res){
	pucnt++;
	res.sendStatus(200);
	console.log('PU++:'+pucnt);
	sendmsg('29');
})
app.post('/AU',function(req,res){
	data=req.query.sec;
	res.sendStatus(200);
	armflag=true;
	if(data==0)
		sendmsg('0');//放下
	else
		sendmsg('32');//抬起
	autime=String(parseInt(data/60))+'分'+String(data%60)+'秒';
	console.log('AU:'+data);
})

app.get('/readPU',function(req,res){
	res.send(String(pucnt));
})
app.get('/readAu',function(req,res){
	res.send(String(autime));
})
app.post('/PUc',function(req,res){
	pucnt=0;
	res.sendStatus(200);
	console.log('PU clear: '+pucnt);
})
app.post("/api",function(req,res){
	var data=req.query.act;
	if(data.charCodeAt(0)>=48&&data.charCodeAt(0)<=57)
	{
		sendmsg(Number(data));
	}
	else
	{
		switch(data)
		{
			case "a":
				sendmsg(17);
				sendpy("/a");
				break;
			case "b":
				sendmsg(18);
				sendpy("/b");
				break;
			case "c":
				sendmsg(19);
				sendpy("/c");
				break;
			case "d":
				sendmsg(20);
				sendpy("/d");
				break;
			case "e":
				sendpy("/follow");
		}
	}
	res.sendStatus(200);
})
app.get("/pushup.html",function(req,res,next){
	sendpy("/pushup");
	puflag=false;
	next();
})
app.get("/armup.html",function(req,res,next){
	sendpy("/armup");
	armflag=false;
	next();
})
app.post("/armup.html",function(req,res)
{
	if(armflag)
		res.send("1")
	else
		res.send("0")
})
app.post("/pushup.html",function(req,res)
{
	if(req.query.ready)
		puflag=true;
	if(puflag)
		res.send("1")
	else
		res.send("0")
})

app.use(function(req,res){
	if(checkPC(req))
	{
		res.sendFile(__dirname + "/pc/" + req.url)
	}
	else
	{
		res.sendFile(__dirname + "/ph/" + req.url)
	}
})

function checkPC(req){
    // var agentstr = navigator.userAgent.toLowerCase();
    var agentstr = req.headers['user-agent'].toLowerCase();  // nodejs
	var agentreg = /(iphone|ipod|ipad|android|symbianos|windows phone|playbook|mobile)/;
	var agentph = agentstr.match(agentreg);
	if(agentph){
		return false;
	}else{
		return true;
	}
}

const server = app.listen(80, function () {
	console.log("服务器已启动, 监听80端口,http://127.0.0.1:80");
})

function sendmsg(msg)
{
	request('http://192.168.4.2/api?act='+msg,{timeout:1500},function(error,res,body){
		console.log('send-robot:'+msg);
	})
}
function sendpy(msg)
{	
	request('http://192.168.4.1:8080'+msg,{timeout:1500},function(error,res,body){
		console.log('send-python:'+msg);
	})
}
