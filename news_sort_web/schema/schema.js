mongoose = require('mongoose');

var Schema = mongoose.Schema;

// create a schema
var userSchema = new Schema({
  Category: String,
  Heading: String,
  Story: String,
  Link: {type:String, unique:true}
},{
  collection: 'BBC'
});

// the schema is useless so far
// we need to create a model using it
module.exports = mongoose.model('BBC', userSchema);