import { rootStore } from '@/stores/rootStore';

// 组件拖入视图前置操作
export const beforeComponentEnterView = (component) => {
  // 拖入时右侧面板默认展开属性名定义
  component.collapseName = 'varName'
  return component
}

function getUniqueKey(obj, key) {
  let originalKey = key;
  let count = 1;
  while (obj.hasOwnProperty(key)) {
      key = originalKey + count;
      count++;
  }
  return key
}

export const updateVarName = (varName) => {
  let originalComponentStateName = rootStore.dataCenter.curComponent.componentStateName
  let newComponentStateName = getUniqueKey(rootStore.dataConfig.stateSet, varName)
  rootStore.dataConfig.addState(newComponentStateName, rootStore.dataConfig.stateSet[originalComponentStateName])
  rootStore.dataCenter.curComponent.componentStateName = newComponentStateName
  buildDataBinds(rootStore.dataCenter.curComponent, newComponentStateName)
  delete rootStore.dataConfig.stateSet[originalComponentStateName]
}

function getUniqueActionKey(obj, key, language = '@julia') {
  let originalKey = key;
  let count = 1;
  while (obj.hasOwnProperty(`${key}${language}`)) {
      key = originalKey + count;
      count++;
  }
  return key
}

// 默认支持julia
export const updateCallback = (callbackForm, language) => {
  // 语言后缀标识
  let languageSign = {Julia: '@julia', Python: '@python', Javascript: ''}[language]
  if (callbackForm.mode === 'new') {
    let actionKey = getUniqueActionKey(rootStore.dataConfig.actionSet, `${rootStore.dataCenter.curComponent.component}_${callbackForm.key}`, languageSign)
    rootStore.dataConfig.addAction(`${actionKey}${languageSign}`, callbackForm.code)
    rootStore.dataCenter.curComponent.actionBinds[callbackForm.key] = `${actionKey}${languageSign}`
  } else {
    let actionKey = rootStore.dataCenter.curComponent.actionBinds[callbackForm.key]
    let actionKeySuffix = actionKey.split('@').pop();
    let languageSwitch = {julia: 'Julia', python: 'Python'}[actionKeySuffix] || 'Javascript'
    // 语言切换 重新绑定
    if(language != languageSwitch) {
      let newActionKey = getUniqueActionKey(rootStore.dataConfig.actionSet, `${rootStore.dataCenter.curComponent.component}_${callbackForm.key}`, languageSign)
      rootStore.dataConfig.addAction(`${newActionKey}${languageSign}`, callbackForm.code)
      rootStore.dataConfig.deleteAction(actionKey)
      rootStore.dataCenter.curComponent.actionBinds[callbackForm.key] = `${newActionKey}${languageSign}`
      return
    }
    rootStore.dataConfig.actionSet[actionKey] = callbackForm.code
  }
}

// 获取组件默认值
const getDefaultComponentValueObj = (component) => {
  let obj = {}
  component.exposeAttr.forEach(key => {
    obj[key] = component.propValue[key]
  });
  return obj
}

// 构建组件数据绑定
const buildDataBinds = (component, componentStateName) => {
  component.exposeAttr.forEach(key => {
    rootStore.dataCenter.curComponent.dataBinds[key] = [componentStateName, key]
  });
}

// 组件拖入视图后置操作
export const afterComponentEnterView = (component) => {
  // 拖入时选中当前组件
  rootStore.dataCenter.setCurComponent({
    component,
    index: rootStore.dataCenter.componentData.length - 1,
  })
  let componentStateName = getUniqueKey(rootStore.dataConfig.stateSet, component.component)
  if (!component.exposeAttr) return
  rootStore.dataConfig.addState(componentStateName, getDefaultComponentValueObj(component))
  component.componentStateName = componentStateName
  buildDataBinds(component, componentStateName)
}