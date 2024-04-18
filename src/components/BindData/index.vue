<template>
    <el-dialog 
        v-model="showOpenImport" 
        :title="title" 
        width="800"
    >
        <el-cascader 
            v-model="selectedKeys" 
            :props="{checkStrictly: true}" 
            :options="getOptions" 
        />
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="emit('cancel')">Cancel</el-button>
                    <el-button type="primary" @click="handleConfirm">
                    Confirm
                    </el-button>
                </div>
            </template>
    </el-dialog>
</template>

<script setup >
import { ref, computed, watchEffect } from 'vue'
import { rootStore } from '@/stores/rootStore';

const emit = defineEmits(['cancel', 'confirm'])
const props = defineProps({
    openImport: {
        type: Boolean,
        default: false
    },
    title: {
        type: String,
        default: '绑定数据'
    }
})
const selectedKeys = ref('')
const showOpenImport = ref(props.openImport)
watchEffect(
    () => {
        showOpenImport.value = props.openImport
        if(!showOpenImport.value) {
            selectedKeys.value = ''
        }
    }
)

const getOptions = computed(() => {
    return extractKeys(rootStore.dataConfig.stateSet);
})

const extractKeys = (obj) => {
    let result = [];
    for (let key in obj) {
        if (typeof obj[key] === 'object' && !Array.isArray(obj[key])) {
            result.push({
                label: key,
                value: key,
                children: extractKeys(obj[key])
            });
        } else {
            result.push({
                label: key,
                value: key
            });
        }
    }
    return result;
}

const handleConfirm = () => {
    emit('confirm', selectedKeys.value)
}

</script>

<style scoped lang="less">
  @import './index.less';
</style>