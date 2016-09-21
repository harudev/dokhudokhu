var Sequelize = require('sequelize');

var sequelize = new Sequelize('dokhudokhu', 'ruci', '13579', {
	host:'localhost',
	dialect:'postgres',
	pool : {
		max:5,
		min:0,
		idle:10000
	},
});
