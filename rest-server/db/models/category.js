'use strict';
module.exports = function(sequelize, DataTypes) {
  var category = sequelize.define('category', {
    code:Datatypes.STRING,
    first:Datatypes.STRING,
    second:Datatypes.STRING,
    third:Datatypes.STRING,
    bookCount:Datatypes.INTEGER,
  }, {
    classMethods: {
      associate: function(models) {
        category.belongsToMany(models.book,{through:'book_category'})
      }
    }
  });
  return category;
};