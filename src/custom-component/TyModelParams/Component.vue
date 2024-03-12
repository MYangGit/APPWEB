<template>
    <div class="no-position">
        <modelParams :data="params" @refreshModel="refreshModel"></modelParams>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import { getComponentParams, editComponentParams, saveModel } from '@/utils/websocket';
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent';

export default {
    name: 'TyModelParams',
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {},
        },
        request: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            /* eslint-disable */
            params: [
                {
                    label: 'General',
                    children: [
                        {
                            label: 'Parameters',
                            children: [
                                {
                                    name: 'nout',
                                    unit: '',
                                    paramUnit: '',
                                    paramDispUnit: '',
                                    bDispUnitEnable: false,
                                    unitComboBox: [],
                                    description: 'Number of outputs',
                                    tabInfo: 'General',
                                    groupInfo: 'Parameters',
                                    value: 'max([size(deltaq, 1); size(qd_max, 1); size(qdd_max, 1)])',
                                    paramValue: 'max([size(deltaq, 1); size(qd_max, 1); size(qdd_max, 1)])',
                                    enable: false,
                                    isDefault: true,
                                    bShowStartAttribute: false,
                                    showOnParamPanel: false,
                                    eValueType: 'Normal',
                                    comboBoxList: [],
                                },
                                {
                                    name: 'deltaq',
                                    unit: '',
                                    paramUnit: '',
                                    paramDispUnit: '',
                                    bDispUnitEnable: false,
                                    unitComboBox: [],
                                    description: 'Distance to move',
                                    tabInfo: 'General',
                                    groupInfo: 'Parameters',
                                    value: '{driveAngle}',
                                    paramValue: '{driveAngle}',
                                    enable: true,
                                    isDefault: false,
                                    bShowStartAttribute: false,
                                    showOnParamPanel: true,
                                    eValueType: 'Normal',
                                    comboBoxList: [],
                                },
                                {
                                    name: 'qd_max',
                                    unit: '',
                                    paramUnit: '',
                                    paramDispUnit: '',
                                    bDispUnitEnable: false,
                                    unitComboBox: [],
                                    description: 'Maximum velocities der(q)',
                                    tabInfo: 'General',
                                    groupInfo: 'Parameters',
                                    value: '{1}',
                                    paramValue: '{1}',
                                    enable: true,
                                    isDefault: false,
                                    bShowStartAttribute: false,
                                    showOnParamPanel: true,
                                    eValueType: 'Normal',
                                    comboBoxList: [],
                                },
                                {
                                    name: 'qdd_max',
                                    unit: '',
                                    paramUnit: '',
                                    paramDispUnit: '',
                                    bDispUnitEnable: false,
                                    unitComboBox: [],
                                    description: 'Maximum accelerations der(qd)',
                                    tabInfo: 'General',
                                    groupInfo: 'Parameters',
                                    value: '{1}',
                                    paramValue: '{1}',
                                    enable: true,
                                    isDefault: false,
                                    bShowStartAttribute: false,
                                    showOnParamPanel: true,
                                    eValueType: 'Normal',
                                    comboBoxList: [],
                                },
                                {
                                    name: 'startTime',
                                    unit: 's',
                                    paramUnit: 's',
                                    paramDispUnit: '',
                                    bDispUnitEnable: true,
                                    unitComboBox: ['s', 'ms', 'min', 'h', 'd'],
                                    description: 'Time instant at which movement starts',
                                    tabInfo: 'General',
                                    groupInfo: 'Parameters',
                                    value: '0.5',
                                    paramValue: '0.5',
                                    enable: true,
                                    isDefault: false,
                                    bShowStartAttribute: false,
                                    showOnParamPanel: true,
                                    eValueType: 'Normal',
                                    comboBoxList: [],
                                },
                            ],
                        },
                    ],
                },
            ],
            modelInfo: {},
        };
    },
    computed: {
        ...mapState(['projectData']),
    },
    methods: {
        updateData(params) {
            this.modelInfo = params;
            if (params.specialization === 'package') {
                this.params = [];
                return;
            }
            this.loadData(params);
        },
        loadData(params) {
            let request = {
                modelName: params.fullName,
                compName: params.compName || '',
            };
            getComponentParams(request).then((res) => {
                const result = res.parameterList;
                if (result.length) {
                    result.forEach((item) => {
                        if (item.eValueType == 'CheckBox') {
                            item.value = item.value == 'true';
                        }
                        item.comboBoxList.forEach((i) => {
                            if (i.value == 'false' || i.value == 'true') {
                                i.value = i.value == 'true';
                            }
                            i.label = i.description;
                            i.value = i.value || i.description;
                        });
                    });
                    this.params = this.splitGroup(result);
                    this.params.forEach((item) => {
                        item.children = this.splitGroup(item.children, 'groupInfo');
                    });
                } else {
                    this.params = [];
                }
            });
        },
        // 分组
        splitGroup(data, key = 'tabInfo') {
            let groups = [];
            data.forEach((item) => {
                let i = groups.findIndex((group) => group.label === item[key]);
                if (i != -1) {
                    groups[i].children.push(item);
                } else {
                    let group = {
                        label: item[key],
                        children: [item],
                    };
                    groups.push(group);
                }
            });
            // 重新排序
            let i = groups.findIndex((group) => group.label == 'General');
            if (i > 0) {
                let temp = groups[0];
                groups[0] = groups[i];
                groups[i] = temp;
            }
            return groups;
        },
        refreshModel(params) {
            const request = {
                ...params,
                modelName: this.modelInfo.fullName,
                compIdent: this.modelInfo.compName,
            };
            editComponentParams(request).then(() => {
                saveModel({
                    projectId: this.projectData.id,
                    modelName: this.modelInfo.fullName,
                }).then(() => {
                    const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateSvgViewer');
                    if (linkageEvents.length) {
                        eventBus.$emit('updateSvgViewer', linkageEvents, this.modelInfo);
                    }
                });
            });
        },
    },
};
</script>

<style lang="less" scoped></style>
