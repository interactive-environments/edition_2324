"use strict";

module.exports = function makeRoutable(layout, log) {
	const nodes = Object.fromEntries(
		Object.entries(layout.nodes).map(([nodeId, node]) => {
			let llog = log.extend(nodeId);
			let routes = [];
			Object.entries(layout.groups).forEach(([groupName, { branches }]) => {
				if (branches.includes(nodeId)) {
					routes.push({ type: "groups", name: groupName, path: [] });
				}
			});

			llog("groups: %O", routes);

			Object.entries(layout.rails).forEach(([railName, rail]) => {
				llog("checking rail %s, current routes: %O", railName, routes);
				if (routes.some((r) => {
					return r.type == "rails" && r.name == railName;
				})) {
					return;
				}

				let { network } = rail;
				if (network[nodeId]) {
					llog("direct connection to %s", railName);
					return routes.push({ type: "rails", name: railName, stationId: nodeId, path: [] });
				}

				routes.some((route) => {
					llog("checking existing route %O against %s", route, railName);
					const { type, name } = route;
					let path = [];
					let routeId = `${type}-${name}`;
					if (network[routeId]) {
						llog("in network", railName);
						if (type == "rails") {
							llog("  %s is rail", routeId);
							let otherRail = layout.rails[name];
							path.push({ nodeId: otherRail.node, path: [otherRail.network[`rails-${railName}`], otherRail.network[route.stationId]] });
						}
						return routes.push({ type: "rails", name: railName, stationId: routeId, path });
					}
					return false;
				});
				llog("routes: %O", routes);
			});

			return [
				nodeId,
				{
					type: node.type ?? "spiral",
					id: nodeId,
					routes,
					routing: {},
					...node
				}
			];
		})
	);

	const nodeValues = Object.values(nodes);

	nodeValues.forEach((node) => {
		if (node.type != "spiral") { return null; }

		const routeMap = nodeValues.map((otherNode) => {
			if (node.id == otherNode.id || otherNode.type != "spiral") { return null; }
			if (otherNode.routing[node.id]) {
				let reversed = [...otherNode.routing[node.id]].reverse().map((route) => {
					return {
						...route,
						path: [...route.path].reverse()
					};
				});
				// reverse path, return
				return [otherNode.id, reversed];
			}

			if (node.id == "node-FD-8C" && otherNode.id == "node-FF-B8") {
				const util = require("util");
				console.log("FD-8C:", util.inspect(node.routes, { depth: Infinity }));
				console.log("FF-B8:", util.inspect(otherNode.routes, { depth: Infinity }));
			}

			let commonRoute;
			node.routes.some((route) => {
				otherNode.routes.some((otherRoute) => {
					if (route.type == otherRoute.type && route.name == otherRoute.name) {
						let path = [...route.path];

						if (route.type == "rails") {
							let rail = layout.rails[route.name];
							path.push({ nodeId: rail.node, path: [rail.network[route.stationId], rail.network[otherRoute.stationId]] });
						}
						path.push(...[...otherRoute.path].reverse());
						commonRoute = { type: route.type, name: route.name, path };
					}
					return commonRoute != undefined;
				});
				return commonRoute != undefined;
			});

			if (commonRoute == undefined) {
				log.error(
					"nodes %s [%s] and %s [%s] have no path",
					node.id, JSON.stringify(node.routes),
					otherNode.id, JSON.stringify(node.routes)
				);
				return null;
			}

			log("nodes %s, %s have common route through %s (%o)", node.id, otherNode.id, commonRoute.name, commonRoute.path);
			const fullPath = [
				{
					nodeId: node.id,
					path: node.reversed
						? [node.leds, 0]
						: [0, node.leds]
				},
				...commonRoute.path,
				{
					nodeId: otherNode.id,
					path: otherNode.reversed
						? [0, otherNode.leds]
						: [otherNode.leds, 0]
				}
			];

			log("full path %o", fullPath);

			return [otherNode.id, fullPath];
		}).filter((a) => a != null);

		node.routing = Object.fromEntries(routeMap);
	});

	nodeValues.forEach((node) => {
		if (node.type != "spiral") { return; }
		log("node %s", node.id);
		Object.entries(node.routing).forEach(([otherNode, route]) => {
			log("  to %s: %o", otherNode, route);
		});
	});

	return nodes;
};

// require("json5/lib/register");
// const layout = require("../../data/layout.json5");
// const log = require("debug")("routing");
// log.error = log.extend("error");
// require("debug").enable("routing*");

// module.exports(layout, log);