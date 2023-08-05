const Logger = require('../../utils/logger');

function processDynamicBom(dynamicBom, rootAppName) {

  try {
    let dynamicBomModules = []
    let dynamicBomModulesToSkip = []

    let modulesNames = [];
    let uniqModuleNames = new Set();
    let uniqueDynamicBom = []
    dynamicBom.forEach(element => {
      if (element.name && !uniqModuleNames.has(element.name)) {
        uniqModuleNames.add(element.name);
        modulesNames.push({ "moduleName": element.name, "modulePath": _getRelativePath(element.modulePath, rootAppName) });
        uniqueDynamicBom.push(element);
      }
    });
    uniqModuleNames.clear();
    dynamicBom = [];

    let sizeToModulesToSkipMap = new Map();
    for (let dynamicBomEntry of uniqueDynamicBom) {
      let masterModuleSet = new Set()
      let masterModuleSetToSkip = new Set()
      let stackFrames = []

      dynamicBomEntry.stackTrace.forEach((stackTraceObject) => {
        let stackTraceMatch = false;
        for (let module of modulesNames) {
          if (stackTraceObject.fileName.lastIndexOf('/') !== -1 && _getPathWoFileName(stackTraceObject.fileName).indexOf(module.moduleName) !== -1) {
            masterModuleSet.add(module)
            if (dynamicBomEntry.name !== module) {
              masterModuleSetToSkip.add(module)
            }
            stackTraceMatch = true;
            stackTraceObject.fileName = _getRelativePath(stackTraceObject.fileName, rootAppName);
            stackFrames.push(stackTraceObject)
            break;
          }
        }
        if (!stackTraceMatch) {
          stackTraceObject.fileName = _getRelativePath(stackTraceObject.fileName, rootAppName);
          stackFrames.push(stackTraceObject)
        }
      })
      masterModuleSet = _insertRootModuleIfRequired(masterModuleSet, dynamicBomEntry, rootAppName);

      if (masterModuleSet.size === 0) {
        stackFrames = stackFrames.concat(dynamicBomEntry.stackTrace)
      } else {
        let dynamicBomModulesToSkipWithSameSize = _processModulesOfSameLengthFromMap(sizeToModulesToSkipMap, masterModuleSetToSkip.size, dynamicBomModulesToSkip);

        if (!_isModuleExists(dynamicBomModulesToSkipWithSameSize, masterModuleSetToSkip)) {
          dynamicBomModulesToSkip.push(masterModuleSetToSkip)
        }
      }
      let dynamicBomEntryObj = {
        "modules": masterModuleSet,
        "stackTrace": stackFrames
      }
      dynamicBomModules.push(dynamicBomEntryObj)
    }
    let filteredDynamicBomModules = [];
    sizeToModulesToSkipMap.clear();

    for (let dynamicBomModuleEntry of dynamicBomModules) {
      let filteredModulesToSkip = _processModulesOfSameLengthFromMap(sizeToModulesToSkipMap, dynamicBomModuleEntry.modules.size, dynamicBomModulesToSkip);

      if (!_isModuleExists(filteredModulesToSkip, dynamicBomModuleEntry.modules)) {
        filteredDynamicBomModules = filteredDynamicBomModules.concat(dynamicBomModuleEntry);
      }
    }
    _formatDynamicBomModules(filteredDynamicBomModules);
    return filteredDynamicBomModules;

  } catch (e) {
    Logger.write(Logger.INFO && `Error in processDynamicBom: ${e}`);
    return []
  }

}


function _processModulesOfSameLengthFromMap(sizeToModulesMap, moduleSize, modulesToSearchIn) {

  let filteredModulesToSearch = []
  if (sizeToModulesMap.has(moduleSize)) {
    filteredModulesToSearch = sizeToModulesMap.get(moduleSize);
  } else {
    filteredModulesToSearch = _filterModules(modulesToSearchIn, moduleSize);
    sizeToModulesMap.set(moduleSize, filteredModulesToSearch);
  }
  return filteredModulesToSearch;
}

function _formatDynamicBomModules(filteredDynamicBomModules) {

  filteredDynamicBomModules.forEach((entry) => {
    let line = entry.stackTrace.map((stackTraceEntry) => {
      return ((stackTraceEntry.fileName ? stackTraceEntry.fileName : '') + (stackTraceEntry.lineNumber ? ":" + stackTraceEntry.lineNumber : '') + (stackTraceEntry.columnNumber ? ":" + stackTraceEntry.columnNumber : ''))
    })
    entry.stackTrace = line

    let modulesArray = [...entry.modules]
    entry.modules = modulesArray
  });

}

function _insertRootModuleIfRequired(masterModuleSet, dynamicBomEntry, rootAppName) {
  const masterModuleSetArray = [...masterModuleSet]
  let index = masterModuleSetArray.findIndex((entry) => entry.moduleName === dynamicBomEntry.name)
  if (index === -1) {
    masterModuleSetArray.splice(0, 0, { "moduleName": dynamicBomEntry.name, "modulePath": _getRelativePath(dynamicBomEntry.modulePath, rootAppName) });
    masterModuleSet = new Set(masterModuleSetArray)
  }
  return masterModuleSet;
}


function _filterModules(modulesToFilter, moduleSize) {

  let filteredModules = modulesToFilter.filter(function (dynamicBomModulesToSkipEntry) {
    return _isSize(dynamicBomModulesToSkipEntry, moduleSize);
  });
  return filteredModules;
}

function _isSize(element, size) {
  return element.size === size
}


function _isModuleExists(dynamicBomModulesToSearchIn, masterModuleSetToSearchFor) {

  for (let dynamicModulesToSearchSet of dynamicBomModulesToSearchIn) {
    let masterModuleSetExists = true;
    let moduleNames = []
    dynamicModulesToSearchSet.forEach((setObj) => {
      moduleNames.push(setObj.moduleName);
    })
    for (let module of masterModuleSetToSearchFor) {
      if (!moduleNames.includes(module.moduleName)) {
        masterModuleSetExists = false;
        break;
      }
    }
    if (masterModuleSetExists) {
      return true;
    }
  }
  return false;
}

function _getRelativePath(fileName, rootAppName) {

  if (fileName.indexOf(rootAppName) !== -1) {
    let substringIndex = fileName.indexOf(rootAppName) + rootAppName.length;
    fileName = fileName.substring(substringIndex);
  }
  return fileName;
}

function _getPathWoFileName(fileName) {
  let lastIndexOfForwardSlash = fileName.lastIndexOf('/');
  return (lastIndexOfForwardSlash !== -1 ? fileName.substring(0, lastIndexOfForwardSlash) : fileName);
}

module.exports = { processDynamicBom: processDynamicBom }