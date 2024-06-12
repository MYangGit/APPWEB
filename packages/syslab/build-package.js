const fs = require('fs-extra');
const { exec } = require('child_process');
const appConfig = require('./extension-build.json'); // Removed assert statement for JSON type

writePackageJson(appConfig);

enterDirAndExecCommand('vsce package --no-dependencies', './packages/syslab').then(() => {
  console.log('打包完成');
});

function enterDirAndExecCommand(command, cwd) {
  return new Promise((resolve, reject) => {
    exec(command, { cwd }, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve(stdout);
      }
    });
  });
}

function writePackageJson(appConfig) {
  // 读取 package.json 文件
  fs.readFile('packages/syslab/package.json', 'utf8', (err, data) => {
    if (err) return;
    const packageObj = JSON.parse(data);
    packageObj.name = appConfig.appName;
    packageObj.displayName = appConfig.displayName;
    packageObj.description = appConfig.description;
    packageObj.version = appConfig.version;
    packageObj.icon = appConfig.icon || 'app-icon.png';
    packageObj.activationEvents = [
      `onCommand:${appConfig.appName}`
    ];
    packageObj.contributes.commands = [
      {
        "command": appConfig.appName,
        "title": appConfig.appName,
      }
    ];

    // 写入更新后的 package.json 文件
    fs.writeFile('packages/syslab/package.json', JSON.stringify(packageObj, null, 2), 'utf8', (err) => {
      if (err) return;
    });
  });
}