"use strict";

const Promise = require("bluebird");
const path = require("node:path");
require("json5/lib/register");

const log = require("./src/lib/log");
const getMyIp = require("./src/lib/network");

const createServer = require("./src/server");
const createSimulatedClients = require("./src/simulated-clients");

// const SERVER_IP = "127.0.0.1";
const SERVER_IP = "192.168.1.101";

const config = {
	dataDir: path.join(__dirname, "data"),
	logPort: 1337,
	serverIp: SERVER_IP,
	localIp: getMyIp(SERVER_IP),
	mqttServer: `mqtt://${SERVER_IP}:1883`,
};

config.layout = require(path.join(config.dataDir, "/layout.json5"));

if (process.env.LOG_SERVER_ONLY == "1") {
	log("ONLY STARTING LOG SERVER");
	require("./src/server/log-server")(config, log.extend("logs"))();
	const mqtt = require("mqtt").connect(config.mqttServer);
	mqtt.on("connect", () => {
		mqtt.publish("/nodes/server/online", "");
		mqtt.end();
	});
} else {
	Promise.try(() => {
		return createServer(config, log.extend("server"));
	}).then(() => {
		// return createSimulatedClients(config, log.extend("virtual-clients"), 1);
	}).catch((e) => {
		log.error(e);
	});
}

