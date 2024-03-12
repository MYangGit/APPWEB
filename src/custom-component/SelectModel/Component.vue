<template>
    <div>
        <el-form style="padding: 20px" :inline="true">
            <el-form-item label="选择仓库">
                <el-select v-model="canvasStyleData.projectId" placeholder="请选择" @change="handleChange">
                    <el-option v-for="item in modelOptions" :key="item.id" :label="item.name" :value="item.id">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="选择模型">
                <el-cascader ref="cascader" v-model="canvasStyleData.modelId" placeholder="请选择" :props="props" :options="packageTree" style="width: 100%;" @change="handleModelChange">
                    <template slot-scope="{ node }">
                        <span class="tree-label">
                            <span class="name">{{ node.label }}</span>
                        </span>
                    </template>
                </el-cascader>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import request from '@/utils/request';
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent'

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: String,
            default: '',
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
                value: 'fullName',
                children: 'children',
                leaf: 'isLeaf',
            },
            cancelRequest: null,
            data: [],
            modelOptions: [],
            packageTree: [],
        };
    },
    computed: mapState(['canvasStyleData']),
    mounted() {
        this.getModules();
        if (this.canvasStyleData.projectId) {
            this.getPackageTree(this.canvasStyleData.projectId, true);
        }
        eventBus.$on('updateList', () => {
            this.getModules();
            if (this.canvasStyleData.projectId) {
                this.getPackageTree(this.canvasStyleData.projectId);
            }
        });
    },
    methods: {
        getModules() {
            this.cancelRequest = request(
                {
                    url: '/mohub/repo/listPrivate',
                    method: 'POST',
                    data: {
                        modelFullName: '',
                        nameOrEnglishName: '',
                        pageIndex: 1,
                        pageSize: 9,
                        searchContent: '',
                        status: '',
                    },
                },
                this,
                'data',
            ).then((res) => {
                this.modelOptions = res.data.data;
            });
        },
        getPackageTree(metadataTaskId, isFirst = false) {
            request({
                url: '/mohub/metadataTask/findLastedMetadataTask',
                method: 'GET',
                params: {
                    projectId: metadataTaskId,
                },
            }).then((res) => {
                request({
                    url: '/mohub/model/getPackageTree',
                    method: 'GET',
                    params: {
                        metadataTaskId: res.data.data.id,
                    },
                }).then((resp) => {
                    this.packageTree = this.dealTree(resp.data.data.modelTreeDTO.children);
                    if (isFirst && this.canvasStyleData.modelId) {
                        eventBus.$emit('changeModelId');
                    }
                });
            });
        },
        dealTree(data) {
            return data.map(i => {
                if (!i.children.length) {
                    delete i.children;
                }
                if (i.children) {
                    i.children = this.dealTree(i.children);
                }
                return i;
            })
        },
        handleChange(val) {
            eventBus.$emit('changeModel');
            this.getPackageTree(val);
        },
        handleModelChange(val) {
            eventBus.$emit('changeModel');
            this.canvasStyleData.metaData = this.$refs.cascader.getCheckedNodes()[0].data;
            eventBus.$emit('changeModelId');
        },
    },
}
</script>

<style lang="less" scoped>
</style>
