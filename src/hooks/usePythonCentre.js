function genPythonVarStrs(obj) {
   let pythonCode = '';
   for (let key in obj) {
      let value = obj[key];
      if (typeof value === 'string') {
         value = `"${value}"`; // Wrap strings in double quotes
      }
      if (typeof value === 'object') {
         value = `json.loads("${JSON.stringify(value).replace(/\"/g, "\\\"")}")`; // Wrap strings in double quotes
      }
      pythonCode += `${key} = ${value}\n`;
   }
   return pythonCode;
}

function genDictByKeys(obj, name) {
   let pythonCode = `${name} = {\n`;
   for (let key in obj) {
      pythonCode += `  "${key}": ${key},\n`;
   }
   pythonCode += '}';
   return pythonCode;
}

// 本地数据注入
const varInject = (str, stateObj) => {
   let pythonVarStrs = genPythonVarStrs(stateObj)
   return `${pythonVarStrs}\n${str}`
}

// 结果返回机制附件
const attachReturn = (str, stateObj, name, appFilePath) => {
   return `
import json
${str}
${genDictByKeys(stateObj, name)}
output_text = json.dumps(${name})
io = open("${appFilePath}","w")
io.write(output_text)
io.close()
   `
}

export const handlePythonCode = (funStr, stateObj, name, appFilePath) => {
   let pythonCode = varInject(funStr, stateObj)
   return attachReturn(pythonCode, stateObj, name, appFilePath)
}

export const parsePythonFn = (code) => {
   return `async ({dataCenter, globalUtils}, eventParams) => {
          const { post, getFilePath, handlePythonCode, postMessage } = globalUtils
          let pythonCode = \`${code}\`
          let code = handlePythonCode(pythonCode, dataCenter, "gd", getFilePath())
          function assignValues(obj, obj2) {
             for (let key in obj) {
                if (obj2.hasOwnProperty(key)) {
                   obj2[key] = obj[key];
                }
             }
          }
          console.log('excuteCode', code)
          let startTime = Date.now()
          let res = await post({
             key: 'excuteCode',
             command: 'excute',
             lang: 'python',
             code
          })
          console.log('res', res.data.value)
          console.log('excuteTime', (Date.now() - startTime) / 1000)
          if (res.data && res.data.value) {
            console.log('value', JSON.stringify(res.data.value))
            assignValues(res.data.value, dataCenter)
            postMessage({
               type: "loaded",
               command: "toPlotService"
            })
          }
       }
    `;
}