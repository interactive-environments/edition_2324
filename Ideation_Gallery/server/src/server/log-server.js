"use strict";

const fs = require("node:fs");
const net = require("node:net");
const path = require("node:path");

module.exports = function ({ logPort, dataDir }, log) {
	const logPath = path.join(dataDir, "logs");
	fs.mkdirSync(logPath, { recursive: true });
	const defaultLog = fs.createWriteStream(path.join(logPath, "unknown"), { flags: "a" });

	const server = net.createServer({ allowHalfOpen: false }, (c) => {
		let node;
		let logFile = defaultLog;
		c.setEncoding("utf8");
		// c.setKeepAlive(true); // keepAlive 10 seconds
		c.on("error", log.error);

		log("connected: %s", c.remoteAddress);

		c.on("data", (data) => {
			const lines = data.replace(/\x00/g, "").split("\r\n");
			if (node == undefined) {
				const containsHost = lines.some((line) => {
					if (line.startsWith("++connect:")) {
						node = path.normalize(line.trim().split("++connect: ")[1]);
						if (node == ".") {
							node = undefined;
						}
						return true;
					}
					return false;
				});

				if (containsHost) {
					logFile = fs.createWriteStream(path.join(logPath, node), { flags: "a" });
				}

				// fs.writeSync(logFile, lines.join("\r\n"));
				// } else {
				// fs.writeSync(logFile, data);
			}

			let ts = getTimestamp();
			lines.forEach((l) => {
				if (l.trim() != "") {
					logFile.write(`${ts} ${l}\n`);
				}
			});
		});

		c.on("close", () => {
			log("%s disconnected (%s)", node, c.remoteAddress);
			if (node != undefined) {
				logFile.write("++disconnect\r\n", () => {
					logFile.close();
				});
			}
		});
	});

	server.on("error", (e) => log.error(e));

	return function start() {
		server.listen(logPort, () => {
			log(
				"logging server listening on %s:%d",
				server.address().address,
				server.address().port
			);
		});
	};
};

function getTimestamp() {
	let d = new Date();
	return `${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}:${d.getSeconds().toString().padStart(2, "0")}.${d.getMilliseconds().toString().padStart(3, "0")}`;
}
