'use strict';
module.exports = function(sequelize, DataTypes) {
  var user = sequelize.define('user', {
    email:DataTypes.STRING,
    nickname:DataTypes.STRING,
    name:DataTypes.STRING,
    password:DataTypes.STRING,
    fg_photo:DataTypes.STRING,
    bg_photo:DataTypes.STRING,
    facebook:DataTypes.STRING,
  }, {
    classMethods: {
      associate: function(models) {
        user.hasMany(models.review)
      }
    }
  });
  return user;
};