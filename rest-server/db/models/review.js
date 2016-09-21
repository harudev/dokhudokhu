'use strict';
module.exports = function(sequelize, DataTypes) {
  var review = sequelize.define('review', {
    title:Datatypes.STRING,
    abstracts:Datatypes.TEXT('tiny'),
    review:Datatypes.TEXT,
    facebook:{
      type:Datatypes.STRING,
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