
const _ = require('lodash');
const Logger = require('../../../utils/logger');
const qs = require('qs');

const scanFilterComparisonOperatorRegex = new RegExp("GT|GE", 'i');


function _toParameters(context) {
  if (!context || (!context['queryParams'] && !context['pathParams'])) {
    return {};
  }

  const parameters = { ...context['pathParams'], ...context['queryParams'] };

  Object.keys(parameters).forEach((key) => {
    if (_.isString(parameters[key])) {
      // open rasp expects each parameter to be an array of strings
      parameters[key] = [parameters[key]];
    }
  });
  return parameters;
}

function _toJson(context) {
  if (!context) {
    return {};
  }

  const contentTypeHeader = context && context['requestHeaders'] && _.getObjectKeysToLower(context['requestHeaders'], 'content-type');
  if (_.isValidJsonRequest(contentTypeHeader) || _.isGraphqlRequest(context.protocol)) {
    if (!_.isString(context['requestBody'])) {
      return {};
    }

    const parsedBody = _.parseIfJson(context['requestBody']);;

    if (!parsedBody) {
      return {};
    }

    return parsedBody;
  }

  if (_.isValidEncodedFormDataRequest(contentTypeHeader)) {
    if (!_.isString(context['requestBody'])) {
      return {};
    }

    return qs.parse(context['requestBody']);
  }

  if (_.isValidMultipartFormDataRequest(contentTypeHeader)) {
    if (!_.isObject(context['formData']) || !_.isObject(context['formData']['fields'])) {
      return {};
    }
    return context['formData']['fields'];
  }

  if (_.isString(context['requestBody'])) {
    return {
      body: context['requestBody']
    };
  }

  return {};
}

function _headerKeysToLower(context) {
  if (!context || !context['requestHeaders']) {
    return {};
  }

  const headers = {};
  Object.keys(context['requestHeaders']).forEach((key) => {
    headers[key.toLowerCase()] = context['requestHeaders'][key];
  });

  return headers;
}

function toContext(context) {
  try {
    const server = {
      os: process.platform
    };
    return {
      header: _headerKeysToLower(context),
      parameter: _toParameters(context),
      url: (context && context['url']) || '',
      json: _toJson(context)
    };
  } catch (e) {
    Logger.write(Logger.ERROR && `toContext: error : ${e}`);
  }
  return {};
}

function getTokensForFilterExpression(scanResults) {

  if (scanResults) {
    let results = [];
    _processObjectForFilterExpression(scanResults, results);
    return _processFilterExpressionOutput(results);
  } else {
    return [];
  }

}

function _processFilterExpressionOutput(result) {
  let tokens = [];
  result.forEach(entry => {
    for (const [key, value] of entry.entries()) {
      if (scanFilterComparisonOperatorRegex.test(key)) {
        value.forEach(obj => {
          for (let [key, value] of Object.entries(obj)) {
            if (key === 'S') {
              tokens.push(value);
            }
          }
        });
      }
    }
  })
  return tokens;
}

function _processObjectForFilterExpression(object, result) {

  let attrVales = [];
  let operator = "";
  for (let [key, value] of Object.entries(object)) {
    if (key === 'AttributeValueList') {
      attrVales = attrVales.concat(value);
    } else if (key === 'ComparisonOperator') {
      operator = value;
    } else if (_.isObject(value)) {
      _processObjectForFilterExpression(value, result);
    }
  }
  if (operator && attrVales.length > 0) {
    let operatorAttributeValuesMap = new Map();
    operatorAttributeValuesMap.set(operator, attrVales);
    result.push(operatorAttributeValuesMap)
  }

}

function getObjectValues(object, tokens) {
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
          tokens.push(getObjectValues(elem, tokens));
        }
      }
      tokens.push(value);
    }
    else if (_.isObject(value)) {
      getObjectValues(value, tokens);
    } else {
      tokens.push(value);
    };
  }
}

function _getTokensForExpression(filterExpression) {
  let isGreaterThanOrEqualToFound = false;
  const filterExpressionTokens = filterExpression.split(" ");
  let tokens = [];

  for (const tokenEntry of filterExpressionTokens) {

    if (isGreaterThanOrEqualToFound) {
      tokens.push(tokenEntry);
      isGreatherThanOrEqualTo = false;
    }

    if (tokenEntry === '>' || tokenEntry === '>=') {
      isGreaterThanOrEqualToFound = true;
    }

  }
  return tokens;
}

function _getMatchingTokensForExpressionAttributeValues(filterExpressionTokens, expressionAttributeValues) {

  let matchingTokens = [];
  for (let [key, value] of Object.entries(expressionAttributeValues)) {

    const tokenIndex = filterExpressionTokens.findIndex((filterExpression) => filterExpression === key);
    if (tokenIndex !== -1) {
      if (_.isString(value)) {
        matchingTokens.push(value);
      } else if (_.isObject(value)) {
        for (let [filterExpressionKey, filterExpressionValue] of Object.entries(value)) {
          if (filterExpressionKey === 'S') {
            matchingTokens.push(filterExpressionValue);
          }
        }
      }

    }
  }
  return matchingTokens;
}


function processExpressionAttributeValues(expression, expressionAttributeValues) {

  const expressionTokens = _getTokensForExpression(expression);
  const matchingTokens = _getMatchingTokensForExpressionAttributeValues(expressionTokens, expressionAttributeValues);
  return matchingTokens;
}

module.exports = {
  toContext: toContext,
  getTokensForFilterExpression: getTokensForFilterExpression,
  getObjectValues: getObjectValues,
  processExpressionAttributeValues: processExpressionAttributeValues
}