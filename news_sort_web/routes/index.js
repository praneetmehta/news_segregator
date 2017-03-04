var express = require('express');
var news_db = require('../schema/schema.js');
var mongoose = require('mongoose');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  news_db.find({}).exec(function(err, news){
  	if(err){
  		res.status(500).send(err);
  	}else{
  		res.render('index',{
  			news:news
  		});
  	}

  });
});

module.exports = router;
