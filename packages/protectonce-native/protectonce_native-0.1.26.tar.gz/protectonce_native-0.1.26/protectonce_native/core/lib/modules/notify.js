const Logger = require('../utils/logger');
const HeartbeatCache = require('../reports/heartbeat_cache');

function notify(data) {
  try {
    if (data.key === 'BOM.usedModule') {
      HeartbeatCache.cacheDynamicBom(data.args[0], data.args[1]);
    }
  } catch (e) {
    Logger.write(Logger.ERROR && `Error in notify method : ${e}`);
  }
}
module.exports = notify