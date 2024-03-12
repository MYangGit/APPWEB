<template>
    <div class="no-position">
        <el-tree
            v-if="isLoad"
            ref="tree"
            node-key="fullName"
            :expand-on-click-node="false"
            :props="props"
            :load="loadNode"
            :render-content="renderContent"
            highlight-current
            lazy
            @node-click="handleNodeClick"
        />
    </div>
</template>

<script>
import { getClasses } from '@/utils/websocket';
import eventBus from '@/utils/eventBus';
import { moIcon } from '@/utils/editor/moIcon.js';
import { mapState } from 'vuex';
import OnEvent from '../common/OnEvent';

export default {
    name: 'ModelUser',
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
            props: {
                label: 'ident',
                children: 'children',
                isLeaf: 'isLeaf',
            },
            currentNode: null,
            isLoad: false,
        };
    },
    computed: mapState(['editMode', 'projectData']),
    mounted() {
        eventBus.$on('connected', () => {
            this.isLoad = false;
            this.$nextTick(() => {
                this.isLoad = true;
            });
        });
        if (this.editMode === 'edit') {
            this.isLoad = true;
        }
    },
    methods: {
        renderContent(h, { node, data }) {
            return (
                <div class="target" title={node.label} id={node.id}>
                    <img src={data.icon} class={data.hasIcon ? 'tree-img' : 'tree-img1'} />
                    <span class="tree-label">
                        <span class="name">{node.label}</span>
                    </span>
                </div>
            );
        },
        handleNodeClick(data, node, e) {
            this.currentNode = node;
            this.updateModelTab(data);
        },
        updateModelTab(data) {
            const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateModelTab');
            if (linkageEvents.length) {
                eventBus.$emit('updateModelTab', linkageEvents, data);
            }
        },
        loadNode(node, resolve) {
            if (node.level == 0) {
                this.loading = true;
            }
            this.loadClass(resolve, node);
            return resolve([]);
        },
        loadClass(resolve, node) {
            const modelName = node.level == 0 ? '' : node.data.fullName;
            getClasses({ modelName }).then((res) => {
                let result = [];
                res.classes.forEach((item) => {
                    if (node.level == 0) {
                        if (item.libType == 'development' && item.encryptLevel != 'Access.hide') {
                            result.push(this.createNodeData(item));
                        }
                    } else if (item.encryptLevel != 'Access.hide') {
                        result.push(this.createNodeData(item));
                    }
                });
                resolve(result);
                this.loading = false;
            });
        },
        createNodeData(data) {
            let hasIcon = true;
            if (!data.icon.icon.length && !data.icon.components.length) {
                hasIcon = false;
            }
            if (!data.isPublish) {
                data.encryptLevel = '';
            }
            return {
                ident: data.icon.ident,
                fullName: data.icon.fullName,
                description: data.icon.description,
                specialization: data.icon.specialization,
                isLeaf: !data.isPackage,
                // eslint-disable-next-line new-cap
                icon: new moIcon(data.icon).base64,
                projectId: data.projectId || this.projectData.id,
                editable: this.projectData.editable,
                encryptLevel: data.encryptLevel,
                hasIcon,
            };
        },
    },
};
</script>

<style lang="less" scoped>
::v-deep .el-tree-node__content {
    height: 30px;
}
::v-deep .target {
    overflow: hidden;
    flex: 1;
    display: flex;
    align-items: center;
}
::v-deep .tree-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #999;
    .name {
        // font-size: 14px;
        color: #333;
    }
}
::v-deep .tree-img {
    height: 22px;
    width: 22px;
    object-fit: cover;
    margin-right: 5px;
}

::v-deep .tree-img1 {
    height: 22px;
    width: 0;
    object-fit: cover;
}
</style>
