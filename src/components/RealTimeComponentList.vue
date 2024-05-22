<script setup>
import { useDataCenterStore } from '@/stores/dataCenter'
import { useSnapShotStore } from '@/stores/snapshot';

const dataCenterStore = useDataCenterStore()
const snapShotStore = useSnapShotStore()

const transformIndex = (index) => {
  return dataCenterStore.componentData.length - 1 - index;
}

// 提交当前组件信息到仓库
const setCurComponent = (index) => {
  dataCenterStore.setCurComponent({ component: dataCenterStore.componentData[index] })
}

const onClick = (index) => {
  setCurComponent(index);
}

const getComponent = (index) => {
  return dataCenterStore.componentData[dataCenterStore.componentData.length - 1 - index];
}

// 上，下移 删除动作 原理：commit提交触发仓库画布组件数据（componentData）的（前后位置，存在与否）更新
// 然后此子组件RealTimeComponentList 重新渲染更新后的数据componentData 就会引入当前视图的变化
const deleteComponent = () => {
  setTimeout(() => {
    dataCenterStore.deleteComponent()
    snapShotStore.recordSnapshot()
  });
}

const upComponent = () => {
  setTimeout(() => {
    dataCenterStore.upComponent()
    snapShotStore.recordSnapshot()
  })
}

const downComponent = () => {
  setTimeout(() => {
    dataCenterStore.downComponent()
    snapShotStore.recordSnapshot()
  });
}
</script>

<!--  左侧下方当前被拖拽至画布的组件列表 -->
<template>
  <div class="real-time-component-list">
    <div
      v-for="(item, index) in dataCenterStore.componentData"
      :key="index"
      class="list"
      :class="{ actived: transformIndex(index) === dataCenterStore.curComponentIndex }"
      @click="onClick(transformIndex(index))"
    >
      <!-- 组件的icon图标 -->
      <span class="iconfont" :class="'icon-' + getComponent(index).icon"></span>
      <!-- 组件的文字标题 -->
      <span>{{ getComponent(index).label }}</span>

      <!-- 组件上移，下移，删除三个点击面板 -->
      <!-- <div class="icon-container">
        <span class="iconfont el-icon-upload2" title="上移" @click="upComponent(transformIndex(index))"></span>
        <span class="iconfont el-icon-download" title="下移" @click="downComponent(transformIndex(index))"></span>
        <span class="iconfont el-icon-delete" title="删除" @click="deleteComponent(transformIndex(index))"></span>
      </div> -->
      <div class="icon-container">
        <el-icon @click="deleteComponent(transformIndex(index))"><Delete /></el-icon>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.real-time-component-list {
  height: 100%;
  overflow-y: auto;

  .list {
    height: 30px;
    cursor: grab;
    text-align: center;
    color: #333;
    display: flex;
    align-items: center;
    font-size: 12px;
    padding: 0 10px;
    position: relative;
    user-select: none;

    &:active {
      cursor: grabbing;
    }

    &:hover {
      background-color: rgba(200, 200, 200, 0.2);

      .icon-container {
        display: block;
      }
    }

    .iconfont {
      margin-right: 4px;
      font-size: 16px;
    }

    // .icon-wenben,
    // .icon-tupian {
    //   font-size: 14px;
    // }

    .icon-container {
      position: absolute;
      right: 10px;
      display: none;
      .iconfont {
        cursor: pointer;
      }
    }
  }

  .actived {
    background: #ecf5ff;
    color: #409eff;
  }
}
</style>