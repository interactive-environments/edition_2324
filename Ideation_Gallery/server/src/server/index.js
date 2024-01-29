"use strict";

const Promise = require("bluebird");
const mqttr = require("mqttr");
const distance = require("euclidean-distance");
const randomFromArray = require("just-random");
const { nanoid } = require("nanoid");

const { createOSCClient, createOSCServer } = require("../lib/osc");
const createLogServer = require("./log-server");
const makeRoutable = require("./routing");
const createSenders = require("./send-discovery");

function pickRandomByDistance(opts) {
	if (opts.length == 1) {
		return opts[0];
	}

	const total = opts.reduce((total, [_, d]) => total + d, 0);
	const random = Math.random() * total;

	let count = 0;
	return opts.find((opt) => {
		let [_, d] = opt;

		const picked = (count + total - d) >= random;
		count += (total - d);
		return picked;
	});
}

const { RawCodec } = require("mqttr/dist/codecs/raw");
const rawCodec = new RawCodec();

module.exports = function createServer(config, log) {
	const clientTracker = {};
	const mqtt = mqttr.connect(config.mqttServer, { clientId: `node-server-${nanoid(6)}`, codec: rawCodec });
	const oscClient = createOSCClient(log.extend("osc"));
	const oscServer = createOSCServer(log.extend("osc"));
	const nodes = makeRoutable(config.layout, log.extend("routing"));

	const { randomDiscoveryPoint } = createSenders(config, {
		clientTracker,
		oscClient,
		log: log.extend("osc")
	});

	mqtt.on("connect", () => {
		log("mqtt connected");
	});

	createLogServer(config, log.extend("logs"))();

	function sendrandom() {
		Promise.try(() => {
			const spiralNodes = Object.values(clientTracker).filter((node) => {
				return node.config.type == "spiral";
			});

			if (spiralNodes.length < 2) {
				return;
			}

			const sendNode = randomFromArray(spiralNodes);
			log("random pulse from %s", sendNode.id);
			// return randomDiscoveryPoint(sendNode, 0.2 + Math.random() * 0.2, 0.7 + Math.random() * 0.6);
			return randomDiscoveryPoint(sendNode, 0.2 + Math.random() * 0.25, 0.7 + Math.random() * 0.6);
		}).then(() => {
			// setTimeout(sendrandom, 3000 + 5000 * Math.random());
			setTimeout(sendrandom, 1600);
		});
	}

	setTimeout(() => {
		return sendrandom();
	}, 200);

	oscServer.addRoute("/discoveryPoint", (d, _rInfo) => {
		// type: iiifs
		const [x, y, z, intensity, nodeId] = d.args.map((a) => a.value);
		log("discovery near %d, %d, %d intensity %f1.1 (%s)", x, y, z, intensity, nodeId);

		let senderId = nodeId;
		let packetNode = nodes[nodeId];
		if (packetNode == undefined || packetNode.type != "spiral") {
			// assign different node as 'sending' node
			// pick from nearby online nodes
			let distances = Object.values(clientTracker).map((node) => {
				if (nodeId == node.id || node.config?.type != "spiral") {
					return null;
				}
				return [node.id, distance([node.config.x, node.config.y, node.config.z], [x, y, z])];
			}).filter((a) => a != null).sort((a, b) => a[1] - b[1]);

			if (distances.length == 0) {
				return log.error("no other nodes online, dropping /discoveryPoint");
			} else {
				// log("sender options: %o", distances);
			}

			const [_senderId, _targetDistance] = pickRandomByDistance(distances);
			log("changed sender node %s to %s", senderId, _senderId);
			senderId = _senderId;
		}

		const sendNode = clientTracker[senderId];
		if (sendNode == undefined) {
			log("sending node %s not in clientTracker, dropping discovery", senderId);
		}

		randomDiscoveryPoint(sendNode, intensity, 1.5);
	});

	return Promise.try(() => {
		return oscServer.listen(1212);
	}).then(() => {
		return mqtt.subscribe("/nodes/:id/online", (_topic, payload, msg) => {
			if (Buffer.isBuffer(payload)) {
				payload = payload.toString();
			}
			const id = msg.params.id;
			if (id == "server") { return; }

			const node = JSON.parse(payload);
			node.id = id;
			node.config = nodes[id];

			log("node %s online, %o", id, node);
			if (config.layout.nodes[id] == undefined) {
				log.error("Unknown client %s", id);
				return;
			}

			clientTracker[id] = node;
			oscClient.sendSkyClock2(node.osc.host, node.osc.port);

			if (nodes[id] != undefined) {
				mqtt.publish(
					`/nodes/${msg.params.id}/config`,
					JSON.stringify(config.layout.nodes[id]),
					{
						retain: true
					}
				);
			}
		});
	}).then(() => {
		mqtt.publish("/nodes/server/online", "").then(() => { log("published server online"); });
		const convertedTags = Object.fromEntries(
			Object.entries(config.layout.tags).map(([tag, color]) => {
				return [tag, parseInt(`0x${color.slice(1).toUpperCase()}`, 16)];
			})
		);
		mqtt.publish("/config/tags", JSON.stringify(convertedTags), { retain: true }).then(() => { log("published tags.json"); });
	});
};
