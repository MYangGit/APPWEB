import * as fs from 'fs';
import * as path from 'path';
import * as cp from 'child_process';
import * as vscode from 'vscode';
import appConfig from './extension-build.json';
import { syslabPlot  } from '../submodule/index';

function getWebViewContent(context: vscode.ExtensionContext, templatePath: string, urlPath: string): string {
  const resourcePath = path.join(context.extensionPath, templatePath);
  let html = fs.readFileSync(resourcePath, 'utf-8');
  
  let port = appConfig.MoHubPort;
  html = html.replace(/(<link.+?href="|<script.+?src="|<img.+?src="|url\(")(.+?)"/g, (m, $1, $2) => {
    if(appConfig.publishMoHub){
      return $1 + (urlPath || '') + `/cn-north-4/syslabonline//stable/${port}/vscode-remote-resource?path=` + context.extensionPath + '/dist' + $2 + '"';
    }
    return $1 + (urlPath || '') + '/vscode-remote-resource?path=' + context.extensionPath + '/dist' + $2 + '"';
  });

  return html;
}


function activate(context: vscode.ExtensionContext) {
  let startAppCommand = appConfig.startCommand ?? 'test-org.startTestApp';
  let disposable = vscode.commands.registerCommand(startAppCommand, (urlPath: string) => {
    if(syslabPlot){
      syslabPlot.SyslabFigure.activate(context, 'app');
    }
    vscode.commands.executeCommand('start app', {
      id: appConfig.appName,
      title: appConfig.appTitle ?? 'TestApp',
      titleEn: appConfig.appTitleEn ?? 'TestApp',
      html: getWebViewContent(context, './dist/index.html', urlPath),
      filePath: process.env.USER_DATA_DIR || '/home/tongyuan/SyslabCloud/code-server',
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
    if(syslabPlot){
      syslabPlot.SyslabFigure.handleAppMessage(message, appConfig.appName);
    }
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

function deactivate() {
  if(syslabPlot){
     syslabPlot.deactivate("app");
  }
}
export { activate, deactivate };
