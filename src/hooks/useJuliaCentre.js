function genJuliaVarStrs(obj) {
   let juliaCode = '';
   for (let key in obj) {
      let value = obj[key];
      if (typeof value === 'string') {
         value = `"${value}"`; // Wrap strings in double quotes
      }
      if (typeof value === 'object') {
         value = `JSON.parse("${JSON.stringify(value).replace(/\"/g, "\\\"")}")`; // Wrap strings in double quotes
      }
      juliaCode += `${key} = ${value}\n`;
   }
   return juliaCode;
}

function genDictByKeys(obj, name) {
   let juliaCode = `${name} = Dict(\n`;
   for (let key in obj) {
      juliaCode += `  "${key}" => ${key},\n`;
   }
   juliaCode += ')';
   return juliaCode;
}

// 本地数据注入
const varInject = (str, stateObj) => {
   let juliaVarStrs = genJuliaVarStrs(stateObj)
   return `${juliaVarStrs}\n${str}`
}

// 结果返回机制附件
const attachReturn = (str, stateObj, name, appFilePath) => {
   return `
 let
   using JSON
   ${str}
   ${genDictByKeys(stateObj, name)}
   output_text = JSON.json(${name})
   io = open("${appFilePath}","w")
   write(io,output_text)
   close(io)
 end
   `
}

export const handleJuliaCode = (funStr, stateObj, name, appFilePath) => {
   let juliaCode = varInject(funStr, stateObj)
   return attachReturn(juliaCode, stateObj, name, appFilePath)
}

export const parseJuliaFn = (code) => {
   return `async ({dataCenter, globalUtils}, eventParams) => {
          const { post, getFilePath, handleJuliaCode } = globalUtils
          let juliaCode = \`${code}\`
          let code = handleJuliaCode(juliaCode, dataCenter, "gd", getFilePath())
          function assignValues(obj, obj2) {
             for (let key in obj) {
                if (obj2.hasOwnProperty(key)) {
                   obj2[key] = obj[key];
                }
             }
          }
          console.log('excuteCode', code)
          let res = await post({
             key: 'excuteCode',
             command: 'excute',
             code
          })
          console.log('res', res.data.value)
          if (res.data && res.data.value) {
             assignValues(res.data.value, dataCenter)
          }
       }
    `;
}