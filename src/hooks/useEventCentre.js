import { rootStore } from '@/stores/rootStore';
import { parseJuliaFn } from '@/hooks/useJuliaCentre'
import globalUtils from './eventCentre/globalUtils'

const getFunction = (actionKey) => {
   let code = rootStore.dataConfig.actionSet[actionKey]
   if (actionKey.indexOf('@') === -1) {
      return new Function(`return ${code}`)()
   }
   if (actionKey.indexOf('@julia') > -1) {
      return new Function(`return ${parseJuliaFn(code)}`)()
   }
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
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils}, {
         newValue: newValue
      })
   }

   // 事件点击
   const onClick = ({ element }) => {
      let { click } = element.actionBinds;
      if (!click) return
      let fn = getFunction(click)
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils})
   }

   // 其它点击事件
   const onClickOther = ({ element, clickName, params }) => {
      let click = element.actionBinds[clickName];
      if (!click) return
      let fn = getFunction(click)
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils}, {
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