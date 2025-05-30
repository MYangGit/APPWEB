export default {
  component: "ErGantt",
  label: "甘特图",
  propValue: {
    columns: [
      {
        field: "title",
        title: "title",
        width: "auto",
        sort: true,
        tree: true,
        editor: "input",
      },
      {
        field: "start",
        title: "start",
        width: "auto",
        sort: true,
        editor: "date-input",
      },
      {
        field: "end",
        title: "end",
        width: "auto",
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
        format(date) {
          return `day ${date.dateIndex}`;
        },
        style: {
          fontSize: 20,
          fontWeight: "bold",
          color: "white",
          strokeColor: "black",
          textAlign: "right",
          textBaseline: "bottom",
          backgroundColor: "#EEF1F5",
          textStick: true,
          padding: [0, 30, 0, 20],
        },
      },
      {
        unit: "hour",
        step: 12,
        format(date) {
          return date.dateIndex.toString();
        },
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
  },
  icon: "chart-line",
  type: "errantia",
  style: {
    width: 800,
    height: 200,
    fixedWidth: "100%",
    fixedHeight: "100%",
    backgroundColor: "#ffffff",
    borderColor: "#dcdfe6",
    borderWidth: 1,
    borderStyle: "solid",
    borderRadius: 4,
  },
};
