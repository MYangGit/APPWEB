<template>
  <div>
    <div class="drag-container" ref="dragContainer">
      <div
        class="draggable-item"
        v-for="item in getfilterMinItems"
        :key="item.uuid"
        :style="getItemStyle(item.uuid, item.style)"
        @dblclick.stop="selectComponent(item, $event)"
        @mousedown.passive="handleCurDragStart(item.style, $event)"
      >
        <div class="header">
          <div>
            <span class="title">{{ item.name }}</span>
          </div>
          <div class="window-controls">
            <div class="min-btn" @click.stop="item.isMinimized = true">
              <el-icon><SemiSelect /></el-icon>
            </div>
            <div class="max-btn" @click.stop="handleMaximize(item)"> 
              <el-icon v-if="getMaximize(item.isMaximized)"  style="transform: rotate(180deg)"><CopyDocument /></el-icon>
              <el-icon v-else ><FullScreen /></el-icon>
            </div>
            <div class="close-btn" @click.stop="handleCloseBox(item.uuid)">    
              <el-icon><CloseBold /></el-icon>
            </div>
          </div>
        </div>
        <div class="window-content">
          <erPlot
            v-if="item.contentType === 'plot'"
            style="width: 100%; height: 100%;"
            :prop-value="item.propValue"
            :element="{dataBinds: {}}"
          />
          <erTable
            v-else-if="item.contentType === 'table'"
            style="width: 100%; height: 100%; background-color: #fff; color: black;"
            :prop-value="item.propValue"
            :element="{
              dataBinds: {},
              actionBinds: {
                onClickRow: '',
                onClickOperate:'',
                onNameBlur:'',
                onDbClickRow:'',
                onContextMenuRow:'',
                onClickCheckbox:''
              }
            }"
          />
        </div>
        <div
          class="shape-point"
          v-if="getUuid === item.uuid"
          v-for="point in RESIZE_POINTS"
          :key="point"
          :style="getPointStyle(point)"
          @mousedown.stop="handleZoomStart(point, curWinData.style, $event)"
        ></div>
      </div>
      <div class="minBox" v-if="!isEmpty(getMinItems)">
        <el-dropdown placement="top-end">
          <el-button><el-icon><Files /></el-icon></el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-for="item in getMinItems"
                :key="item.uuid"
              >
                <div class="action-item">
                  <div @click.stop="item.isMinimized = false" style="margin-right: 10px;">{{item.name}}</div>
                  <el-icon @click.stop="handleCloseBox(item.uuid)"><Close /></el-icon>
                </div>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { isEmpty, getComputedGet, getComputedSet, } from "@/utils/utils";
import { useDragZoomCentre } from "@/hooks/useDragZoomCentre";
import { rootStore } from "@/stores/rootStore";
import erPlot from "../Plot/Component.vue";
import erTable from "../Table/Component.vue";
import { useEventCentre } from '@/hooks/useEventCentre';

// 常量配置
const RESIZE_POINTS = ["lt", "t", "rt", "r", "rb", "b", "lb", "l"];
const CURSOR_MAP = {
  lt: "nw-resize",
  t: "n-resize",
  rt: "ne-resize",
  r: "e-resize",
  rb: "se-resize",
  b: "s-resize",
  lb: "sw-resize",
  l: "w-resize",
};

const props = defineProps({
  propValue: {
    type: Object,
    default: () => ({
      funParam: "",
      curWinData: {},
      winDataList: [],
    })
  },
  element: {
    type: Object,
    default: () => ({})
  }
})

// 计算属性，最小化项
const getMinItems = computed(()=>{
  return winDataList?.value?.filter(item => item.isMinimized) || []
})

// 计算属性，最小化项
const getfilterMinItems = computed(()=>{
  return winDataList?.value?.filter(item => !item.isMinimized) || []
})

const getUuid = computed(()=>{
  return curWinData?.value.uuid || ''
})

const curWinData = computed({
  get: () => {
    return getComputedGet(
      'curWinData',
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    )
  },
  set: (val) => {
    getComputedSet(
      'curWinData',
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    )
  }
})

const winDataList = computed({
  get: () => {
    return getComputedGet(
      'winDataList',
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    )
  },
  set: (val) => {
    getComputedSet(
      'winDataList',
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    )
  }
})

// 支持拖拽的容器
const dragContainer = ref(null);

//  每个组件的位置大小
const getItemStyle = (uuid, item) => ({
    width: `${item.width}px`,
    height: `${item.height}px`,
    left: `${item.left}px`,
    top: `${item.top}px`,
    zIndex: curWinData?.value.uuid === uuid ? 2 : 1,
})

// 可以缩放的点
const getPointStyle = (point) => {
  if(isEmpty(curWinData.value)) return 
  const { x, y } = calculatePointPosition(point, curWinData.value.style);
  return {
    marginLeft: "-4px",
    marginTop: "-4px",
    left: `${x}px`,
    top: `${y}px`,
    cursor: CURSOR_MAP[point],
  };
};

// 计算属性，根据 isMaximized 返回不同的按钮文本
const getMaximize = computed(() => {
  return (item) => {
    return item
  };
});

// 设置可拖拽点的位置
function calculatePointPosition(point, { width, height }) {
  const positions = {
    lt: [0, 0],          rt: [width, 0],
    lb: [0, height],     rb: [width, height],
    t: [width/2, 0],     b: [width/2, height],
    l: [0, height/2],    r: [width, height/2]
  };
  return { x: positions[point][0], y: positions[point][1] };
}

const {
    handleDragStart, 
    handleZoomStart,
    handleMaximize,
} = useDragZoomCentre(dragContainer)

const { onClickOther } = useEventCentre()

// 过滤操作内容点击
const handleCurDragStart = (style, event) => {
  const target = event.target;
  if (target.closest(".window-content")) {
    return;
  }
  handleDragStart(style, event);
};

// 双击选中切换要操作的组件
function selectComponent(item, event) {
  event.stopPropagation(); // 阻止事件冒泡
  event.preventDefault(); // 阻止默认事件
  if(isEmpty(item?.uuid)) return;
  if (item.uuid === curWinData.value.uuid) return;
  curWinData.value = item;
  onClickOther({
      element: props.element, 
      clickName: 'onSwitchWin', 
      params: { 
        curWinDataUuid: item,
        containerHV: {
          width: dragContainer.value.clientWidth,
          height: dragContainer.value.clientHeight,
        },
        funParam: props.propValue.funParam,
      }
  })
}

// 关闭窗口
const handleCloseBox = (uuid) => {
  const index = winDataList.value.findIndex(item => item.uuid === uuid);
  if (index === -1) return;
  if (winDataList.value.length === 1) {
    winDataList.value = [];
    curWinData.value = {};
    return;
  }
  winDataList.value.splice(index, 1);
  // curWinData.value = winDataList.value[winDataList.value.length - 1];
}

const init = ()=>{
   if(winDataList.value?.length === 1) {
      curWinData.value = winDataList.value[0]
   }
 }
init()
</script>

<style scoped lang="less">
@header-color: #e6e6e6;
@header-font-color: #000;
@content-color: #F5F5F5;
.drag-container {
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;
  overflow: hidden;
  .shape-point {
    position: absolute;
    background: #fff;
    border: 1px solid #59c7f9;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    z-index: 1;
  }
  .draggable-item {
    position: absolute;
    width: 150px;
    height: 150px;
    cursor: grab;
    touch-action: none;
    transition: transform 0.1s ease;
    border: 1px solid #B3B3B3;
    user-select: none;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    &:active {
      cursor: grabbing;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .header {
      white-space: nowrap;
      background: @header-color;
      color: @header-font-color;
      overflow: hidden;
      border-bottom: 1px solid #B3B3B3;
      height: 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      .title {
        padding-left: 5px;
        font-weight: 600;
      }
    }
    .window-controls {
      display: flex;
      align-items: center;
      cursor: pointer;
      .min-btn,.close-btn,.max-btn {
        width: 32px;
        height: 32px;
        display: flex;
        justify-content: center;
        align-items: center;
        &:hover{
          background: rgba(161, 160, 160, 0.2);
        }
      }
      .close-btn:hover {
        background: #e81123 !important;
      }
      
    }
    .window-content {
      cursor: auto;
      background-color: @content-color;
      overflow: hidden;
      padding: 5px;
      width: 100%;
      height: calc(100% - 32px);
    }
  }
  .minBox {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    right: 0;
    bottom: 10px;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    width: fit-content;
    height: 30px;
    background: #fff;
    cursor: pointer;
  }
}
.action-item{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: fit-content;
}
</style>
