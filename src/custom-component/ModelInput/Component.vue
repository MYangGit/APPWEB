<template>
    <div class="no-position">
        <el-button style="margin-bottom: 20px" @click="openDialog">输入设置</el-button>
        <el-form class="demo-form-inline">
            <el-form-item v-for="item, index in propValue.setting" :key="index" :label="item.key" label-width="100px">
                <el-select v-if="item.type === 'select'" v-model="propValue.value[item.key]" style="width: 100px">
                    <el-option v-for="i, ind in item.options" :key="ind" :label="i.label" :value="i.value"></el-option>
                </el-select>
                <el-input v-else v-model="propValue.value[item.key]" style="width: 100px"></el-input>
            </el-form-item>
        </el-form>

        <el-dialog
            title="输入设置"
            :visible.sync="dialogVisible"
            width="1000px"
            :before-close="handleClose"
            :append-to-body="true"
        >
            <el-button type="primary" style="margin-bottom: 20px" @click="handleAdd">添加</el-button>
            <div v-for="(item, index) in propValue.setting" :key="index">
                <el-form :inline="true" class="demo-form-inline">
                    <el-form-item label="类型">
                        <el-select v-model="item.type" style="width: 100px">
                            <el-option label="输入框" value="input"></el-option>
                            <el-option label="下拉框" value="select"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="绑定参数名">
                        <el-input v-model="item.key" style="width: 100px"></el-input>
                    </el-form-item>
                    <el-form-item v-if="item.type === 'select'" label="配置项">
                        <el-button size="small" @click="add(item.options)">+</el-button>
                        <el-form
                            v-for="(ite, ind) in item.options"
                            :key="ind"
                            :inline="true"
                            label-width="60px"
                            size="small"
                            style="padding: 10px 0"
                        >
                            <el-form-item label="label" style="margin-bottom: 0">
                                <el-input v-model="ite.label" style="width: 80px" />
                            </el-form-item>
                            <el-form-item label="value" style="margin-bottom: 0">
                                <el-input v-model="ite.value" style="width: 80px" />
                            </el-form-item>
                            <el-form-item label="" style="margin-bottom: 0">
                                <el-button @click="deleteRow(item.options, ind)">-</el-button>
                            </el-form-item>
                        </el-form>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleDelete(index)">删除</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="submit()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent';

export default {
    name: 'ModelInput',
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
            dialogVisible: false,
        };
    },
    computed: {},
    watch: {
        'propValue.value': {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, { ...val });
                }
            },
            deep: true,
        },
    },
    methods: {
        submit() {
            this.propValue.value = {};
            this.dialogVisible = false;
        },
        openDialog() {
            this.dialogVisible = true;
        },
        handleClose() {
            this.dialogVisible = false;
        },
        handleAdd() {
            this.propValue.setting.push({
                type: '',
                key: '',
                options: [],
            });
        },
        handleDelete(index) {
            this.propValue.setting.splice(index, 1);
        },
        add(options) {
            options.push({
                label: '',
                value: '',
            });
        },
        deleteRow(options, index) {
            options.splice(index, 1);
        },
    },
};
</script>

<style lang="less" scoped>
.no-position {
    .el-dialog__body {
        // height: 600px;
    }
}
</style>
