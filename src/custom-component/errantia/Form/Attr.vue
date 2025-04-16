<template>
    <div>
        <CommonAttr>
            <el-form size="small">
                <el-form-item label="表单项尺寸" >
                    <el-radio-group v-model="curComponent.propValue.size">
                        <el-radio-button value="large">large</el-radio-button>
                        <el-radio-button value="default">default</el-radio-button>
                        <el-radio-button value="small">small</el-radio-button>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="表单项对齐" label-position="right">
                    <el-radio-group v-model="curComponent.propValue.labelPosition">
                        <el-radio-button value="left">Left</el-radio-button>
                        <el-radio-button value="right">Right</el-radio-button>
                        <el-radio-button value="top">Top</el-radio-button>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="匹配内容选中：">
                    <el-input  v-model="curComponent.propValue.activateText"  size="small" />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
}
</script>