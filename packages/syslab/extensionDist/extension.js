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
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
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
const index_1 = __webpack_require__(6);
function getWebViewContent(context, templatePath, urlPath) {
    const resourcePath = path.join(context.extensionPath, templatePath);
    let html = fs.readFileSync(resourcePath, 'utf-8');
    let port = extension_build_json_1.default.MoHubPort;
    html = html.replace(/(<link.+?href="|<script.+?src="|<img.+?src="|url\(")(.+?)"/g, (m, $1, $2) => {
        if (extension_build_json_1.default.publishMoHub) {
            return $1 + (urlPath || '') + `/cn-north-4/syslabonline//stable/${port}/vscode-remote-resource?path=` + context.extensionPath + '/dist' + $2 + '"';
        }
        return $1 + (urlPath || '') + '/vscode-remote-resource?path=' + context.extensionPath + '/dist' + $2 + '"';
    });
    return html;
}
function activate(context) {
    let startAppCommand = extension_build_json_1.default.startCommand ?? 'test-org.startTestApp';
    let disposable = vscode.commands.registerCommand(startAppCommand, (urlPath) => {
        if (index_1.syslabPlot) {
            index_1.syslabPlot.SyslabFigure.activate(context, 'app');
        }
        vscode.commands.executeCommand('start app', {
            id: extension_build_json_1.default.appName,
            title: extension_build_json_1.default.appTitle ?? 'TestApp',
            titleEn: extension_build_json_1.default.appTitleEn ?? 'TestApp',
            html: getWebViewContent(context, './dist/index.html', urlPath),
            filePath: process.env.USER_DATA_DIR || '/home/tongyuan/SyslabCloud/code-server',
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
        if (index_1.syslabPlot) {
            index_1.syslabPlot.SyslabFigure.handleAppMessage(message, extension_build_json_1.default.appName);
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
function deactivate() {
    if (index_1.syslabPlot) {
        index_1.syslabPlot.deactivate("app");
    }
}


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

module.exports = /*#__PURE__*/JSON.parse('{"appName":"antennaArrayDesigner","displayName":"antennaArrayDesigner","startCommand":"antennaArrayDesigner","startTitle":"antennaArrayDesigner","publishMoHub":false,"MoHubPort":47736,"icon":"app-icon.png","version":"1.0.0","description":"这是一个天线阵列设计器","appTitle":"天线阵列设计器","appTitleEn":"antennaArrayDesigner","appHeight":750,"appWidth":1200,"appType":"julia"}');

/***/ }),
/* 6 */
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   syslabPlot: () => (/* binding */ syslabPlot)
/* harmony export */ });

let syslabPlot = null;

// if (isUseVInteractPlot) {
//     (async () => {
//         try {
//             // 动态导入所有相关模块
//             const modules = import.meta.glob('./syslab_online_plot/**');
//             const SyslabFigure = await modules[`./syslab_online_plot/src/figure/syslab_figure.ts`]();
//             const { deactivate } = await modules[`./syslab_online_plot/src/extension.ts`]();
//             const loadingGif = await modules[`./syslab_online_plot/lib/webagg/_images/loading.gif`]();
            
//             // 动态导入其他依赖
//             await modules[`./syslab_online_plot/lib/lodash.js`]();
//             await modules[`./syslab_online_plot/lib/webagg/mpl.js`]();
//             await modules[`./syslab_online_plot/lib/webagg/color_change.js`]();
//             await modules[`./syslab_online_plot/lib/webagg/text_editor.js`]();
//             await modules[`./syslab_online_plot/lib/webagg/confirm_box.js`]();
//             await modules[`./syslab_online_plot/lib/webagg/_static/css/page.css`]();
//             await modules[`./syslab_online_plot/lib/webagg/_static/css/boilerplate.css`]();
//             await modules[`./syslab_online_plot/lib/webagg/_static/css/fbm.css`]();
//             await modules[`./syslab_online_plot/lib/webagg/_static/css/mpl.css`]();
//             await modules[`./syslab_online_plot/lib/webagg/_static/css/color_change.css`]();

//             syslabPlot = {
//                 SyslabFigure,
//                 deactivate
//             };
//         } catch (error) {
//             console.error('Failed to dynamically import modules:', error);
//         }
//     })();
// }

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
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
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