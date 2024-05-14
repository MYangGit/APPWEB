import { exec } from 'child_process';
import fs from 'fs-extra';

export function enterDirAndExecCommand(command, cwd) {
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

export function copyFileTo(sourceDirectory, targetDirectory){
  return fs.copy(sourceDirectory, targetDirectory, {overwrite: true})
} 

export function writePackageJson (appConfig) {
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
      if (err) return
    });
  });
}

export function writeExtensionBuildJson (appConfig) {
  fs.readFile('packages/syslab/extension-build.json', 'utf8', (err, data) => {
    if (err) return;
    const buildObj = JSON.parse(data);
    buildObj.appName = appConfig.appName;
    buildObj.displayName = appConfig.displayName;
    buildObj.startCommand = appConfig.appName;
    buildObj.startTitle = appConfig.appName;
    buildObj.icon = appConfig.icon || "app-icon.png";
    buildObj.version = appConfig.version;
    buildObj.publishMoHub = appConfig.publishMoHub;
    buildObj.MoHubPort = appConfig.MoHubPort;
    buildObj.appTitle = appConfig.displayName;
    buildObj.appTitleEn = appConfig.displayName;
    buildObj.appWidth = appConfig.width;
    buildObj.appHeight = appConfig.height;

    fs.writeFile('packages/syslab/extension-build.json', JSON.stringify(buildObj, null, 2), 'utf8', (err) => {
      if (err) return
    });
  });
}


