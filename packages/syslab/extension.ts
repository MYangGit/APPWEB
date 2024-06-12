import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';
import appConfig from './extension-build.json';
import * as SyslabFigure from '../submodule/syslab_online_plot/src/figure/syslab_figure'

function getWebViewContent(context: vscode.ExtensionContext, templatePath: string, urlPath: string): string {
  const resourcePath = path.join(context.extensionPath, templatePath);
  let html = fs.readFileSync(resourcePath, 'utf-8');
  console.log('html', resourcePath);
  
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
  SyslabFigure.activate(context);
  let startAppCommand = appConfig.startCommand ?? 'test-org.startTestApp';
  let disposable = vscode.commands.registerCommand(startAppCommand, (urlPath: string) => {
    vscode.commands.executeCommand('start app', {
      id: 'test-app',
      title: appConfig.appTitle ?? 'TestApp',
      titleEn: appConfig.appTitleEn ?? 'TestApp',
      html: getWebViewContent(context, './dist/index.html', urlPath),
      filePath: process.env.USER_DATA_DIR || '/home/tongyuan/SyslabCloud/code-server',
      width: appConfig.appWidth ?? 1080,
      height: appConfig.appHeight ?? 750,
      appType: appConfig.appType ?? 'julia',
    });

    vscode.commands.executeCommand('plot.forward', {
      appid: 'test-app',
      data: {
        type: "hahaha",
        value: "111111"
      }
    });
  });

  context.subscriptions.push(disposable);
  context.subscriptions.push(vscode.commands.registerCommand('plot.receive', (message: any) => {
    console.log('from-app-message', message);
  }));
}

function deactivate() {}

export { activate, deactivate };
