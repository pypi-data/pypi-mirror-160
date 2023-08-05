const _ = require('lodash');
const Constants = require('../utils/constants');
const { Route, Inventory, Api } = require('./inventory');
const bom_helper = require('../modules/bom/bom_helper');

class HeartbeatCache {
  constructor() {
    this._cache = {
      reports: {},
      inventory: {},
      staticBom: [],
      dynamicBom: [],
      graphqlEndpoints: [],
      isRouteSentToBackend: false
    };
    this._appName = "";
  }

  cacheGraphqlEndpoint(graphqlEndpoint) {
    if (graphqlEndpoint !== '/') {
      graphqlEndpoint = graphqlEndpoint.replace(
        Constants.PATH_TRIMMING_REGEX,
        ''
      );
    }
    this._cache.graphqlEndpoints = Array.from(new Set([...this._cache.graphqlEndpoints, graphqlEndpoint]));
    this._cache.isRouteSentToBackend = false;
  }

  isGraphqlRequest(requestPath) {
    return this._cache.graphqlEndpoints.includes(requestPath);
  }

  cacheDynamicBom(dynamicBom, appName) {
    if (!this._appName) {
      this._appName = appName;
    }
    this._cache.dynamicBom.push(dynamicBom);
  }

  cacheInventory(inventory) {
    this._cache.inventory = inventory;
    this._cache.isRouteSentToBackend = false;
  }

  getInventory() {
    return this._cache.inventory;
  }

  cacheReportEvents(report) {
    if (!this._cache.reports[report.requestId]) {
      this._cache.reports[report.requestId] = report;
    } else {
      this._cache.reports[report.requestId].events.push(...report.events);
    }
  }

  cacheReport(report) {
    this._cache.reports[report.requestId] = report;
  }

  getReport(requestId) {
    return this._cache.reports[requestId] || null;
  }

  flush() {
    const reports = [];
    for (let requestId in this._cache.reports) {
      const report = this._cache.reports[requestId];
      if (report.isClosed()) {
        const securityActivity = report.getJson();
        if ((_.isArray(securityActivity.events) && !_.isEmpty(securityActivity.events)) || securityActivity.hasApiData) {
          delete securityActivity.hasApiData;
          reports.push(securityActivity);
        }
        delete this._cache.reports[requestId];
      }
    }
    if (!this._cache.isRouteSentToBackend) {
      this._cache.inventory = this._populateInventoryForGraphqlRoutes(this._cache.inventory, this._cache.graphqlEndpoints);
    }
    const inventory = this._cache.inventory;
    this._cache.inventory = {};
    let dynamicBom = [];
    if (this._cache.dynamicBom && this._cache.dynamicBom.length > 0) {
      dynamicBom = bom_helper.processDynamicBom(this._cache.dynamicBom, this._appName);
      this._cache.dynamicBom = [];
    }
    this._cache.isRouteSentToBackend = true;

    return {
      reports,
      inventory,
      [Constants.HEARTBEAT_DYNAMIC_BOM_KEY]: dynamicBom,
    };
  }

  setClosed(id) {
    if (this._cache.reports[id]) {
      this._cache.reports[id].setClosed();
    }
  }

  _populateInventoryForGraphqlRoutes(inventory, graphqlRoutes) {
    let paths = [];
    let host = undefined;
    let routes = [];
    if (_.isArray(graphqlRoutes)) {
      if (_.isObject(inventory) && _.isObject(inventory.api) && _.isArray(inventory.api.routes)) {
        routes = inventory.api.routes.map((route) => {
          paths.push(route.path);
          host = route.host;
          if (graphqlRoutes.includes(route.path)) {
            route.isGraphqlRoute = true;
          }
          return route;
        });
      }

      graphqlRoutes.forEach((graphqlRoute) => {
        if (!paths.includes(graphqlRoute)) {
          routes.push(new Route(graphqlRoute, ['POST'], host, true));
        }
      });
    }
    if (_.isObject(inventory) && _.isObject(inventory.api) && _.isArray(inventory.api.routes)) {
      inventory.api.routes = routes;
      return inventory;
    }
    return new Inventory(new Api(routes));
  }
}

module.exports = new HeartbeatCache();
