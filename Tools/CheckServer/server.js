const express = require('express')
const asyncHandler = require('express-async-handler')
const SteamUser = require('steam-user');
const GlobalOffensive = require('globaloffensive');
// accounts_info.js ->
// const accounts = [
// 	{login:'acc_login', pass:'acc_pass'}
// ];
// module.exports = {accounts};
const {accounts} = require('./accounts_info.js')


const active_accounts = []


function loginToAccounts() {
	for (var account of accounts) {
	    (function(account) {
	    	console.log("Login to " + account["login"]);
	    	var client = new SteamUser();
	    	var csgo = new GlobalOffensive(client);

	    	client.logOn({
	            "accountName": account["login"],
	            "password": account["pass"]
	        });

	        client.on('loggedOn', function(details) {
	            console.log("Logged into Steam as " + account["login"]);
	            client.setPersona(SteamUser.EPersonaState.Online);
	            client.gamesPlayed([730]);
	            console.log("Set CSGO " + account["login"]);
	        });


            csgo.on('connectedToGC', function() {
                console.log("Connected to CSGO " + account["login"]);
                active_accounts.push(csgo);
            });

	    })(account);
	}
}



loginToAccounts();

var bot_id = 0
const app = express();


app.get('/', asyncHandler(async (req, res, next) => {
	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify({"Desk": "NodeJS Server Active", "bots_online": active_accounts.length}));
}))


app.get('/getinfo', asyncHandler(async (req, res, next) => {
	let code1 = req.query.code1;
	let code2 = req.query.code2;
	let url = `steam://rungame/730/${code1}/+csgo_econ_action_preview%${code2}`;

	if (bot_id > active_accounts.length - 1) {
		bot_id = 0
	}

	let csgo = active_accounts[bot_id]
	bot_id = bot_id + 1

	console.log("Send new request to CSGO Bot_Id: " + bot_id);
	await csgo.inspectItem(url, (callback) => {
						console.log("Get response from CSGO Bot_Id: " + bot_id)
						res.setHeader('Content-Type', 'application/json');
						res.end(JSON.stringify(callback));
					});
}))


console.log("Start server on 3000 port.")
app.listen(3000);
