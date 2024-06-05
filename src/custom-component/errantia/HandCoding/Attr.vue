<template>
    <div>
        <CommonAttr>
            <el-form>
                <el-form-item label="手写组件列表:">
                    <el-select
                        v-model="curComponent.propValue.codingName"
                        filterable
                        placeholder="Select"
                        style="width: 240px"
                    >
                        <el-option
                            v-for="item, index in options"
                            :key="index"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
import { useCodingCentre } from '@/hooks/useCodingCentre';
const { codingComponents } = useCodingCentre();

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options(){
            return codingComponents
        }
    },
};
</script>
