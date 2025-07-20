export default {
  component: "ErG6",
  label: "G6绘图",
  propValue: {
    funParam: '',
    nodes: [
      {
        id: "node1",
        style: {
          x: 50,
          y: 100,
        },
        data: {
          label: "圆形",
          category: "shape",
          subtitle: '你的第一个自定义节点1', // 副标题
        },
      },
      {
        id: "node2",
        style: {
          x: 200,
          y: 100,
        },
        data: {
          label: "椭圆",
          category: "shape",
          subtitle: '第二个自定义节点1', // 副标题
        },
      },
    ],
    edges: [
      {
        id: "edge-1",
        source: "node1",
        target: "node2",
      },
    ],
  },
  icon: "chart-line",
  type: "errantia",
  style: {
    width: 866,
    height: 600,
    fixedWidth: "100%",
    fixedHeight: "100%",
    backgroundColor: "#ffffff",
    borderColor: "#dcdfe6",
    borderWidth: 1,
    borderStyle: "solid",
    borderRadius: 4,
  },
  actionBinds: {
      onMounted: '',
      handlePluginClick: '',
      handleNodeClick: '',
  },
};
