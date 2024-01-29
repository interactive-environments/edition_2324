"use strict";

const debugLib = require("debug");

const PROJECT = "virtual-client";

let debugEnv = process.env.DEBUG;
if (debugEnv == undefined) {
	debugEnv = "";
}
debugLib.enable(`${debugEnv},${PROJECT}*`);

const log = debugLib(PROJECT);
log._name = PROJECT;
log.debug = log.extend("debug");
log.error = log.extend("error");
log.extend = function extend(name) {
	let newLog = debugLib(this._name).extend(name);
	newLog._name = `${this._name}:${name}`;
	newLog.debug = newLog.extend("debug");
	newLog.error = newLog.extend("error");
	return newLog;
};

module.exports = log;
