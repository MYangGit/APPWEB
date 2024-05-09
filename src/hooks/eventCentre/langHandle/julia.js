function genJuliaVarStrs(obj) {
  let juliaCode = '';
  for (let key in obj) {
      let value = obj[key];
      if (typeof value === 'string') {
          value = `"${value}"`; // Wrap strings in double quotes
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
  ${str}
  ${genDictByKeys(stateObj, name)}
  using JSON
  output_text = JSON.json(${name})
  io = open("${appFilePath}","w")
  write(io,output_text)
  close(io)
end
  `
}

const handleJuliaCode = (funStr, stateObj, name, appFilePath) => {
  let juliaCode = varInject(funStr, stateObj)
  return attachReturn(juliaCode, stateObj, name, appFilePath)
}

export {
  handleJuliaCode
}

