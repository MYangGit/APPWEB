<template>
  <div>
    <div
      ref="ganttContainer"
      style="position: absolute; width: 100%; height: 100%"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from "vue";
import { Gantt } from "@visactor/vtable-gantt";
import { isEmpty, getComputedGet, getComputedSet } from "@/utils/utils";
import { rootStore } from "@/stores/rootStore";

const props = defineProps({
  propValue: {
    type: Object,
    default: () => ({
      columns: [
        {
          field: "title",
          title: "title",
          width: "100",
          sort: true,
          tree: true,
          editor: "input",
        },
        {
          field: "start",
          title: "start",
          width: "200",
          sort: true,
          editor: "date-input",
        },
        {
          field: "end",
          title: "end",
          width: "200",
          sort: true,
          editor: "date-input",
        },
      ],
      records: [
        {
          id: 1,
          title: "Task 1",
          developer: "liufangfang.jane@bytedance.com",
          start: "2024-07-24",
          end: "2024-07-26",
          progress: 31,
          priority: "P0",
        },
        {
          id: 2,
          title: "Task 2",
          developer: "liufangfang.jane@bytedance.com",
          start: "07/24/2024",
          end: "08/04/2024",
          progress: 60,
          priority: "P0",
        },
        {
          id: 3,
          title: "Task 3",
          developer: "liufangfang.jane@bytedance.com",
          start: "2024-08-04",
          end: "2024-08-04",
          progress: 100,
          priority: "P1",
        },
      ],
      dateHeader: [
        {
          unit: "day",
          step: 1,
          startOfWeek: 1,
          style: {
            fontSize: 20,
            fontWeight: "bold",
            color: "white",
            strokeColor: "black",
            textAlign: "right",
            textBaseline: "bottom",
            backgroundColor: "#EEF1F5",
            textStick: true,
          },
        },
        {
          unit: "hour",
          step: 12,
          style: {
            fontSize: 20,
            fontWeight: "bold",
            color: "white",
            strokeColor: "black",
            textAlign: "right",
            textBaseline: "bottom",
            backgroundColor: "#EEF1F5",
          },
        },
      ],
    }),
  },
  element: {
    type: Object,
    default: () => ({}),
  },
});

// 渲染容器
const ganttContainer = ref(null);
const ganttInstance = ref(null);

// 任务表头
const columns = computed({
  get: () => {
    return getComputedGet(
      "columns",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    );
  },
  set: (val) => {
    getComputedSet(
      "columns",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    );
  },
});

// 甘特图数据
const records = computed({
  get: () => {
    return getComputedGet(
      "records",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    );
  },
  set: (val) => {
    getComputedSet(
      "records",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    );
  },
});

// 日期表头
const dateHeader = computed({
  get: () => {
    return getComputedGet(
      "dateHeader",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue
    );
  },
  set: (val) => {
    getComputedSet(
      "dateHeader",
      props.element.dataBinds,
      rootStore.dataConfig.stateSet,
      props.propValue,
      val
    );
  },
});

// 初始化甘特图的函数
const initGantt = () => {
  if (!ganttContainer.value) return;
  const option = {
    overscrollBehavior: "none",
    records: records.value,
    taskListTable: {
      columns: columns.value,
      theme: {
        headerStyle: {
          borderColor: "#e1e4e8",
          borderLineWidth: 1,
          fontSize: 18,
          fontWeight: "bold",
          color: "red",
          bgColor: "#EEF1F5",
        },
        bodyStyle: {
          borderColor: "#e1e4e8",
          borderLineWidth: [1, 0, 1, 0],
          fontSize: 16,
          color: "#4D4D4D",
          bgColor: "#FFF",
        },
      },
      //rightFrozenColCount: 1
    },
    frame: {
      outerFrameStyle: {
        borderLineWidth: 2,
        borderColor: "#e1e4e8",
        cornerRadius: 8,
      },
      verticalSplitLine: {
        lineColor: "#e1e4e8",
        lineWidth: 3,
      },
      horizontalSplitLine: {
        lineColor: "#e1e4e8",
        lineWidth: 3,
      },
      verticalSplitLineMoveable: true,
      verticalSplitLineHighlight: {
        lineColor: "green",
        lineWidth: 3,
      },
    },
    grid: {
      verticalLine: {
        lineWidth: 1,
        lineColor: "#e1e4e8",
      },
      horizontalLine: {
        lineWidth: 1,
        lineColor: "#e1e4e8",
      },
    },
    headerRowHeight: 40,
    rowHeight: 40,
    taskBar: {
      startDateField: "start",
      endDateField: "end",
      progressField: "progress",
      resizable: true,
      moveable: true,
      hoverBarStyle: {
        barOverlayColor: "rgba(99, 144, 0, 0.4)",
      },
      labelText: "{title}  complete {progress}%",
      labelTextStyle: {
        fontFamily: "Arial",
        fontSize: 16,
        textAlign: "left",
        textOverflow: "ellipsis",
      },
      barStyle: {
        width: 20,
        /** 任务条的颜色 */
        barColor: "#ee8800",
        /** 已完成部分任务条的颜色 */
        completedBarColor: "#91e8e0",
        /** 任务条的圆角 */
        cornerRadius: 8,
        /** 任务条的边框 */
        borderLineWidth: 1,
        /** 边框颜色 */
        borderColor: "black",
      },
    },
    timelineHeader: {
      colWidth: 100,
      backgroundColor: "#EEF1F5",
      horizontalLine: {
        lineWidth: 1,
        lineColor: "#e1e4e8",
      },
      verticalLine: {
        lineWidth: 1,
        lineColor: "#e1e4e8",
      },
      scales: [
        {
          ...dateHeader.value[0],
          format(date) {
            const endDate = new Date(date.endDate);
            const endDay = `${endDate.getMonth() + 1}/${endDate.getDate()}`;
            return endDay;
          },
        },
        {
          ...dateHeader.value[1],
          format(date) {
            return date.dateIndex.toString();
          },
        },
      ],
    },
    markLine: [],
    rowSeriesNumber: {
      title: "行号",
      dragOrder: true,
      headerStyle: {
        bgColor: "#EEF1F5",
        borderColor: "#e1e4e8",
      },
      style: {
        borderColor: "#e1e4e8",
      },
    },
    scrollStyle: {
      scrollRailColor: "RGBA(246,246,246,0.5)",
      visible: "scrolling",
      width: 6,
      scrollSliderCornerRadius: 2,
      scrollSliderColor: "#5cb85c",
    },
  };
  if (ganttInstance.value) {
    ganttInstance.value.updateOption(option);
    return;
  }
  nextTick(() => {
    ganttInstance.value = new Gantt(ganttContainer.value, option);
  });
};

onMounted(() => {
  initGantt();
});

watch(
  () => [records.value, columns.value, dateHeader.value],
  (newVal) => {
    if (isEmpty(newVal)) return;
    initGantt();
  },
  { deep: true }
);

</script>

<style lang="less" scoped></style>
