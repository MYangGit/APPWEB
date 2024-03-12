<template>
    <div class="no-position">
        <el-tree
            :data="data"
            :props="propValue.props || defaultProps"
            :lazy="propValue.isLazy"
            :load="loadNode"
            :highlight-current="true"
            :show-checkbox="propValue.isShowCheck"
            @node-click="handleNodeClick"
            @check-change="handleCheckChange"
        ></el-tree>
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import request from '@/utils/request';
import OnEvent from '../common/OnEvent';

export default {
    name: 'TreeList',
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
            data: [
                {
                    label: '一级 1',
                    children: [
                        {
                            label: '二级 1-1',
                            children: [
                                {
                                    label: '三级 1-1-1',
                                },
                            ],
                        },
                    ],
                },
                {
                    label: '一级 2',
                    children: [
                        {
                            label: '二级 2-1',
                            children: [
                                {
                                    label: '三级 2-1-1',
                                },
                            ],
                        },
                        {
                            label: '二级 2-2',
                            children: [
                                {
                                    label: '三级 2-2-1',
                                },
                            ],
                        },
                    ],
                },
                {
                    label: '一级 3',
                    children: [
                        {
                            label: '二级 3-1',
                            children: [
                                {
                                    label: '三级 3-1-1',
                                },
                            ],
                        },
                        {
                            label: '二级 3-2',
                            children: [
                                {
                                    label: '三级 3-2-1',
                                },
                            ],
                        },
                    ],
                },
            ],
            defaultProps: {
                children: 'children',
                label: 'label',
            },
            params: {},
        };
    },
    watch: {
        request: {
            handler() {
                if (this.request.url && this.request.method && this.request.data.length) {
                    this.updateData({});
                }
            },
            deep: true,
        },
    },
    mounted() {
        this.updateData({});
    },
    methods: {
        handleNodeClick(data) {
            const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'handleNodeClick');
            if (linkageEvents.length) {
                eventBus.$emit('handleNodeClick', linkageEvents, {
                    ...data,
                    simulationTaskId: this.params.simulationTaskId,
                });
            }
        },
        handleCheckChange(data, checked, indeterminate) {
            const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'handleNodeClick');
            if (linkageEvents.length) {
                eventBus.$emit('handleCheckChange', linkageEvents, {
                    ...data,
                    simulationTaskId: this.params.simulationTaskId,
                });
            }
        },
        updateData(params) {
            this.params = params;
            this.loadData('').then((res) => {
                this.data = [res.data.data];
            });
        },
        loadNode(node, resolve) {
            this.loadData(node.data.path).then((res) => {
                resolve(res.data.data.children);
            });
        },
        loadData(path) {
            const taskId = this.request.data.filter((i) => i[0] === 'taskId');
            return request({
                url: this.request.url,
                method: this.request.method,
                params: {
                    taskId: this.params.simulationTaskId || (taskId.length ? taskId[0][1] : ''),
                    path,
                },
            });
        },
    },
};
</script>

<style lang="less" scoped></style>
