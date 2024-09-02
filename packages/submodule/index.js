
export let syslabPlot = null;

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