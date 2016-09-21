'use strict';
module.exports = function(sequelize, DataTypes) {
  var reviewSocial = sequelize.define('reviewSocial', {
    type: DataTypes.STRING(1)
  }, {
    classMethods: {
      associate: function(models) {
        reviewSocial.belongsTo(models.review);
      }
    }
  });
  return reviewSocial;
};