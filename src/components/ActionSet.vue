
<script setup>
import { computed, ref } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { javascript } from "@codemirror/lang-javascript"
import { rootStore } from '@/stores/rootStore'
import { ElMessageBox } from 'element-plus'

const extensions = [javascript(), noctisLilac]
const activeName = ref('')
activeName.value = Object.keys(rootStore.dataConfig.actionSet)[0]

const code = computed({
  get() {
    if (!activeName.value) return ''
    return rootStore.dataConfig.actionSet[activeName.value] || ''
  },
  set(value) {
    rootStore.dataConfig.actionSet[activeName.value] = value
  }
})

const autoActive = () => {
  if (!rootStore.dataConfig.actionSet[activeName.value]) {
    if (Object.keys(rootStore.dataConfig.actionSet).length > 0) {
      activeName.value = Object.keys(rootStore.dataConfig.actionSet)[0]
    } else {
      activeName.value = ''
    }
  }
}

const handleDelete = (name) => {
  delete rootStore.dataConfig.actionSet[name]
  autoActive()
}

const handleAdd = () => {
  ElMessageBox.prompt('请输入动作名称(英文和数字组合), 以init_开始的命名在页面初始化，会自动执行一次', '新增动作', {
    confirmButtonText: '提交',
    cancelButtonText: '取消',
    inputPattern: /^[a-zA-Z][_a-zA-Z0-9]*$/,
    inputErrorMessage: '无效的动作命名',
  })
  .then(({ value }) => {
    if(value.substring(0, 6) === 'Julia@') {
      return ElMessageBox.alert('动作名称不能以Julia@开头', '新增动作失败')
    }
    rootStore.dataConfig.addAction(value, `({dataCenter, globalUtils}, eventParams) => { 
      // TODO: 你的代码
    }`)
    autoActive()
  })
  
}
</script>

<template>
  <div class="btns-wrapper">
    <el-button 
      type="primary" 
      plain 
      class="add-btn" 
      style="width: 100%" 
      @click="handleAdd"
    >
      新增动作
    </el-button>
  </div>
  <div class="data-set-wrapper">
    <div class="action-list">
      <div 
        class="action-item" 
        :class="{ active: activeName === key }" 
        @click="activeName = key" 
        :key="key" 
        v-for="key in Object.keys(rootStore.dataConfig.actionSet)?.filter(item => !(item.substring(0, 6) === 'Julia@'))"
      >
        <span>{{ key }}</span>
        <el-icon @click.stop="handleDelete(key)" >
          <Delete />
        </el-icon>
      </div>
    </div>
    <div class="content">
      <codemirror
        v-if="activeName"
        v-model="code"
        :autofocus="false"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="extensions"
      />
    </div>
  </div>
</template>

<style lang="less" scoped>
.data-set-wrapper {
  height: 100%;
  display: flex;
  .action-list {
    width: 150px;
    display: flex;
    flex-direction: column;
    margin-right: 10px;
    .action-item {
      height: 30px;
      cursor: pointer;
      padding-left: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .action-item:hover, .action-item.active {
      color: #409eff;
    }
  }
  .content {
    flex: 1;
  }
}
</style>
