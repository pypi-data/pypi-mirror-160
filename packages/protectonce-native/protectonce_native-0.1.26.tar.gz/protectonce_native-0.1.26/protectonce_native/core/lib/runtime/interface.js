const rasp = require('../modules/rasp');
const waf = require('../modules/waf');
const httpServer = require('../modules/httpServer');
const userMonitoring = require('../modules/userMonitoring');
const reporting = require('../modules/reporting');
const api = require('../modules/api');
const rulesManagerInterface = require('../rules/rules_manager_interface');
const notify = require('../modules/notify');
function stop() {
    // TODO: Implement this method and add cleanup if any
    return null;
}

function sync() {
    // TODO: Implement this method
    return null;
}

module.exports = {
    userMonitoring: userMonitoring,
    rasp: rasp,
    waf: waf,
    httpServer: httpServer,
    reporting: reporting,
    api: api,
    coreInterface: rulesManagerInterface,
    stop: stop,
    notify: notify
};
