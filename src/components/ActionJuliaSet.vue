
<script setup>
import { computed, ref } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { javascript } from "@codemirror/lang-javascript"
import { ElMessageBox } from 'element-plus'
import { useJuliaCentre } from '@/hooks/useJuliaCentre'
import { erPicText, erFlex } from 'errantia'
import BindData from './BindData/index.vue'
import { isEmpty } from '@/utils/utils'
 
const juliaCentre = useJuliaCentre()
juliaCentre.init()
const extensions = [javascript(), noctisLilac]
const code = computed({
  get() {
    if (isEmpty(juliaCentre.currentFun.name)) return ''
    return juliaCentre.currentFun.code || ''
  },
  set(value) {
    juliaCentre.setJuliaFunList({uuidName: juliaCentre.currentFun.name, data: {code: value}})
  }
})

const handleDelete = (name) => {
  juliaCentre.setJuliaFunList({type: 'delete', uuidName: name})
}

const handleAdd = () => {
  ElMessageBox.prompt('请输入动作名称(英文和数字组合), 以init_开始的命名在页面初始化，会自动执行一次', '新增动作', {
    confirmButtonText: '提交',
    cancelButtonText: '取消',
    inputPattern: /^[a-zA-Z][_a-zA-Z0-9]*$/,
    inputErrorMessage: '无效的动作命名',
  })
  .then(({ value }) => {
    const newFunData = {
      name: value,
      type: 'Julia',
      props:{},
      returns: {},
      code: `// TODO: 你的代码`
    }
    juliaCentre.setJuliaFunList({type: 'add', uuidName: value, data: newFunData})
  })
}
const openImportParam = ref(false)
const handleAction = () => {
  openImportParam.value = true
}
// 命名a-z 如果超过26个则命名为a_1 - z_N
const handConfirmBindData = (val) => {
  const oldProps = Object.keys(juliaCentre.currentFun.props)
  let propsName = `_${String.fromCharCode(97 + oldProps.length % 26)}_`
  if(oldProps.includes(propsName)) {
    let i = 1;
    for(i; i < 26; i++) {
      let newPropsName = `_${String.fromCharCode(97 + (oldProps.length + i) % 26)}_`
      if(!oldProps.includes(newPropsName)) {
        propsName = newPropsName
        break
      }
    }
    if(i >= 26) {
      if(oldProps.includes(propsName)){
        let ext = 1;
        let newName = propsName;
        while (oldProps.some(item => item === newName)) {
          newName = `${item}_${ext}`;
          ext++;
        }
        propsName = newName;
      }
    }
  }
  const newProps = {
    [propsName]: val
  }
  juliaCentre.updateCurrentFunProps({data: newProps})
  openImportParam.value = false
}

const handleParamCommand = (command) => {
  if(command.type === 'delete') {
    juliaCentre.updateCurrentFunProps({type: 'delete', data:{[command.name]: command.name}})
  }
}

const handleBlur = () => {
  juliaCentre.setCurrentFun(juliaCentre.currentFun?.name)
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
        :class="{ active: juliaCentre.currentFun.name === item.name }" 
        @click="juliaCentre.setCurrentFun(item.name)"
        :key="item.name" 
        v-for="item in juliaCentre.juliaFunList"
      >
        <span>{{ item.name }}</span>
        <el-icon @click.stop="handleDelete(item.name)" >
          <Delete />
        </el-icon>
      </div>
    </div>
    <div v-if="!isEmpty(juliaCentre.currentFun)" style="width: 100%;">
      <div class="edit-param">
        <div class="param">
          <erFlex aligns="center" style="width: max-content; height: max-content; gap: 10px;">
            <erPicText
              iconPath="https://img.icons8.com/ios/452/plus-math.png"
              title="引入参数"
              @onAction="handleAction"
            />
            <div v-if="!isEmpty(juliaCentre.currentFun?.props)" class="example">
              "示例: x = ${_a_} 等同于变量 x 的值为引入参数 _a_ 的值, 引入参数需要 ${你的参数名}, 例如: ${_a_}"
            </div>
          </erFlex>
          <div class="conrainer">
            <div 
              class="conrainer-item"
              v-for="item in Object.entries(juliaCentre.currentFun?.props ?? {})"
              :key="item[0]"
             >
              <el-dropdown trigger="contextmenu" @command="handleParamCommand">
                 <span>
                  <span style="color:deepskyblue;font-weight: bold;">{{ item[0] }} : </span>{{ item[1].join('.') }}
                 </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{type:'delete', name: item[0]}">删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </div>
      <div class="content">
        <codemirror
          v-if="juliaCentre.currentFun.name"
          v-model="code"
          :autofocus="false"
          :indent-with-tab="true"
          :tab-size="2"
          :extensions="extensions"
          @blur="handleBlur"
        />
      </div>
    </div>
  </div>
  <BindData 
    title="选择参数"
    :openImport="openImportParam"  
    @cancel="openImportParam = false"
    @confirm="handConfirmBindData"
  />
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
  .edit-param {
      width: 100%;
      height: 200px;
      border-left: 31px solid #F2F1F8;
      .param {
        width: 100%;
        height: 98%;
        padding: 10px;
        border-left: 1px solid #DDDDDD;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        .example {
          background-color: #E1DEF4; 
          color: #9995b7;
          height: 30px;
          line-height: 30px;
          font-size: 14px;
        }
      }
  }
  .content {
    flex: 1;
  }
  .conrainer{
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    .conrainer-item {
      padding: 5px 10px;
      background-color: #F2F1F8;
      border-radius: 10px;
      display: flex;
      align-items: center;
    }
  }
}
</style>
