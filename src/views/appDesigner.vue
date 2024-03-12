<script setup>
import { ref } from 'vue';
import { deepCopy, getQueryVariable } from '@/utils/utils';
import componentList from '@/custom-component/component-list'; // 左侧列表数据
import generateID from '@/utils/generateID';

import ToolBar from '@/components/ToolBar.vue';
import ComponentList from '@/components/ComponentList.vue';
import RealTimeComponentList from '@/components/RealTimeComponentList.vue';
import Editor from '@/components/Editor/index.vue';
import CodeEdit from '@/components/CodeEdit.vue';
import { useDataCenterStore } from '@/stores/dataCenter';
import { useComposeStore } from '@/stores/compose';
import { usePageStore } from '@/stores/page';
import { useSnapShotStore } from '@/stores/snapshot';
import { useEditorStore } from '@/stores/editor';
import { useContextMenuStore } from '@/stores/contextmenu';

const dataCenterStore = useDataCenterStore();
const composeStore = useComposeStore()
const pageStore = usePageStore()
const snapShotStore = useSnapShotStore()
const editorStore = useEditorStore()
const contextMenuStore = useContextMenuStore()

const mode = ref('design')
const activeName = ref('attr')

// 组件拖拽的动作
const handleDrop = (e) => {
  e.preventDefault();
  e.stopPropagation();
  const index = e.dataTransfer.getData('index');
  const rectInfo = composeStore.editor.getBoundingClientRect();
  if (index) {
    const component = deepCopy(componentList[index]);
    component.style.top = e.clientY - rectInfo.y;
    component.style.left = e.clientX - rectInfo.x;
    if (component.type === 'report') {
      component.style.left = 0;
    }
    component.id = generateID();
    if (component.component === 'Tabs') {
      component.tabs = new Array(3).fill(1).map((i, j) => ({
        name: generateID(),
        label: `Tab${j + 1}`,
      }));
    } else if (component.component === 'GridLayout') {
      component.items = new Array(3 * 3).fill(1).map((i, j) => ({
        name: generateID(),
        label: `Grid${j + 1}`,
      }));
    }
    if (component.style.width.toString().includes('%')) {
      component.style.width =
        (Number(pageStore.canvasStyleData.width) * parseFloat(component.style.width)) / 100;
    }
    if (dataCenterStore.componentData.filter(i => i.component === component.component).length) {
      component.label += dataCenterStore.componentData.filter(i => i.component === component.component).length;
    }
    dataCenterStore.addComponent({ component })
    snapShotStore.recordSnapshot()
  }
}

const handleDragOver = (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'copy';
}

const handleMouseDown = (e) => {
  e.stopPropagation();
  editorStore.setClickComponentStatus(false)
  editorStore.setInEditorStatus(true)
}

const deselectCurComponent = (e) => {
  if (!editorStore.isClickComponent) {
    dataCenterStore.setCurComponent({
      component: null,
      index: null,
    })
  }

  // 0 左击 1 滚轮 2 右击
  if (e.button != 2) {
    contextMenuStore.hideContextMenu()
  }
}

</script>

<template>
  <div class="home">
    <ToolBar></ToolBar>
    <main>
      <!-- 左侧组件列表 -->
      <section class="left">
        <el-tabs type="border-card" tab-position="left" class="sidebar">
          <el-tab-pane label="组件库">
            <ComponentList />
          </el-tab-pane>
          <el-tab-pane label="组件浏览器">
            <RealTimeComponentList />
          </el-tab-pane>
        </el-tabs>
      </section>
      <!-- 中间画布 -->
      <section class="center">
        <div class="mode">
          <el-radio-group v-model="mode" size="small">
            <el-radio-button value="design">设计视图</el-radio-button>
            <el-radio-button value="code">代码视图</el-radio-button>
          </el-radio-group>
        </div>
        <div
          v-if="mode === 'design'"
          class="content"
          @drop="handleDrop"
          @dragover="handleDragOver"
          @mousedown="handleMouseDown"
          @mouseup="deselectCurComponent"
        >
          <Editor />
        </div>
        <div v-else class="content">
          <CodeEdit />
        </div>
      </section>
      <!-- 右侧属性列表 -->
      <section class="right">
        <el-tabs v-if="dataCenterStore.curComponent" v-model="activeName" class="no-padding sidebar" type="border-card" tab-position="right">
          <el-tab-pane label="属性" name="attr">
            <component :is="dataCenterStore.curComponent.component + 'Attr'" />
          </el-tab-pane>
          <el-tab-pane label="动画" name="animation" style="padding-top: 20px">
            <!-- <AnimationList /> -->
          </el-tab-pane>
          <el-tab-pane label="事件" name="events" style="padding-top: 20px">
            <!-- <EventList /> -->
          </el-tab-pane>
        </el-tabs>
        <!-- <CanvasAttr v-show="!curComponent"></CanvasAttr> -->
      </section>
    </main>
  </div>
</template>

<style lang="less">
.home {
  height: 100vh;
  background: #fff;
  display: flex;
  flex-direction: column;

  main {
    height: 0;
    flex: 1;
    display: flex;
    position: relative;

    .left {
      width: 250px;
      border-right: 1px solid #ddd;
      & > div {
        overflow: auto;

        &:first-child {
          border-bottom: 1px solid #ddd;
        }
      }
    }

    .right {
      width: 308px;
      right: 0;
      top: 0;
      border-left: 1px solid #ddd;

      .el-select {
        width: 100%;
      }
    }

    .center {
      flex: 1;
      background: #f5f5f5;
      overflow: auto;
      padding: 40px 20px;
      position: relative;

      .content {
        width: 100%;
        height: 100%;
        overflow: auto;
      }

      .mode {
        position: absolute;
        top: 5px;
        right: 20px;
      }
    }
  }

  .placeholder {
    text-align: center;
    color: #333;
  }

  .global-attr {
    padding: 10px;
  }
}
.right .el-tabs__nav-scroll {
  padding-left: 20px;
}
</style>
