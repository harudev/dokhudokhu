'use strict';
module.exports = function(sequelize, DataTypes) {
  var category = sequelize.define('category', {
    code:DataTypes.STRING,
    first:DataTypes.STRING,
    second:DataTypes.STRING,
    third:DataTypes.STRING,
    bookCount:DataTypes.INTEGER,
  }, {
    classMethods: {
      associate: function(models) {
        category.belongsToMany(models.book,{through:'book_category'})
      }
    }
  });
  return category;
};