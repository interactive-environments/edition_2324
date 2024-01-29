"use strict";

const Promise = require("bluebird");
const shuffleArray = require("just-shuffle");
const randomFromArray = require("just-random");

const { getSkyClock, oscInt } = require("../lib/osc");

const LED_SPEED = 45;

module.exports = function createSenders(config, { clientTracker, oscClient, log }) {
	function randomDiscoveryPoint(sendNode, intensity, speed = 1) {
		let shuffledTags = shuffleArray(sendNode.config.tags);
		let recvNode, path;

		let onlineTargets = shuffleArray(Object.values(clientTracker).filter((node) => {
			return node.id != sendNode.id && node.config.type == "spiral";
		}));

		// pick 'receiving' node from online clients with same tag
		// let tag = randomFromArray(Object.keys(config.layout.tags));
		let tag = shuffledTags.find((tag_) => {
			// pick 'receiving' node from online clients with same tag
			recvNode = onlineTargets.find((node) => {
				if (node.config.tags?.includes(tag_)) {
					path = sendNode.config.routing[node.id];

					if (path != undefined) {
						return true;
					}

					log.error("no route from %s to %s, re-routing discoveryPoint", sendNode.id, node.id);
				}
				return false;
			});

			return recvNode != undefined; // first tag that has a receiver online
		});

		// tag = randomFromArray(Object.keys(config.layout.tags));

		if (tag == undefined) {
			return log.error("sendNode %s has no routes to matching tags, dropping discoveryPoint", sendNode.id);
		}

		return sendDiscoveryPath(sendNode, recvNode, path, tag, intensity, speed);
	}

	function sendDiscoveryPath(sendNode, recvNode, path, tag, intensity, speed = 1) {
		log("sending /discoveryPoint from %s to %s, tag '%s', intensity %d, speed %d", sendNode.id, recvNode.id, tag, intensity, speed);

		let time = getSkyClock();
		let failure = false;
		log("PATH %O", path);
		const packets = path.map((routeSection) => {
			const node = clientTracker[routeSection.nodeId];

			if (node == undefined) {
				log("/discoveryPoint section %s (in path from %s to %s) is offline, dropping discoveryPoint", routeSection.nodeId, sendNode.id, recvNode.id);
				failure = true;
				return null;
			}

			let recvTime = time + (LED_SPEED * speed) * Math.abs(routeSection.path[0] - routeSection.path[1]);
			log("section from %d:%d, distance %d, start %f end %f (%f)",
				routeSection.path[0],
				routeSection.path[1],
				Math.abs(routeSection.path[0] - routeSection.path[1]),
				time,
				recvTime,
				recvTime - time
			);

			const packet = {
				_id: node.id,
				host: node.osc.host,
				port: node.osc.port,
				payload: [
					tag,
					intensity,
					oscInt(time),
					oscInt(recvTime),
					oscInt(routeSection.path[0]),
					oscInt(routeSection.path[1])
				]
			};

			time = recvTime; // for next packet in chain
			return packet;
		});

		if (!failure) {
			return Promise.map(packets, ({ host, port, payload, _id }) => {
				log("sending %s (%s:%d) %d:%d", _id, host, port, payload[4].value, payload[5].value);
				return oscClient.send(
					host, port, "/discoveryPoint", payload
				);
			});
		}

	}

	return { randomDiscoveryPoint, sendDiscoveryPath };
};