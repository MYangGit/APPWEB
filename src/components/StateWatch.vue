
<script setup>
import { computed, ref } from 'vue'
import { rootStore } from '@/stores/rootStore'

const tableData = computed(() => {
  return rootStore.dataConfig.watchRegisters
})

const dialogVisible = ref(false)

const form = ref({
  index: -1,
  title: '',
  state: '',
  action: ''
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

const getOptions = () => {
  let options = extractKeys(rootStore.dataConfig.stateSet);
  return options;
}

const getActionOptions = () => {
  return Object.keys(rootStore.dataConfig.actionSet)
}

const openNewDialog = () => {
  form.value = {
    index: -1,
    title: '',
    state: '',
    action: ''
  }
  dialogVisible.value = true
}

const handleSubmit = () => {
  dialogVisible.value = false
  if (form.value.index > -1) {
    rootStore.dataConfig.watchRegisters.splice(form.value.index, 1, {
      title: form.value.title,
      state: form.value.state,
      action: form.value.action,
    })
  } else {
    rootStore.dataConfig.watchRegisters.push({
      title: form.value.title,
      state: form.value.state,
      action: form.value.action,
    })
  }
}

const deleteRow = (index) => {
  rootStore.dataConfig.watchRegisters.splice(index, 1)
}

const editRow = (index) => {
  let item = tableData.value[index]
  form.value = {
    index,
    title: item.title,
    state: item.state,
    action: item.action,
  }
  dialogVisible.value = true
}


</script>
<template>
  <div class="sw-wrapper">
    <el-button type="primary" plain class="add-btn" style="width: 100%" @click="openNewDialog">添加监听</el-button>
    <el-table
      :data="tableData"
      style="width: 100%"
      class="table-wrapper"
      empty-text="无数据"
    >
      <el-table-column prop="title" label="标题" width="320" />
      <el-table-column prop="state" label="数据"/>
      <el-table-column prop="action" label="动作"/>
      <el-table-column fixed="right" label="操作" width="120">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="deleteRow(scope.$index)"
          >
            Remove
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="editRow(scope.$index)"
          >
            Edit
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      v-model="dialogVisible"
      :title="form.index > -1 ? `编辑数据监听` : `添加数据监听`"
      width="500"
    >
    <el-form :model="form" label-width="auto" style="max-width: 600px">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="请输入标题，用于标识描述" />
      </el-form-item>
      <el-form-item label="数据字段">
        <el-cascader v-model="form.state" :props="{checkStrictly: true}" :options="getOptions()" />
      </el-form-item>
      <el-form-item label="动作">
        <el-select v-model="form.action" placeholder="请选择动作">
          <el-option v-for="item in getActionOptions()" :key="item" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>
    </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
<style lang="less" scoped>
.sw-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.add-btn {
  margin: 10px 0;
  outline: none;
  flex: 0;
}
.table-wrapper {
  flex: 1;
}
</style>
<style>
label {
  margin-bottom: 0;
}
</style>
