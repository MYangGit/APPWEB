import { rootStore } from '@/stores/rootStore';

const parseJuliaFn = (name, props, code, returns) => {
   return  `async ({dataCenter, globalUtils}, eventParams) => {
         const { post, getFilePath } = globalUtils
         const getJuliaValueByDotKey = (obj, dotKey) => {
            const keys = dotKey.split('.');
            let value = obj;
            for (let key of keys) {
              if (value.hasOwnProperty(key)) {
                value = value[key];
              } else {
                value = ''; // 如果键不存在，返回 undefined
              }
            }
            if (typeof value === 'string') {
               value = '"' + value + '"';
            }
            if (typeof value === 'object') {
               value = JSON.stringify(value);
            }
            return value;
         }
         const setJuliaValueByDotKey = (obj, dotKey, value) => {
            const keys = dotKey.split('.');
            const lastKey = keys.pop();
            let currentObj = obj;
            for (let key of keys) {
              if (!currentObj.hasOwnProperty(key) || typeof currentObj[key] !== 'object') {
                currentObj[key] = {};
              }
              currentObj = currentObj[key];
            }
            currentObj[lastKey] = value;
         }
         let getVarListCodeStr = () => {
            let props = ${JSON.stringify(props)}
            let strs = Object.keys(props).map(key => {
               return \`\${key} = \${getJuliaValueByDotKey(dataCenter, props[key].join('.'))}\`
            })
            return strs.join('\\n')
         }
         let getExcuteCode = () => {
            return \`
let
   using TyDSPSystem
   using TyPlot
   function tmp()
      \$\{getVarListCodeStr()\}
      ${code}
   end
   using JSON
   output_text = JSON.json(tmp())
   io = open("\${getFilePath()}","w")
   write(io,output_text)
   close(io)
end
            \`
         }
         console.log('excuteCode', getExcuteCode())
         let res = await post({
            key: 'excuteCode',
            command: 'excute',
            code: getExcuteCode()
         })
         let returns = ${JSON.stringify(returns)}
         if (returns && res.data &&res.data.value) {
            let keys = returns[\`Julia@${name}\`]
            setJuliaValueByDotKey(dataCenter, keys.join('.'), res.data.value)
         }
      }
   `;
}

const getFunction = (configOrFn) => {
   let isFn = configOrFn.indexOf('{') === 0 ? false : true
   if (isFn) return new Function(`return ${configOrFn}`)()
   let {name, type, props, code, returns} = JSON.parse(configOrFn)
   if (type === 'Julia') {
      return new Function(`return ${parseJuliaFn(name, props, code, returns)}`)()
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
      let fn = new Function(`return ${rootStore.dataConfig.actionSet[change]}`)()
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils: {}}, {
            newValue: newValue
      })
   }

   // 事件点击
   const onClick = ({ element }) => {
      let { click } = element.actionBinds;
      if (!click) return
      let fn = getFunction(rootStore.dataConfig.actionSet[click])
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils: {
         post: () => {},
         getFilePath: () => {}
      }})
   }

   // 其它点击事件
   const onClickOther = ({ element, clickName, params }) => {
      let click = element.actionBinds[clickName];
      if (!click) return
      let fn = new Function(`return ${rootStore.dataConfig.actionSet[click]}`)()
      fn({dataCenter: rootStore.dataConfig.stateSet, globalUtils: {}}, {
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