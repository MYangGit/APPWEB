<template>
    <div class="no-position">
        <el-button @click="openDialog">输出设置</el-button>
        <div class="outter">
            <div class="output">
                <div v-for="item, index in propValue.setting" :key="index">
                    <div class="iconfont icon-lamp" :style="{ color: valueList[index] ? valueList[index].color : '', fontSize: `70px` }"></div>
                    <div>{{ item.key }}</div>
                </div>
            </div>
            <div v-if="propValue.numberSetting.length" class="output">
                <div v-for="item, index in propValue.numberSetting" :key="index">
                    <div class="number-bg">8</div>
                    <div class="number">{{ NumberList[index] }}</div>
                </div>
            </div>
        </div>

        <el-dialog
            title="输出设置"
            :visible.sync="dialogVisible"
            width="1000px"
            :before-close="handleClose"
            :append-to-body="true"
        >
            <el-button type="primary" style="margin-bottom: 20px;" @click="handleAdd">添加灯泡</el-button>
            <div v-for="(item, index) in propValue.setting" :key="index">
                <el-form :inline="true" class="demo-form-inline">
                    <el-form-item label="绑定参数名">
                        <el-input v-model="item.key" style="width: 100px"></el-input>
                    </el-form-item>
                    <el-form-item label="警戒值">
                        <el-input-number v-model="item.warningValue" style="width: 100px"></el-input-number>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleDelete(index)">删除</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <el-button type="primary" style="margin-bottom: 20px;" @click="handleAddNumber">添加数码管</el-button>
            <div v-for="(item, index) in propValue.numberSetting" :key="'num' + index" class="border">
                <el-form v-for="(ite, ind) in item" :key="ind" :inline="true" class="demo-form-inline">
                    <el-form-item :label="ite.label">
                        <el-input v-model="ite.key" style="width: 100px"></el-input>
                    </el-form-item>
                    <el-form-item label="警戒值">
                        <el-input-number v-model="ite.warningValue" style="width: 100px"></el-input-number>
                    </el-form-item>
                    <el-form-item>
                        <el-button v-show="!ind" type="primary" @click="handleDeleteNumber(index)">删除</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent';

export default {
    name: 'ModelOutput',
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
            valueList: [],
            NumberList: [],
        };
    },
    computed: {},
    watch: {
        'propValue.setting': {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, val.concat(this.propValue.numberSetting.flat()).map(i => (['variableName', i.key])));
                }
            },
            deep: true,
        },
        'propValue.numberSetting': {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, val.flat().concat(this.propValue.setting).map(i => (['variableName', i.key])));
                }
            },
            deep: true,
        },
    },
    methods: {
        handleAddNumber() {
            this.propValue.numberSetting.push([
                {
                    label: '第一位参数名',
                    key: '',
                    warningValue: '',
                },
                {
                    label: '第二位参数名',
                    key: '',
                    warningValue: '',
                },
                {
                    label: '第三位参数名',
                    key: '',
                    warningValue: '',
                },
                {
                    label: '第四位参数名',
                    key: '',
                    warningValue: '',
                },
            ])
        },
        handleDeleteNumber(index) {
            this.propValue.numberSetting.splice(index, 1);
        },
        openDialog() {
            this.dialogVisible = true;
        },
        handleClose() {
            this.dialogVisible = false;
        },
        handleAdd() {
            this.propValue.setting.push({
                warningValue: '',
                key: '',
            })
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
        updateData(params) {
            // eslint-disable-next-line arrow-body-style
            this.valueList = this.propValue.setting.map(i => {
                const obj = { ...i };
                obj.color = params.find(j => j.name === i.key)?.value > (i.warningValue || 0) ? 'red' : '';
                return obj;
            });
            this.NumberList = this.propValue.numberSetting.map(i => {
                const values = i.map(j => {
                    const value = params.find(k => k.name === j.key)?.value > (j.warningValue || 0) ? '1' : '0';
                    return value;
                }).reduce((sum, i) => `${sum}${i}`, '');
                const sixteenValue = parseInt(values, 2).toString(16);
                return sixteenValue;
            });
            this.$forceUpdate();
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
.output {
    flex: 1;
    text-align: center;
    & > div {
        margin-bottom: 10px;
        position: relative;
        text-align: center;
    }
}
.outter {
    display: flex;
}
.border {
    border-bottom: 1px solid #efefef;
    margin-bottom: 20px;
}
.number {
    display: inline-block;
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 70px;
    font-size: 60px;
    font-family: 'digifaw';
    color: orange;
}
.number-bg {
    display: inline-block;
    z-index: 1;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 50px;
    height: 70px;
    color: rgba(205, 205, 205, 0.5);
    font-size: 60px;
    font-family: 'digifaw';
    background-color: #000;
}
</style>
