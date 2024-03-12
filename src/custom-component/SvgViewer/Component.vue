<template>
    <div class="no-position">
        <TySvgViewer :value="value" @click="singleClick" @dbclick="doubleClick"></TySvgViewer>
        <!-- <div id="modelEditor" class="moEditor"></div> -->
    </div>
</template>

<script>
import { mapState } from 'vuex';
import { getDiagram } from '@/utils/websocket';
import { moEditor } from '@/utils/editor';
import { mxUtils } from '@/utils/editor/mxgraph';
import eventBus from '@/utils/eventBus';
import request from '@/utils/request';
import OnEvent from '../common/OnEvent';

export default {
    name: 'SvgViewer',
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
            value: '',
            editor: null,
            modelInfo: {},
        };
    },
    computed: mapState(['canvasStyleData']),
    watch: {
        request: {
            handler() {
                this.getData();
            },
            deep: true,
        },
    },
    mounted() {
        this.getData();
        eventBus.$on('connected', () => {
            if (this.canvasStyleData.modelId) {
                // this.updateData({
                //     fullName: this.canvasStyleData.modelId[0],
                // });
                this.updateView(this.canvasStyleData.metaData);
            }
        });
        eventBus.$on('changeModelId', () => {
            if (this.canvasStyleData.modelId) {
                // this.updateData({
                //     fullName: this.canvasStyleData.modelId[this.canvasStyleData.modelId.length - 1],
                // });
                this.updateView(this.canvasStyleData.metaData);
            }
        });
        if (this.canvasStyleData.modelId) {
            this.updateView(this.canvasStyleData.metaData);
        }
        // this.$nextTick(() => {
        //     this.init();
        // });
    },
    methods: {
        init() {
            const container = document.getElementById('modelEditor');
            this.editor = new moEditor(container);
            const { graph } = this.editor;
            graph.getSelectionModel().addListener(
                'change',
                mxUtils.bind(this, function (sender, evt) {
                    let cells = sender.cells.filter((cell) => {
                        return cell.vertex && cell.data && cell.data.ident;
                    });
                    const compName = cells.length == 1 ? cells[0].data.ident : '';
                    const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'componentChange');
                    if (linkageEvents.length && compName) {
                        eventBus.$emit('componentChange', linkageEvents, {
                            compName,
                            fullName: this.modelInfo.fullName,
                        });
                    }
                }),
            );
        },
        singleClick(id) {
            console.log(id);
        },
        doubleClick(id) {
            console.log(id);
        },
        updateData(params) {
            this.modelInfo = params;
            if (params.specialization === 'package') {
                return;
            }
            getDiagram({ modelName: params.fullName }).then((res) => {
                this.value = res.diagram;
                this.value.editable = true;
                this.value.compName = '';
                this.editor.refreshGraph(this.value, false);
            });
        },
        getData() {
            if (this.request.url && this.request.method) {
                request({
                    url: this.request.url,
                    method: this.request.method,
                }).then((res) => {
                    this.editor.refreshGraph(res.data, false);
                });
            }
        },
        // 获取组件所在的模型
        async getParentModel(component) {
            const { id, hostLocation, commitId } = this.canvasStyleData.metaData;
            const url =
                hostLocation +
                '/alchemy/model/findParentModel?metadataTaskId=' +
                id +
                '&typeFullName=' +
                component.typeFullName +
                '&version=' +
                commitId;
            const res = await request(url);
            if (res.data.code == 0) {
                return res.data.data;
            }
        },
        // 更新模型相关视图
        async updateView(data) {
            console.log(data);
            // 这个字段模型才有 区分模型和组件
            if (!data.metadataChildTaskId) {
                data = await this.getParentModel(data);
            }
            if (!data) {
                return;
            }
            const { moUrl, iconUrl, diagramSvgUrl, infoUrl, hostLocation } = data;
            if (diagramSvgUrl) {
                const svg = diagramSvgUrl ? hostLocation + '/alchemy/' + diagramSvgUrl : '';
                const value = await request(svg);
                this.value = value.data;
            }
        },
    },
};
</script>

<style lang="less" scoped>
.moEditor {
    width: 100%;
    height: 100%;
    position: relative;
}
</style>
