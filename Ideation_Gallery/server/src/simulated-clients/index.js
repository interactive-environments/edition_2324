"use strict";

const Promise = require("bluebird");
const mqttr = require("mqttr");

const { createOSCClient, createOSCServer } = require("../lib/osc");

class SkyClock {
	constructor() {
		this.clock = 0;
		this.lastUpdate = 0;
	}

	receiveSkyClock2({ args }) {
		this.lastUpdate = new Date() / 1000;
		this.clock = args[0].value / 10000;
	}

	get() {
		return this.clock + (((new Date() / 1000) - this.lastUpdate) / 10000);
	}
}

function createClient(_config, id, log) {
	const mqtt = mqttr.connect(_config.mqttServer, { clientId: id });
	const oscClient = createOSCClient();
	const oscServer = createOSCServer(log, () => { });

	const config = {};
	const sky = new SkyClock();

	oscServer.addRoute("/skyClock2", sky.receiveSkyClock2);

	function sendDiscovery() {
		return oscClient.send(config.serverIp, 1212, "/discoveryPoint", [
			{ type: "integer", value: config.x },
			{ type: "integer", value: config.y },
			{ type: "integer", value: config.z },
			{ type: "integer", value: 0 }, // art
			{ type: "string", value: id }
		]);
	}

	return Promise.try(() => {
		return oscServer.listen(_config.localIp).then((port) => {
			log("listening on %s:%d", _config.localIp, port);
			return port;
		});
	}).then((oscPort) => {
		mqtt.subscribe(`/nodes/${id}/config`, (_topic, payload, _msg) => {
			const newConf = JSON.parse(payload);
			log("received new config %o", newConf);
			Object.assign(config, newConf);
		});

		return mqtt.publish(`/nodes/${id}/online`, `${_config.localIp}:${oscPort}`);
	}).then(() => {
		setInterval(() => {
			if (id == "virtual-0") {
				log("sending discoveryPoint");
				sendDiscovery();
			}
		}, 5000);
	}).catch((e) => {
		log.error(e);
	});
}

module.exports = function createSimulatedClients(config, log, amount = 1) {
	return Promise.map([...new Array(amount)], (_, i) => {
		const name = `virtual-${i}`;
		log("starting", name);
		return createClient(config, name, log.extend(name));
	});
};
