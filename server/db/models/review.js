'use strict';
module.exports = function(sequelize, DataTypes) {
  var review = sequelize.define('review', {
    title:DataTypes.STRING,
    abstracts:DataTypes.TEXT,
    review:DataTypes.TEXT,
    facebook:DataTypes.STRING
  }, {
    classMethods: {
      associate: function(models) {
        review.belongsTo(models.user);
        review.belongsTo(models.book);
        review.hasMany(models.reviewSocial);
      }
    }
  });
  return review;
};