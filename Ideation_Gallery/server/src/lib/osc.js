"use strict";

const Promise = require("bluebird");
const udp = require("node:dgram");
const osc = require("osc-min");

function oscInt(int) {
	return { type: "integer", value: int };
}

function getSkyClock() { // milliseconds since midnight
	let a = new Date();
	let b = new Date(a);
	return a - b.setHours(0, 0, 0, 0);
}

function createOSCClient(log) {
	const socket = udp.createSocket("udp4");
	function send(host, port, address, args) {

		return Promise.try(() => {
			return osc.toBuffer({
				address,
				args,
			});
		}).then((packet) => {
			return new Promise((resolve, reject) => {
				socket.send(packet, 0, packet.length, port, host, (err) => {
					if (err != null) {
						log.error(err);
						reject(err);
					} else {
						resolve();
					}
				});
			});
		});
	}

	function sendSkyClock2(host, port) {
		log("sending /skyClock2 to %s:%d", host, port);
		return send(host, port, "/skyClock2", oscInt(getSkyClock()));
	}

	function close() {
		socket.close();
	}

	return { send, close, sendSkyClock2 };
}

function createOSCServer(_log) {
	const log = _log.extend("osc");

	const routes = {};

	const server = udp.createSocket("udp4", (msg, rInfo) => {
		try {
			const decoded = osc.fromBuffer(msg);
			log("received %s from %s:%d", decoded, rInfo.address, rInfo.port);

			const matched = Object.keys(routes).some((r) => {
				if (r == decoded.address) {
					routes[r](decoded, rInfo);
					return true;
				}
				return false;
			});
			if (!matched) {
				log("%s matched no routes", decoded.address);
			}
		} catch (e) {
			log.error("decoding error %o", e);
		}
	});

	function listen(ip, port = undefined) {
		return new Promise((resolve, reject) => {
			server.on("error", reject);
			let args = [ip];
			if (port) {
				args = [port, ip];
			}
			return server.bind(...args, () => {
				const { port } = server.address();
				resolve(port);
			});
		});
	}

	function addRoute(r, callback) {
		routes[r] = callback;
	}

	return { server, listen, addRoute };
}

module.exports = {
	createOSCClient,
	createOSCServer,
	getSkyClock,
	oscInt
};