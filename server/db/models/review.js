'use strict';
module.exports = function(sequelize, DataTypes) {
  var review = sequelize.define('review', {
    title:DataTypes.STRING,
    abstracts:DataTypes.TEXT,
    review:DataTypes.TEXT,
    facebook:{
      type:DataTypes.STRING,
      default:null
    }
  }, {
    classMethods: {
      associate: function(models) {
        review.belongsTo(models.book);
      }
    }
  });
  return review;
};