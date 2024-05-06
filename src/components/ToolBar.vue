<!-- 界面上方工具栏 -->
<template>
  <div class="toolbar-wrap">
    <div class="toolbar">
      <div class="tool-item" v-for="item in actions" :key="item.title" @click="handleAction(item)">
        <img :src="item.icon" class="item-icon" />
        <p class="item-title">{{ item.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import localforage from 'localforage';
  import { actions } from '@/config/toolbar'
  import { rootStore } from '@/stores/rootStore';
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const handleAction = (item) => {
    if (item.key === 'import') importFile()
    if (item.key === 'export') generateJson()
    if (item.key === 'canceldo') undo()
    if (item.key === 'redo') redo()
    if (item.key === 'preview') preview()
    if (item.key === 'clear') clearCanvas()
    if (item.key === 'generate') buildApp()
  }

  const importFile = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.id = 'fileId';
    input.click();
    input.onchange = () => {
      const files = input.files;
      const reader = new FileReader(); // 新建一个FileReader
      reader.readAsText(files[0], 'UTF-8'); // 读取文件
      reader.onload = (evt) => {
        // 读取完文件之后会回来这里 这是个异步
        const fileString = evt.target.result; // 读取文件内容
        const data = JSON.parse(fileString);
        rootStore.dataConfig.stateSet = data.dataCenter
        rootStore.dataConfig.actionSet = data.actionCenter
        rootStore.dataConfig.watchRegisters = data.watchRegisters
        rootStore.dataCenter.setComponentData(data.components)
      };
    }
  }
  const undo = () => {
    rootStore.snapshot.undo()
  }
  const redo = () => {
    rootStore.snapshot.redo()
  }
  const preview = () => {
    localforage.setItem('canvasData', JSON.stringify(rootStore.dataCenter.componentData));
    localforage.setItem('canvasStyle', JSON.stringify(rootStore.page.canvasStyleData), (err) => {
      const route = router.resolve({
        name: 'preview',
      });
      window.open(route.href, '_blank');
    });
  }
  const clearCanvas = () => {
    rootStore.dataCenter.setCurComponent({ component: null, index: null })
    rootStore.dataCenter.setComponentData([]);
    rootStore.snapshot.recordSnapshot()
    rootStore.dataConfig.stateSet = {}
    rootStore.dataConfig.actionSet = {}
    rootStore.dataConfig.watchRegisters = []
  }
  const generateJson = () => {
    // 创建一个包含JSON数据的对象
    var jsonData = {
      components: rootStore.dataCenter.componentData,
      dataCenter: rootStore.dataConfig.stateSet,
      actionCenter: rootStore.dataConfig.actionSet
    };
    // 将JSON对象转换为字符串
    var jsonString = JSON.stringify(jsonData);
    // 创建一个Blob对象
    var blob = new Blob([jsonString], { type: "application/json" });
    // 创建一个链接
    var url = URL.createObjectURL(blob);
    // 创建一个<a>元素
    var a = document.createElement('a');
    // 获取当前时间
    const now = new Date();

    // 获取时分秒的字符串，并转换为12_12_12格式
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours}_${minutes}_${seconds}`;

    // 构建文件名
    const fileName = `file_${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}_${timeString}.json`;

    a.download = fileName; // 设置文件名
    a.href = url;
    // 将<a>元素添加到文档中
    document.body.appendChild(a);
    // 模拟点击链接以触发下载
    a.click();
    // 清理链接和对象URL以释放内存
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
  const buildApp = () => {
    // 创建一个包含JSON数据的对象
    var jsonData = {
      components: rootStore.dataCenter.componentData,
      dataCenter: rootStore.dataConfig.stateSet,
      actionCenter: rootStore.dataConfig.actionSet,
      watchRegisters: rootStore.dataConfig.watchRegisters
    };
    // 将JSON对象转换为字符串
    var jsonString = JSON.stringify(jsonData);
    fetch('http://172.16.1.177:4000/buildAppVsix', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        appJson: jsonString
      })
    }).then(res => {
      res.json().then(data => {
        console.log(data)
        const downloadLink = document.createElement('a');
        downloadLink.href = data.fileUrl;
        // 点击链接触发下载
        downloadLink.click();
      })
    })
  }
</script>

<style lang="less" scoped>
.toolbar-wrap {
  display: flex;
  border-bottom: 1px solid #ddd;
  align-items: center;
}
.toolbar {
  padding: 15px 10px;
  white-space: nowrap;
  overflow-x: auto;
  background: #fff;
  display: flex;
  font-size: 12px;

  .tool-item {
    text-align: center;
    padding: 2px 6px;
    border: 1px solid transparent;
    cursor: pointer;

    .item-icon {
      width: 35px;
      height: 35px;
      display: block;
    }
    .item-title {
      margin: 2px 0;
      display: inline-block;
    }
    &:hover {
      background: #e5e5e5;
      border: 1px solid #e5e5e5;
    }
  }

  .canvas-config {
    display: inline-block;
    margin-left: 10px;
    font-size: 14px;
    color: #606266;

    input {
      width: 50px;
      margin-left: 4px;
      outline: none;
      padding: 0 5px;
      border: 1px solid #ddd;
      color: #606266;
    }

    span {
      margin-left: 10px;
    }
  }

  .insert {
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background: #fff;
    border: 1px solid #dcdfe6;
    color: #606266;
    text-align: center;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    transition: 0.1s;
    font-weight: 500;
    padding: 9px 15px;
    font-size: 12px;
    border-radius: 3px;
    margin-left: 10px;

    &:active {
      color: #3a8ee6;
      border-color: #3a8ee6;
      outline: 0;
    }

    &:hover {
      background-color: #ecf5ff;
      color: #3a8ee6;
    }
  }
  .import-file {
    position: relative;
    #fileId {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      opacity: 0;
    }
  }
}
.app-name {
  width: 200px;
}
</style>
