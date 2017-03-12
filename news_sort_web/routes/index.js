var express = require('express');
var news_db = require('../schema/schema.js');
var mongoose = require('mongoose');
var PythonShell = require('python-shell');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    if(req.query.page > 1){
        n = req.query.page;
        console.log(req.query.page);

    }else{
        n=1;
    }
    var options = {
      mode: 'text',
      scriptPath: '/media/praneet/Trash/ML/news-sort-master/scraper/',
      args: [n-1]
    };
    console.log(options.args);
    PythonShell.run('scraper.py', options, function(error, results){
            console.log(error);
            news_db.find({'Page':n}).exec(function(err, news){
               if(err){
                   res.status(500).send(err);
               }else{
                   res.render('index',{
                       news:news
                   });
               }

            });

    })
});

module.exports = router;
