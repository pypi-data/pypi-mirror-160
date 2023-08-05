const _ = require('lodash');
const Logger = require('../../../utils/logger');
const headerInjection = ["user-agent", "referer", "x-forwarded-for"]
const nosqlHelper = require("./nosqlHelper");

function _getObject(key, value) {
  const obj = {
    [key]: value
  }
  return JSON.stringify(obj, function (k, v) { return v === undefined ? "undefined" : v });
}


function _getTokens(object, tokens) {
  if (_.isEmpty(object)) {
    return tokens;
  }

  for (let [key, value] of Object.entries(object)) {
    if (_.isString(value)) {
      const parsed = _.parseIfJson(value);
      if (parsed) {
        value = parsed;
      }
    }
    if (_.isArray(value)) {
      for (let elem of value) {
        if (_.isObject(elem)) {
          tokens.push(_getTokens(elem, tokens));
        }
      }
      tokens.push(_getObject(key, value));
    }
    else if (_.isObject(value)) {
      _getTokens(value, tokens);
    } else {
      tokens.push(_getObject(key, value));
    };
  }
}

function _getMatchingTokens(queryObj, requestObj) {
  let result = [];
  for (const queryObjectEntry of queryObj) {
    const found = requestObj.find((requestObjectEntry) => requestObjectEntry === queryObjectEntry);
    if (found !== undefined) {
      result.push(found);
    }
  }
  return result;
}


function _parseBody(query, json) {
  try {
    const queryObj = JSON.parse(query);
    let queryObjectTokens = [];
    _getTokens(queryObj, queryObjectTokens);
    let requestObjectTokens = [];
    _getTokens(json, requestObjectTokens);
    return _getMatchingTokens(queryObjectTokens, requestObjectTokens);
  } catch (e) {
    Logger.write(Logger.DEBUG && `NoSqli:parseBody: failed with error: ${e}`);
  }
  return [];
}

function _parseQueryParametersAndHeaders(query, context) {
  let result = [];
  try {
    let parameters = context.parameter || {};
    let queryParamsResult = _parseQueryParameters(parameters, query);
    if (_.isArray(queryParamsResult) && queryParamsResult.length > 0) {
      result = result.concat(queryParamsResult);
    }
    let requestHeaderResult = _parseRequestHeaders(context.header, query);
    if (_.isArray(requestHeaderResult) && requestHeaderResult.length > 0) {
      result = result.concat(requestHeaderResult);
    }
  } catch (e) {
    Logger.write(Logger.DEBUG && `NoSqli:parseQueryParametersAndHeaders: failed with error: ${e}`);
  }
  return result;
}

function check(query, context) {
  context = nosqlHelper.toContext(context);
  let parsedValues = [];
  try {
    if (!_.isEmpty(context.json)) {
      let parsedBodyResult = _parseBody(query, context.json);
      if (_.isArray(parsedBodyResult) && parsedBodyResult.length > 0) {
        parsedValues = parsedValues.concat(parsedBodyResult);
      }
    }
    let parsedQueryParamsResult = _parseQueryParametersAndHeaders(query, context);
    if (_.isArray(parsedQueryParamsResult) && parsedQueryParamsResult.length > 0) {
      parsedValues = parsedValues.concat(parsedQueryParamsResult);
    }
  } catch (e) {
    Logger.write(Logger.ERROR && `NoSqli:check: failed with error: ${e}`);
  }
  return parsedValues;
}

function _parseRequestHeaders(headers, query) {

  let result = [];
  Object.keys(headers).forEach(function (name) {
    if (name.toLowerCase() == "cookie") {
      let cookies = _getCookies(headers.cookie)
      for (name in cookies) {
        result = result.concat(_isQueryContainsInput([cookies[name]], query));
      }
    }
    else if (headerInjection.indexOf(name.toLowerCase()) != -1) {
      result = result.concat(_isQueryContainsInput([headers[name]], query));
    }
  })
  return result;
}

function _getCookies(cookieStr) {
  let cookieItems = cookieStr.split(';')
  let result = {}
  for (let i = 0; i < cookieItems.length; i++) {
    let item = cookieItems[i].trim()
    if (item.length == 0) {
      continue
    }
    let keyLen = item.indexOf("=")
    if (keyLen <= 0) {
      continue
    }
    let key = unescape(item.substr(0, keyLen))
    let value = unescape(item.substr(keyLen + 1))
    result[key] = value

  }
  return result
}

function _parseQueryParameters(parameters, query) {
  let results = [];
  Object.keys(parameters).forEach(function (name) {
    var valueList = []
    Object.values(parameters[name]).forEach(function (value) {
      if (typeof value == 'string') {
        valueList.push(value)
      } else {
        valueList = valueList.concat(Object.values(value))
      }
    })
    results = results.concat(_isQueryContainsInput(valueList, query));
  })
  return results;
}

function _isQueryContainsInput(values, query) {
  let result = [];
  values.forEach(function (value) {
    if (query.includes(value)) {
      result.push(value);
    }
  });
  return result;
}

function parseDynamoDBData(data, context) {
  let matchingTokens = [];
  try {
    context = nosqlHelper.toContext(context);
    let queryTokens = [];
    if (data.KeyConditionExpression && data.ExpressionAttributeValues) {
      queryTokens = queryTokens.concat(nosqlHelper.processExpressionAttributeValues(data.KeyConditionExpression, data.ExpressionAttributeValues));
    }
    if (data.FilterExpression && data.ExpressionAttributeValues) {
      queryTokens = queryTokens.concat(nosqlHelper.processExpressionAttributeValues(data.FilterExpression, data.ExpressionAttributeValues));
    }
    if (data.ScanFilter) {
      queryTokens = queryTokens.concat(nosqlHelper.getTokensForFilterExpression(data.ScanFilter));
    }
    if (data.QueryFilter) {
      queryTokens = queryTokens.concat(nosqlHelper.getTokensForFilterExpression(data.QueryFilter));
    }
    if (data.KeyConditions) {
      queryTokens = queryTokens.concat(nosqlHelper.getTokensForFilterExpression(data.KeyConditions));
    }
    if (!_.isEmpty(context.json)) {
      let requestObjectTokens = [];
      nosqlHelper.getObjectValues(context.json, requestObjectTokens);
      matchingTokens = matchingTokens.concat(_getMatchingTokens(queryTokens, requestObjectTokens));
    }
    let parameters = context.parameter || {};
    let queryParameters = _getQueryParameters(parameters);
    if (_.isArray(queryParameters) && queryParameters.length > 0) {
      matchingTokens = matchingTokens.concat(_getMatchingTokens(queryTokens, queryParameters));
    }

    let header = context.header || {};
    let requestHeaders = _getRequestHeaders(header);
    if (_.isArray(requestHeaders) && requestHeaders.length > 0) {
      matchingTokens = matchingTokens.concat(_getMatchingTokens(queryTokens, requestHeaders));
    }
  } catch (e) {
    Logger.write(Logger.ERROR && `NoSqli:parseDynamoDBData: failed with error: ${e}`);
  }

  return matchingTokens;
}


function _getQueryParameters(parameters) {
  let results = [];
  Object.keys(parameters).forEach(function (name) {
    var valueList = []
    Object.values(parameters[name]).forEach(function (value) {
      if (typeof value == 'string') {
        valueList.push(value)
      } else {
        valueList = valueList.concat(Object.values(value))
      }
    })
    results = results.concat(valueList);
  })
  return results;
}

function _getRequestHeaders(headers) {
  let result = [];
  Object.keys(headers).forEach(function (name) {
    if (name.toLowerCase() == "cookie") {
      let cookies = _getCookies(headers.cookie)
      for (name in cookies) {
        result = result.concat([cookies[name]]);
      }
    }
    else if (headerInjection.indexOf(name.toLowerCase()) != -1) {
      result = result.concat([headers[name]]);
    }
  })
  return result;
}


module.exports = {
  check: check,
  parseDynamoDBData: parseDynamoDBData
}



