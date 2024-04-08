import { rootStore } from '@/stores/rootStore';

/**
 * @description 事件暴露二次覆盖重写中心
 * @returns 
 */
export const useEventCentre = () => {

   // 事件触发
   const onChange = ({ element, newValue, oldValue }) => {
      let { change } = element.actionBinds;
      if (!change) return
      let fn = new Function(`return ${rootStore.dataConfig.actionSet[change]}`)()
      fn(rootStore.dataConfig.stateSet, {
            globalUtils: {},
            newValue: newValue, 
            oldValue: oldValue 
      })
   }

   // 事件点击
   const onClick = ({ element }) => {
      let { click } = element.actionBinds;
      if (!click) return
      let fn = new Function(`return ${rootStore.dataConfig.actionSet[click]}`)()
      fn(rootStore.dataConfig.stateSet, {
         globalUtils: {},
      })
   }
   
   return {
    onChange,
    onClick
   }
};