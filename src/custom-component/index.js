import { defineAsyncComponent } from "vue";

const components = [
    'CircleShape',
    'Picture',
    'VText',
    'VButton',
    'VSelect',
    'VInput',
    'Group',
    'RectShape',
    'LineShape',
    'VTable',
    'TreeList',
    'Tabs',
    'GridLayout',
    'TyCharts',
    'SvgViewer',
    'ModelAttributes',
    'TyModelParams',
    'ModelUser',
    'Gauge',
    'Radar',
    'Pie',
    'RTitle',
    'Section',
    'Paragraph',
    'ModelList',
    'ModelName',
    'ModelSnapshot',
    'ModelDocument',
    'ModelParameterTable',
    'SimulationList',
    'SimulationParameter',
    'SimulationSettings',
    'SimulationResult',
    'SimulationVariable',
    'SimulationVariablePlot',
    'SimulationTime',
    'SelectModel',
    'Lamp',
    'Tube',
    'ModelInput',
    'ModelOutput',
    'Animation',
    'VHtml',
    'VRadio',
    'VCheckBox',
    'VInputNumber',
    'VTextArea',
    'VDate',
    'VSlide',
    'VPanel',
];

export const install = function (app) {
    // forEach边历子组件 并使用懒加载模式注册给vue
    components.forEach((key) => {
        app.component(key, defineAsyncComponent(() => import(`@/custom-component/${key}/Component.vue`)));
        app.component(key + 'Attr', defineAsyncComponent(() => import(`@/custom-component/${key}/Attr.vue`)));
    });

    const svgs = ['SVGStar', 'SVGTriangle'];

    svgs.forEach((key) => {
        app.component(key, () => import(`@/custom-component/svgs/${key}/Component.vue`));
        app.component(key + 'Attr', () => import(`@/custom-component/svgs/${key}/Attr.vue`));
    });
};
