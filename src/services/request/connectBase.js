import defer from 'defer-promise'

let vscode;
if (window.acquireVsCodeApi) {
  vscode = window.acquireVsCodeApi();
  window.vscode = vscode
} else {
  vscode = window.parent;
}

// 目前只实现了单个请求发起
let deferred = defer();
export const post = async (config) => {
  config.filePath = filePath
  vscode.postMessage(config)
  deferred = defer();
  let res;
  try {
    res = await deferred.promise
  } catch (error) {
    res = {
      type: 'error',
      message: error
    }
  }
  return res
}

export const postMessage = (config) => {
  config.filePath = getFilePath()
  vscode.postMessage(config)
}

// 处理消息返回
window.addEventListener('message', event => {
  const message = event.data;
  // console.log('message', message)
  if (message.type === 'receiveData') {
    if (!message.result) {
      deferred.resolve(false)
      return
    }
    if (message.result && message.result.inline && message.result.inline.indexOf('ERROR') > -1) {
      deferred.resolve(false)
      return
    }
    deferred.resolve(message)
  } else {
    deferred.resolve(message)
  }
});

let filePath = ''

export const initFilePath = async () => {
  let message = await post({
    key: 'filePath',
    command: 'getFilePath'
  })
  if (message && message.data) filePath = message.data.value
  return message.data
}

export const getFilePath = () => {
  return filePath
}

// 检查变量是否存在
export const checkValHas = async (varNames) => {
  let message = await post({
    key: 'checkVar',
    command: 'getWorkspaceVariables',
    filePath: getFilePath(),
  })
  if (message && message.data && message.type === 'receiveWorkspaceVariables') {
    let varList = message.data.value.map((item) => item.fullname)
    let catchVar;
    for (let varname of varNames) {
      if (varList.indexOf(varname) > -1) {
        catchVar = varname
        break;
      }
    }
    return catchVar
  }
}

// 导出设计文件
export const importDesignFile = async () => {
  let message = await post({
    key: 'importTextFile',
    command: 'importTextFile',
    filePath: getFilePath()
  })
  let fileContent = message.data.value.slice(0, message.data.value.lastIndexOf('}\n') + 1);
  let md5hash = message.data.value.slice(message.data.value.lastIndexOf('}\n') + 2);
  if ((window).md5(fileContent) !== md5hash) {
    return {
      type: 'error',
      message: '文件校验失败'
    }
  }
  return JSON.parse(fileContent);
}

// 加载 syslab 文件 param 必须满足JSON格式
export const exportDesignFile = (param) => {
  let text = JSON.stringify(param, null, "\t");
  // 执行导出获取返回
  post({
    key: 'exportTextFile',
    command: 'exportTextFile',
    content: `${text}\n${(window).md5(text)}`,
    filePath: getFilePath(),
  })
}