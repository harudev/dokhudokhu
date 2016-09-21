'use strict';
module.exports = function(sequelize, DataTypes) {
  var book = sequelize.define('book', {
    isbn:DataTypes.STRING,
    title:DataTypes.STRING,
    author:DataTypes.STRING,
    publisher:DataTypes.STRING,
    primere:DataTypes.DATE,
    cover:DataTypes.STRING,
    link:DataTypes.STRING
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