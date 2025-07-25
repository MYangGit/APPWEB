/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ([
/* 0 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.activate = activate;
exports.deactivate = deactivate;
const fs = __importStar(__webpack_require__(1));
const path = __importStar(__webpack_require__(2));
const cp = __importStar(__webpack_require__(3));
const vscode = __importStar(__webpack_require__(4));
const extension_build_json_1 = __importDefault(__webpack_require__(5));
const getQueryVariable = (variable, location) => {
    const query = location.search.substring(1);
    const vars = query.split('&');
    for (let i = 0; i < vars.length; i++) {
        const pair = vars[i].split('=');
        if (pair[0] === variable) {
            return pair[1];
        }
    }
    return (false);
};
async function getWebViewContent(context, templatePath, urlPath) {
    let location = await vscode.commands.executeCommand('Syslab.getWindowLocationInfo');
    const syslabPort = getQueryVariable('syslabPort', location);
    const syslabIp = getQueryVariable('syslabIp', location);
    let pathtemp = '';
    if (syslabPort && syslabIp) {
        pathtemp = `/stable/${syslabPort}/${syslabIp}`;
    }
    else if (syslabPort && !syslabIp) {
        pathtemp = `/stable/${syslabPort}`;
    }
    pathtemp = location.pathname + pathtemp;
    pathtemp = pathtemp === '/' ? '' : pathtemp;
    if (location && location.href) {
        urlPath = pathtemp;
    }
    const resourcePath = path.join(context.extensionPath, templatePath);
    let html = fs.readFileSync(resourcePath, 'utf-8');
    html = html.replace(/(<link.+?href="|<script.+?src="|<img.+?src="|url\(")(.+?)"/g, (m, $1, $2) => {
        let pre = $1 + (urlPath || '');
        if (pre[pre.length - 1] !== '/')
            pre += '/';
        return pre + 'vscode-remote-resource?path=' + context.extensionPath + '/dist' + $2 + '"';
    });
    return html;
}
function activate(context) {
    let startAppCommand = extension_build_json_1.default.startCommand ?? 'test-org.startTestApp';
    let disposable = vscode.commands.registerCommand(startAppCommand, async (urlPath) => {
        vscode.commands.executeCommand('start app', {
            id: extension_build_json_1.default.appName,
            title: extension_build_json_1.default.appTitle ?? 'TestApp',
            titleEn: extension_build_json_1.default.appTitleEn ?? 'TestApp',
            html: await getWebViewContent(context, './dist/index.html', urlPath),
            filePath: process.env.TONGYUAN_PATH || '/home/tongyuan/SyslabCloud/code-server',
            // filePath: 'C:/Users/admin/syslabCloud',
            width: extension_build_json_1.default.appWidth ?? 1080,
            height: extension_build_json_1.default.appHeight ?? 750,
            appType: extension_build_json_1.default.appType ?? 'julia',
        });
    });
    context.subscriptions.push(disposable);
    // 接收来自app的消息
    context.subscriptions.push(vscode.commands.registerCommand('syslabApp.sendToPlotService', (message) => {
        if (message.command === 'closeApp') {
            deactivate();
            return;
        }
    }));
    // 执行python脚本
    context.subscriptions.push(vscode.commands.registerCommand('syslab.excutePython', (pythonCode, workspace) => {
        const pythonFilePath = `${workspace}/temp.py`;
        fs.writeFileSync(pythonFilePath, pythonCode);
        return new Promise((resolve) => {
            cp.exec(`python ${pythonFilePath}`, (error) => {
                resolve(error?.message);
            });
        });
    }));
}
function deactivate() { }


/***/ }),
/* 1 */
/***/ ((module) => {

module.exports = require("fs");

/***/ }),
/* 2 */
/***/ ((module) => {

module.exports = require("path");

/***/ }),
/* 3 */
/***/ ((module) => {

module.exports = require("child_process");

/***/ }),
/* 4 */
/***/ ((module) => {

module.exports = require("vscode");

/***/ }),
/* 5 */
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"appName":"CNOOC","displayName":"CNOOC","startCommand":"CNOOC","startTitle":"CNOOC","publishMoHub":false,"MoHubPort":47736,"icon":"app-icon.png","version":"1.0.0","description":"这是一个中海油demo应用","appTitle":"中海油demo","appTitleEn":"CNOOC","appHeight":1200,"appWidth":1700,"appType":"julia"}');

/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__(0);
/******/ 	module.exports = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=extension.js.map