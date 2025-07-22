<template>
  <div>
    <div
      ref="g6Container"
      style="position: absolute; width: 100%; height: 100%"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, toRaw, onBeforeUnmount, computed , watch} from "vue";
import { isEmpty, deepCopy, getComputedGet, getComputedSet } from "@/utils/utils";
import { rootStore } from "@/stores/rootStore";
import { Graph , NodeEvent, GraphEvent, register, ExtensionCategory} from "@antv/g6";
import { useEventCentre } from '@/hooks/useEventCentre';
import { breathNode, FlyMarkerCubic } from "./custom/index.js";



const { onClickOther } = useEventCentre();

const props = defineProps({
  propValue: {
    type: Object,
    default: () => ({
      funParam: "",
      nodes: [
        {
          id: "node-0",
          style: {
            x: 50,
            y: 100,
          },
          data: {
            label: "圆形",
            category: "shape",
            subtitle: '你的第一个自定义节点1', // 副标题
            class: "地铁二号线", // 自定义类名
            name: "地铁二号线 0", // 自定义属性
          },
        },
        {
          id: "node-1",
          style: {
            x: 200,
            y: 100,
          },
          data: {
            label: "椭圆",
            category: "shape",
            subtitle: '第二个自定义节点', // 副标题
          },
        },
      ],
      edges: [
        {
          id: "edge-1",
          source: "node-0",
          target: "node-1",
        },
      ],
    }),
  },
  element: {
    type: Object,
    default: () => ({}),
  },
});
// 节点数据
const nodes = computed({
  get: () => {
    return getComputedGet(
      "nodes",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    );
  },
  set: (val) => {
    getComputedSet(
      "nodes",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    );
  },
});

// 边数据
const edges = computed({
  get: () => {
    return getComputedGet(
      "edges",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    );
  },
  set: (val) => {
    getComputedSet(
      "edges",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    );
  },
});
// 注册自定义节点类型
// 渲染容器
const g6Container = ref(null);
// 图形实例
let graph = null;

// 初始化甘特图的函数
const initG6 = () => {
  if (!g6Container.value) return;
  // 销毁之前的图形实例
  if (graph) {
    graph.off(); // 移除所有事件监听
    graph.destroy(); // 销毁图形实例
    graph = null; // 清空引用
  }
  register(ExtensionCategory.NODE, 'dual-label-node', breathNode);
  register(ExtensionCategory.EDGE, 'fly-marker-cubic', FlyMarkerCubic);
  // 创建图形实例
  graph = new Graph({
    container: g6Container.value,
    autoResize: true, // 自动调整大小
    fitView: true, // 自动适应视图
    behaviors: ["drag-canvas", "zoom-canvas", "click-select"],
    data: {
      nodes: toRaw(nodes.value),
      edges: toRaw(edges.value),
    },
    node: {
      // 各状态下的样式
      type: "dual-label-node", // 使用自定义节点类型
      style: {
        halo: true,
        size: 50,
        // 设置节点的标签样式
        labelFill: "#fff",
        labelFontSize: 14,
        labelFontWeight: 600,
        iconUrl: () => 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix', // 这会变成 attributes.iconUrl
        labelText: (d) => d.data.label, // 节点标签内容
        subtitle: (d) => d.data.subtitle, // 副标题
      },
      palette: ['#3875f6', '#efb041', '#ec5b56', '#72c240', '#5c6bc0', '#ab47bc', '#ff7043', '#8d6e63', '#78909c', '#26a69a'],
      // state: {
      //   selected: {
      //     fill: "red",
      //     stroke: "transparent",
      //     lineWidth: 2,
      //     shadowColor: "transparent",
      //     shadowBlur: 10,
      //   },
      //   highlight: {
      //     fill: "yellow",
      //     stroke: "yellow",
      //     lineWidth: 2,
      //   },
      //   disable: {
      //     fill: "#ECECEC",
      //     stroke: "#BFBFBF",
      //     opacity: 0.5,
      //   },
      // },
    },
    edge: {
      type: "fly-marker-cubic", // 使用自定义边类型
      style: {
        lineDash: [10, 10],
      },
    },
    plugins: [
      {
        type: "tooltip",
        trigger: "click",
        enterable: true,
        getContent: (e, items) => {
          return handleNodePluginClick(e, items);
        },
      },
    ],
  });
  // 渲染图形
  graph.render();
  // 设置节点的交互事件
  // graph.on(NodeEvent.CLICK, handleNodeClick);
  // 设置画布的交互事件
  // graph.on(GraphEvent.AFTER_DRAW, () => {
  //   onClickOther({
  //       element: props.element, 
  //       clickName: 'drawComplete', 
  //       params: { 
  //         graph: graph,
  //         funParam: props.propValue.funParam,
  //       }
  //   })
  // });
};

onMounted(() => {
  initG6();
});

// 监听数据变化
const handleNodePluginClick = (e, items) => {
  // 生成包含交互元素的HTML结构
  const content = `
    <div class="custom-tooltip">
      <h4 data-clickable="header">自定义操作面板</h4>
      <div class="action-list">
        ${items
          .map(
            (item, index) => `
          <div class="action-item" 
               data-node-id="${item.id}" 
               data-action-index="${index}">
            <span>${item.data.label}</span>
            <button class="info-btn" data-action="detail">查看详情</button>
            <button class="config-btn" data-action="config">配置</button>
          </div>
        `
          )
          .join("")}
      </div>
    </div>
  `;

  // 延迟绑定事件以保证DOM渲染完成
  setTimeout(() => {
    const container = document.querySelector(".custom-tooltip");
    if (container) {
      // 事件委托实现
      container.addEventListener("click", (event) => {
        const target = event.target.closest("[data-action]");
        if (!target) return;
        const nodeItem = items.find(
          (item) => item.id === target.closest(".action-item").dataset.nodeId
        );
        // 执行不同操作
        switch (target.dataset.action) {
          case "detail":
            handlePluginClick(nodeItem);
            break;
          case "config":
            handleConfigClick(nodeItem);
            break;
        }
      });
    }
  }, 0);

  return content;
};

const handlePluginClick = async (nodeData) => {
  onClickOther({
      element: props.element, 
      clickName: 'handlePluginClick', 
      params: { 
        nodeData: nodeData,
        funParam: props.propValue.funParam,
      }
  })
  // graph.updateNodeData([
  //   {
  //     id: nodeData.id,
  //     data: {
  //       ...nodeData.data,
  //       label: "这是一个详细信息示例",
  //     },
  //   },
  // ]);
  // await graph.draw();
};

// 监听画布点击事件
const handleNodeClick = (e) => {
   onClickOther({
      element: props.element, 
      clickName: 'handleNodeClick', 
      params: { 
        event: e,
        funParam: props.propValue.funParam,
      }
  })
};

// 监听节点数据变化
watch(nodes, (newNodes) => {
  // 深拷贝节点数据，避免Vue的响应式陷阱
  if (graph) {
    // graph.updateNodeData(deepCopy(newNodes));
    // graph.render();
    initG6(); // 重新初始化图形
  }
}, { deep: true });

// 监听边数据变化
watch(edges, (newEdges) => {
  if (graph) {
    // graph.updateEdgeData(deepCopy(newEdges));
    // graph.render();
    initG6(); // 重新初始化图形
  }
}, { deep: true });

// 监听数据变化
const destroyGraph = () => {
  if (graph) {
    // 关键！移除所有事件监听
    graph.off();
    graph.destroy();
    graph = null;
  }
};

onBeforeUnmount(() => {
  destroyGraph(); // 组件销毁时清理
});
</script>

<style lang="less">
/* 确保点击元素的可交互状态 */
.custom-tooltip {
  cursor: pointer;
  transition: opacity 0.3s;
}
.custom-tooltip:hover {
  opacity: 0.8;
}
/* 按钮样式增强 */
.info-btn {
  background: #1890ff;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
}
.config-btn {
  background: #52c41a;
  margin-left: 8px;
}
</style>
