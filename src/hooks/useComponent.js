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
  let originalKey = rootStore.dataCenter.curComponent.dataBinds[rootStore.dataCenter.curComponent.coreKey][0]
  let key = getUniqueKey(rootStore.dataConfig.stateSet, varName)
  rootStore.dataConfig.addState(key, rootStore.dataConfig.stateSet[originalKey])
  rootStore.dataCenter.curComponent.dataBinds[rootStore.dataCenter.curComponent.coreKey] = [key]
  delete rootStore.dataConfig.stateSet[originalKey]
}

function getUniqueActionKey(obj, key) {
  let originalKey = key;
  let count = 1;
  while (obj.hasOwnProperty(`${key}@julia`)) {
      key = originalKey + count;
      count++;
  }
  return key
}

// 默认支持julia
export const updateCallback = (callbackForm) => {
  if (callbackForm.mode === 'new') {
    let actionKey = getUniqueActionKey(rootStore.dataConfig.actionSet, `${rootStore.dataCenter.curComponent.component}_${callbackForm.key}`)
    rootStore.dataConfig.addAction(`${actionKey}@julia`, callbackForm.code)
    rootStore.dataCenter.curComponent.actionBinds[callbackForm.key] = `${actionKey}@julia`
  } else {
    let actionKey = rootStore.dataCenter.curComponent.actionBinds[callbackForm.key]
    rootStore.dataConfig.actionSet[actionKey] = callbackForm.code
  }
}

// 组件拖入视图后置操作
export const afterComponentEnterView = (component) => {
  // 拖入时选中当前组件
  rootStore.dataCenter.setCurComponent({
    component,
    index: rootStore.dataCenter.componentData.length - 1,
  })
  let key = getUniqueKey(rootStore.dataConfig.stateSet, component.component)
  if (!component.coreKey) return
  rootStore.dataConfig.addState(key, component.propValue[component.coreKey])
  rootStore.dataCenter.curComponent.dataBinds[component.coreKey] = [key]
}