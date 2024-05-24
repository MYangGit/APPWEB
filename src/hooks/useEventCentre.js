import { rootStore } from '@/stores/rootStore';
import { useGlobalUtils } from '@/hooks/useGlobalUtils';
import { parseJuliaFn } from '@/hooks/useJuliaCentre'
import { parsePythonFn } from '@/hooks/usePythonCentre'
import { computed } from 'vue';

const actionCenter = computed(() => {
   let actionCenter = {}
   for (const key in rootStore.dataConfig.actionSet) {
      if (Object.hasOwnProperty.call(rootStore.dataConfig.actionSet, key)) {
         actionCenter[key] = function () {
            return excuteJsAction(key, {
               params: [...arguments]
            })
         }
      }
   }
   return actionCenter
})

const getFunction = (actionKey) => {
   let code = rootStore.dataConfig.actionSet[actionKey]
   if (actionKey.indexOf('@') === -1) {
      return new Function(`return ${code}`)()
   }
   if (actionKey.indexOf('@julia') > -1) {
      return new Function(`return ${parseJuliaFn(code)}`)()
   }
   if (actionKey.indexOf('@python') > -1) {
      return new Function(`return ${parsePythonFn(code)}`)()
   }
}

export const excuteJsAction = (actionName, eventParams = {}) => {
   let fn = getFunction(actionName)
   return fn({dataCenter: rootStore.dataConfig.stateSet, actionCenter: actionCenter.value, globalUtils: useGlobalUtils()}, eventParams)
}

/**
 * @description 事件暴露二次覆盖重写中心
 * @returns
 */
export const useEventCentre = () => {
   // 事件触发
   const onChange = ({ element, newValue }) => {
      let { change } = element.actionBinds;
      if (!change) return
      let fn = getFunction(change)
      fn({
            dataCenter: rootStore.dataConfig.stateSet,
            actionCenter: actionCenter.value,
            globalUtils: useGlobalUtils()
         },
         {
            newValue: newValue
         }
      )
   }

   // 事件点击
   const onClick = ({ element }) => {
      let { click } = element.actionBinds;
      if (!click) return
      let fn = getFunction(click)
      fn({dataCenter: rootStore.dataConfig.stateSet, actionCenter: actionCenter.value, globalUtils: useGlobalUtils()}, {})
   }

   // 其它点击事件
   const onClickOther = ({ element, clickName, params }) => {
      let click = element.actionBinds[clickName];
      if (!click) return
      let fn = getFunction(click)
      fn({dataCenter: rootStore.dataConfig.stateSet ,actionCenter: actionCenter.value, globalUtils: useGlobalUtils()}, {
            clickName,
            params: params
      })
   }
   
   return {
      onChange,
      onClick,
      onClickOther
   }
};