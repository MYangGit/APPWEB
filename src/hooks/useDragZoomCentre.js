import { ref, computed, onUnmounted } from 'vue';
import { rootStore } from '@/stores/rootStore';
import calculateComponentPositonAndSize from "@/utils/calculateComponentPositonAndSize";
import { deepCopy, isEmpty } from '@/utils/utils';

// 常量配置
const BOUNDARY_OFFSET = 30; // 边界可显示区域
const MIN_SIZE = 67; // 最小尺寸限制

export function useDragZoomCentre(dragContainer) {
  const isDragging = ref(false);
  const isResizing = ref(false);
  const editMode = computed(() => rootStore.editor.editMode);
  
  // 缓存容器尺寸信息 - 取消
  let containerRectCache = null;
  const getContainerRect = () => {
    containerRectCache = dragContainer.value.getBoundingClientRect();
    return containerRectCache;
  };

  // 统一事件处理
  const eventHandler = {
    preventDefault(e) {
      e.stopPropagation();
    },
    addEvents(eventMap) {
      Object.entries(eventMap).forEach(([event, handler]) => {
        document.addEventListener(event, handler, { passive: true });
      });
    },
    removeEvents(eventMap) {
      Object.entries(eventMap).forEach(([event, handler]) => {
        document.removeEventListener(event, handler);
      });
    }
  };

  // 边界限制计算
  const calcBoundedPosition = (value, min, max) => Math.max(min, Math.min(value, max));

  // 拖拽逻辑
  const handleDragStart = (style, startEvent) => {
    if (isEmpty(style)) return;
    if (editMode.value === "edit" || isResizing.value) return;
    eventHandler.preventDefault(startEvent);
    isDragging.value = true;
    
    const { clientX: startX, clientY: startY } = startEvent;
    const startTop = Number(style.top);
    const startLeft = Number(style.left);
    const itemRect = startEvent.target.getBoundingClientRect();
    const containerRect = getContainerRect();
    
    const maxTop = containerRect.height - BOUNDARY_OFFSET;
    const maxLeft = containerRect.width - BOUNDARY_OFFSET;
    const minTop = -(itemRect.height - BOUNDARY_OFFSET);
    const minLeft = -(itemRect.width - BOUNDARY_OFFSET);
    let isFirst = true;
    const handleMove = (moveEvent) => {
      if(isFirst){
        isFirst = false
        return
      }
      eventHandler.preventDefault(moveEvent);
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;
      // 优化频繁操作时的性能
      style.pointerEvents = Date.now() - startEvent.timeStamp > 200 
        ? "none" 
        : "all";
      style.top = calcBoundedPosition(startTop + deltaY, minTop, maxTop);
      style.left = calcBoundedPosition(startLeft + deltaX, minLeft, maxLeft);
    };

    const handleEnd = () => {
      isDragging.value = false;
      style.pointerEvents = "all";
      eventHandler.removeEvents({
        mousemove: handleMove,
        mouseup: handleEnd
      });
    };

    eventHandler.addEvents({
      mousemove: handleMove,
      mouseup: handleEnd
    });
  };

  // 缩放逻辑
  const handleZoomStart = (point, style, startEvent) => {
    if (isEmpty(style)) return;
    if (editMode.value === 'edit' || isDragging.value) return;
    
    eventHandler.preventDefault(startEvent);
    isResizing.value = true;
    
    const containerRect = getContainerRect();
    const pointRect = startEvent.target.getBoundingClientRect();
    const center = {
      x: style.left + style.width / 2,
      y: style.top + style.height / 2
    };
    
    const curPoint = {
      x: pointRect.left - containerRect.left + pointRect.width / 2,
      y: pointRect.top - containerRect.top + pointRect.height / 2
    };
    
    const symmetricPoint = {
      x: center.x * 2 - curPoint.x,
      y: center.y * 2 - curPoint.y
    };
    let isFirst = true
    const handleMove = (moveEvent) => {
      if(isFirst){
        isFirst = false
        return
      }
      eventHandler.preventDefault(moveEvent);
      const curPosition = {
        x: moveEvent.clientX - containerRect.left,
        y: moveEvent.clientY - containerRect.top
      };
      
      calculateComponentPositonAndSize(
        point,
        style,
        curPosition,
        style.width / style.height,
        false,
        { center, curPoint, symmetricPoint }
      );
      
      // 添加最小尺寸限制
      style.width = Math.max(style.width, MIN_SIZE);
      style.height = Math.max(style.height, MIN_SIZE);
    };

    const handleEnd = () => {
      isResizing.value = false;
      eventHandler.removeEvents({
        mousemove: handleMove,
        mouseup: handleEnd
      });
    };

    eventHandler.addEvents({
      mousemove: handleMove,
      mouseup: handleEnd
    });
  };

  // 最大化
  const handleMaximize = (item)=> {
    console.log("handleMaximize", item)
    // 已经最大了 再点击还原
    if(item.isMaximized){
      item.style = deepCopy(item.lastStyle)
      item.isMaximized = !item.isMaximized
      return
    }
    item.lastStyle = deepCopy(item.style)
    const containerRect = getContainerRect();
    item.style = { 
      ...item.style, 
      left: 0, 
      top: 0,
      height: containerRect.height,
      width: containerRect.width
    }
    item.isMaximized = !item.isMaximized
  }

  // 组件卸载时清理
  onUnmounted(() => {
    eventHandler.removeEvents({
      mousemove: null,
      mouseup: null
    });
  });

  return { 
    handleDragStart,
    handleZoomStart,
    handleMaximize,
  };
}