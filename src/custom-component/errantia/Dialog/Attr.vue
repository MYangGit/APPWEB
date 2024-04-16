<template>
    <div>
        <CommonAttr>
            <el-form>
                <el-form-item label="标题：">
                    <el-input  v-model="curComponent.propValue.title"  size="small" />
                </el-form-item>
                <el-form-item label="显示浮窗：">
                    <el-checkbox v-model="curComponent.propValue.isShowVisible"  size="small" />
                </el-form-item>
                <el-form-item label="浮窗宽度：">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.width" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="浮窗高度：">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.height" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="取消表头：">
                    <el-checkbox v-model="curComponent.propValue.showDialogHeader"  size="small" />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
    methods: {
       
    },
};
</script>

<style lang="less" scoped>
</style>
