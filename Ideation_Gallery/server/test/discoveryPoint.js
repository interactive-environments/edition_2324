"use strict";

const Promise = require("bluebird");
const { createOSCClient, oscInt, getSkyClock } = require("../src/lib/osc");
const randomFromArray = require("just-random");
require("json5/lib/register");

const layout = require("../data/layout.json5");

Promise.map([...new Array(1)], () => {
	return Promise.try(() => {
		// let randomNode = randomFromArray(
		// 	// Object.entries(layout.nodes).filter(([k, n]) => n.type == "spiral" && n.staging).map(([k]) => k)
		// 	Object.entries(layout.nodes).filter(([k, n]) => n.type == "spiral").map(([k]) => k)
		// );

		// console.log("random node: %s", randomNode);

		// let node = layout.nodes[randomNode];

		// return new Promise((resolve) => {
		// 	osc.send("192.168.1.101", 1212, "/discoveryPoint", [
		// 		oscInt(node.x),
		// 		oscInt(node.y),
		// 		oscInt(node.z),
		// 		{ type: "float", value: 0.9 },
		// 		"virtual"
		// 	]).then(() => {
		// 		osc.close();
		// 		resolve();
		// 	});
		// });
		new Promise((resolve) => {
			const osc = createOSCClient();

			osc.send("192.168.1.117", 1212, "/discoveryPoint", [
				// randomFromArray(Object.keys(layout.tags)),
				"art",
				{ type: "float", value: 0.80 },
				oscInt(0),
				oscInt(getSkyClock() + (60 * 50)),
				oscInt(0),
				oscInt(121),
				// oscInt(20),
			]).then(() => {
				osc.close();
				resolve();
			});
		});
		return new Promise((resolve) => {
			const osc = createOSCClient();

			osc.send("192.168.1.117", 1212, "/discoveryPoint", [
				// randomFromArray(Object.keys(layout.tags)),
				"tech",
				{ type: "float", value: 0.80 },
				oscInt(0),
				oscInt(getSkyClock() + (60 * 50)),
				oscInt(121),
				oscInt(0),
				// oscInt(20),
			]).then(() => {
				osc.close();
				resolve();
			});
		});
	}).catch((e) => {
		console.error(e);
	});
}, { concurrency: 1 });
