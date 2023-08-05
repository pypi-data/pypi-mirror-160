const RulesManager = require('./rules_manager');
const Constants = require('../utils/constants');
const HeartbeatCache = require('../reports/heartbeat_cache');
const Logger = require('../utils/logger');

function getRuntimeRules(data) {
    const resp = {};
    try {
        RulesManager.handleIncomingRules(data.data);
        const rules = RulesManager.runtimeRules;
        const appDeleted = RulesManager.isAppDeleted();
        const features = RulesManager.features
        resp['hooks'] = rules;
        resp['appDeleted'] = appDeleted;
        resp['features'] = features
        return resp;
    } catch (e) {
        Logger.write(Logger.DEBUG && `rules.getRuntimeRules: Failed error: ${e}`);
    }
    return {};
}

function getHeartbeatInfo(data) {
    try {
        const heartbeatInfo = {};
        heartbeatInfo[Constants.HEARTBEAT_HASH_KEY] = RulesManager.hash;
        const { agentId, workLoadId, reports, inventory, dynamicBom } = HeartbeatCache.flush();
        heartbeatInfo[Constants.HEARTBEAT_REPORT_KEY] = reports;
        heartbeatInfo[Constants.HEARTBEAT_INVENTORY_KEY] = inventory;
        heartbeatInfo[Constants.HEARTBEAT_WORKLOADID_KEY] = workLoadId;
        heartbeatInfo[Constants.HEARTBEAT_AGENTID_KEY] = agentId;
        heartbeatInfo[Constants.HEARTBEAT_DYNAMIC_BOM_KEY] = dynamicBom;
        return heartbeatInfo;
    } catch (e) {
        Logger.write(Logger.DEBUG && `rules.getHeartbeatInfo: Failed error: ${e}`);
    }
    return {}
}

module.exports = {
    getRuntimeRules: getRuntimeRules,
    getHeartbeatInfo: getHeartbeatInfo
}