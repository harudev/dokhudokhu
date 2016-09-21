'use strict';
module.exports = function(sequelize, DataTypes) {
  var book = sequelize.define('book', {
    isbn:Datatypes.STRING,
    title:Datatypes.STRING,
    subTitle:Datatypes.STRING,
    author:Datatypes.STRING,
    publisher:Datatypes.STRING,
    primere:Datatypes.DATE,
    summary:Datatypes.TEXT,
    cover:Datatypes.STRING,
    link:Datatypes.STRING
  }, {
    classMethods: {
      associate: function(models) {
        book.belongsToMany(models.category,{through:'book_category'})
        book.hasMany(models.review)
      }
    }
  });
  return book;
};