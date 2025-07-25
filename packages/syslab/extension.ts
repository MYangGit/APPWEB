import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';
import * as vscode from 'vscode';
import appConfig from './extension-build.json';

const getQueryVariable = (variable, location) => {
  const query = location.search.substring(1);
  const vars = query.split('&');
  for (let i = 0; i < vars.length; i++) {
    const pair = vars[i].split('=');
    if (pair[0] === variable) { return pair[1]; }
  }
  return (false);
};

async function getWebViewContent(context, templatePath, urlPath) {
  let location = await vscode.commands.executeCommand('Syslab.getWindowLocationInfo') as any;
  const syslabPort = getQueryVariable('syslabPort', location);
	const syslabIp = getQueryVariable('syslabIp', location);
  let pathtemp = '';
  if (syslabPort && syslabIp) {
    pathtemp = `/stable/${syslabPort}/${syslabIp}`;
  } else if (syslabPort && !syslabIp) {
    pathtemp = `/stable/${syslabPort}`;
  }
  pathtemp = location.pathname + pathtemp;
	pathtemp = pathtemp === '/' ? '' : pathtemp;
  if (location && location.href) {
    urlPath = pathtemp
  }
  const resourcePath = path.join(context.extensionPath, templatePath)
  let html = fs.readFileSync(resourcePath, 'utf-8');
  html = html.replace(/(<link.+?href="|<script.+?src="|<img.+?src="|url\(")(.+?)"/g, (m, $1, $2) => {
    let pre = $1 + (urlPath || '')
    if(pre[pre.length - 1] !== '/') pre += '/'
    return  pre + 'vscode-remote-resource?path=' + context.extensionPath + '/dist' + $2 + '"'
  })
  return html
}

function activate(context: vscode.ExtensionContext) {
  let startAppCommand = appConfig.startCommand ?? 'test-org.startTestApp';
  let disposable = vscode.commands.registerCommand(startAppCommand, async (urlPath: string) => {
    vscode.commands.executeCommand('start app', {
      id: appConfig.appName,
      title: appConfig.appTitle ?? 'TestApp',
      titleEn: appConfig.appTitleEn ?? 'TestApp',
      html: await getWebViewContent(context, './dist/index.html', urlPath),
      filePath: process.env.TONGYUAN_PATH || '/home/tongyuan/SyslabCloud/code-server',
      // filePath: 'C:/Users/admin/syslabCloud',
      width: appConfig.appWidth ?? 1080,
      height: appConfig.appHeight ?? 750,
      appType: appConfig.appType ?? 'julia',
    });
  });

  context.subscriptions.push(disposable);
  // 接收来自app的消息
  context.subscriptions.push(vscode.commands.registerCommand('syslabApp.sendToPlotService', (message: any) => {
    if (message.command === 'closeApp') { deactivate(); return; }
  }));
  // 执行python脚本
  context.subscriptions.push(vscode.commands.registerCommand('syslab.excutePython', (pythonCode: string, workspace: string) => {
    const pythonFilePath = `${workspace}/temp.py`;
		fs.writeFileSync(pythonFilePath, pythonCode);
		return new Promise((resolve: (value: string | undefined) => void) => {
			cp.exec(`python ${pythonFilePath}`, (error: any) => {
				resolve(error?.message);
			})
		})
  }));
}

function deactivate() {}
export { activate, deactivate };
