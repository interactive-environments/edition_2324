"use strict";

const { networkInterfaces } = require("node:os");
const cidr = require("cidr-tools");
const nets = networkInterfaces();

module.exports = function getMyIp(serverIp) {
	let MY_IP;

	Object.values(nets).some((iface) => {
		return iface.some((addr) => {
			if (cidr.contains(addr.cidr, serverIp)) {
				MY_IP = addr.address;
				return true;
			}
			return false;
		});
	});

	return MY_IP;
};