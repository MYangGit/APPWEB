import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import fileUpload from 'express-fileupload'
import fs from 'fs-extra';
import path from 'path'
import { enterDirAndExecCommand, writePackageJson, writeExtensionBuildJson } from './utils.js'

const port = 3000

const app = express()

// 启用文件上传
app.use(fileUpload({
  createParentPath: true
}));

app.use(express.static('./packages/'))

//添加其他中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// POST请求的路由处理程序
app.post('/buildAppVsix', (req, res) => {
  // 从请求中获取appjson文本参数
  const { appJson, appConfig: appConfigJson } = req.body;

  // 确保请求中有appjson参数
  if (!appJson || !appConfigJson) {
    return res.status(400).json({ error: 'Missing appjson parameter' });
  }
  // 生成文件路径
  const jsonFilePath = path.join('./packages/syslab/', 'syslabApp.json');
  // appConfig
  const appConfig = JSON.parse(appConfigJson)
  fs.writeFile(jsonFilePath, appJson).then(() => {
    console.log(111111)
    // 删除旧的dist目录
    fs.removeSync('./packages/syslab/dist');
    console.log(2222222)
    enterDirAndExecCommand('npm run build:app', './').then(() =>{
      console.log('dist构建完成')
      writePackageJson(appConfig)
      writeExtensionBuildJson(appConfig)
      enterDirAndExecCommand('vsce package --no-dependencies', './packages/syslab/').then(() => {
        console.log('vsce打包完成')
        res.status(200).json({
          fileUrl: `http://${req.headers.host}/syslab/${appConfig.appName}-${appConfig.version}.vsix`
        });
      })
    }, () => {
      res.status(500).json({ message: 'File generation failed' });
    })
  })
  .catch(err => {
    console.error(err);
    res.status(500).json({ error: 'Failed to write file' });
  });
});

app.listen(port, () => {
  console.log(`App Service is listening on port http://localhost:${port}.`)
})