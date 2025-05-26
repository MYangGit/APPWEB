import { flattenArray, isEmpty } from "@/utils/utils";
import Plotly from "plotly.js-dist-min";

/**
 * @description 绘图处理中心
 * @author: MY
 * @data 2024-07-13 14:00:00
 */
export const hasHeightMap = new Map(); // 高亮选中的数据
const DotLIMIT = 15; // 两次点击的差值 n以内认为是同一个点
export const useAllDrawCenter = () => {
  // 处理点击打点事件
  const handleDotClick = ({ domRef, event, points, annotations = [], scaleType }) => {
    console.log("handleDotClick", event, points);
    const {
      curveNumber,
      pointNumber,
      data: { uuid, autoType, yaxis },
    } = points[0];
    if(uuid === "not-dot") return;
    if(!isFixedRange({})) return;
    if(event.detail > 1) return;
    if (isEmpty(points)) return;
    if (event.button === 2 || event.which === 3) {
      handleRightClick({ domRef, points });
      return;
    }
    const canRes = cancelDotClick({ domRef, points, annotations, autoType });
    if (!canRes) return;
    points?.forEach((point) => {
      let annotate_text = bulidTooltip(point);
      let x = point.x;
      let y = point.y;
      if(scaleType === "log") {
        x = Math.log10(x);
      }
      let annotation = {
        x,
        y,
        text: annotate_text,
        font: {
          size: 16,
          color: "#000000",
        },
        bordercolor: "#A5A5A7",
        align: "left",
        arrowhead: 6,
        arrowcolor: "#000000",
        ax: 0,
        ay: 0,
        arrowwidth: 2,
        xanchor: "left",
        yanchor: "bottom",
        borderRaduis: 4,
        borderwidth: 2,
        bgcolor: "#FAFAFF",
        uuidDot: {
          curveNumber,
          pointNumber,
          uuid,
        },
      };
      if(!isEmpty(yaxis)) {
        annotation.yref  = yaxis;
      }
      annotations.push(annotation);
      Plotly.relayout(domRef, { annotations: annotations });
    });
  };

  // 取消打点
  const cancelDotClick = ({
    domRef,
    points = [],
    annotations,
    type = "clearOne",
    uuidStr = "",
    autoType = ""
  }) => {
    if (isEmpty(annotations)) return true;
    // 清除所有打点
    if (type === "clearAll") {
      Plotly.relayout(domRef, { annotations: [] });
      return;
    }
    // 清除选中的线的点
    if (type === "clearSelectLine") {
      const uuidList = [...hasHeightMap.keys()];
      annotations = annotations.filter((item) => {
        return !uuidList.includes(item.uuidDot.uuid);
      });
      Plotly.relayout(domRef, { annotations: annotations });
      return;
    }
    // 清除uuidStr的点
    if (type === "uuidStr") {
      if (isEmpty(uuidStr)) return;
      annotations = annotations.filter((item) => {
        return item.uuidDot.uuid !== uuidStr;
      });
      Plotly.relayout(domRef, { annotations: annotations });
      return;
    }
    // 重复点击相同的点取消打点
    const index = annotations.findIndex((item) => {
      if(autoType === "splashes") return calcDotClick(item, points, 0); 
      return calcDotClick(item, points, DotLIMIT);
    });
    if (index > -1) {
      annotations.splice(index, 1);
      Plotly.relayout(domRef, { annotations: annotations });
      return;
    }
    return true;
  };

  // 判断是否有打点
  const isHasDot = ({ type = "all", annotations }) => {
    const allHas = annotations?.length > 0;
    if (type === "selectLine" && allHas && hasHeightMap.size > 0) {
      const uuidList = [...hasHeightMap.keys()];
      return annotations.some((item) => {
        return uuidList.includes(item.uuidDot.uuid);
      });
    }
    return allHas;
  };

  // 计算两次点击的差值，如何小于5，认为同一个点
  const calcDotClick = (oldDot, newDot, limit = 5) => {
    const {
      curveNumber,
      pointNumber,
      data: { uuid },
    } = newDot[0];
    return (
      oldDot.uuidDot.curveNumber === curveNumber &&
      oldDot.uuidDot.uuid === uuid &&
      Math.abs(oldDot.uuidDot.pointNumber - pointNumber) <= limit
    );
  };

  // 组织注解内容
  const bulidTooltip = (point) => {
    return ` ${point.xaxis.title.text} ${point.x.toPrecision(6)}<br> ${
      point.yaxis.title.text
    } ${point.y.toPrecision(6)}`;
  };

  // 处理右键事件
  const handleRightClick = ({ domRef, points }) => {
    const uuid = points[0].data.uuid;
    if (isHighlight(uuid)) {
      setLineHighlight({ domRef, type: "Unhighlight", points });
    } else {
      setLineHighlight({ domRef, type: "Highlight", points });
    }
  };

  // 高亮选中设置
  const setLineHighlight = ({ domRef, points, type, dataList }) => {
    let curveNumber = [points[0].curveNumber];
    const uuid = points[0].data.uuid;
    const { autoType } = points[0].data;
    const updateHighlight = {};
    if(autoType === "splashes") {
      const indices = dataList.reduce((acc, item, index) => {
        if (item.uuid === uuid) {
          acc.push(index);
          if(!isEmpty(item?.marker?.line?.width) && !Reflect.has(updateHighlight, "marker.line.width")) {
            Reflect.set(updateHighlight, "marker.line.width", item.marker.line.width + (type === "Highlight" ? 2 : -2))
          }
          if(!isEmpty(item?.line?.width) && !Reflect.has(updateHighlight, "line.width")) {
            Reflect.set(updateHighlight, "line.width", item.marker.size + (type === "Highlight" ? 2 : -2))
          }
        }
        return acc;
      }, []);
      Reflect.set(updateHighlight, "marker.size", points[0].data.marker.size + (type === "Highlight" ? 2 : -2))
      curveNumber = indices;
    }else{
      Reflect.set(updateHighlight, "line.width", points[0].data.line.width + (type === "Highlight" ? 2 : -2))
    }
    if (type === "Unhighlight") {
      clearHighlight({ uuid });
    }
    if (type === "Highlight") {
      hasHeightMap.set(uuid, { type, data: points[0].data, curveNumber });
    }
    Plotly.restyle(domRef, updateHighlight, [...curveNumber]);
    if(autoType === "splashes" && type === "Highlight") {
      setLineColor({ domRef, lineColor: points[0].data.marker.color, uuid });
    }
  };

  // 判断是否高亮的数据
  const isHighlight = (uuid = "") => {
    if (isEmpty(uuid)) return hasHeightMap.size > 0;
    return (
      hasHeightMap.has(uuid) && hasHeightMap.get(uuid).type === "Highlight"
    );
  };

  // 去除高亮
  const clearAllHighlight = ({currDomRef, uuid = "", clearhighlight = false, dataList }) => {
    if(!clearhighlight) return;
    if (!isEmpty(uuid)) {
      const uuidItem = hasHeightMap.get(uuid);
      if(isEmpty(uuidItem)) return;
      let { curveNumber, data } = uuidItem;
      const { autoType } = data;
      const updateHighlight = {};
      if(autoType === "splashes") {
        const indices = dataList.reduce((acc, item, index) => {
          if (item.uuid === uuid) {
            acc.push(index);
            if(!isEmpty(item?.marker?.line?.width) && !Reflect.has(updateHighlight, "marker.line.width")) {
              Reflect.set(updateHighlight, "marker.line.width", item.marker.line.width - 2)
            }
            if(!isEmpty(item?.line?.width) && !Reflect.has(updateHighlight, "line.width")) {
              Reflect.set(updateHighlight, "line.width", item.marker.size - 2)
            }
          }
          return acc;
        }, []);
        Reflect.set(updateHighlight, "marker.size", data.marker.size - 2)
        curveNumber = indices;
      }else{
        Reflect.set(updateHighlight, "line.width", data.line.width - 2)
      } 
      Plotly.restyle(currDomRef, updateHighlight, [...curveNumber]);
    } else {
      const selectList = [...hasHeightMap.values()]
      selectList?.forEach((item) => {
        let { curveNumber, data } = item;
        const { autoType, uuid:uuids } = data;
        const updateHighlight = {};
        if(autoType === "splashes") {
          const indices = dataList.reduce((acc, item, index) => {
            if (item.uuid === uuids) {
              acc.push(index);
              if(!isEmpty(item?.marker?.line?.width) && !Reflect.has(updateHighlight, "marker.line.width")) {
                Reflect.set(updateHighlight, "marker.line.width", item.marker.line.width - 2)
              }
              if(!isEmpty(item?.line?.width) && !Reflect.has(updateHighlight, "line.width")) {
                Reflect.set(updateHighlight, "line.width", item.marker.size - 2)
              }
            }
            return acc;
          }, []);
          Reflect.set(updateHighlight, "marker.size", data.marker.size - 2)
          curveNumber = indices;
        }else{
          Reflect.set(updateHighlight, "line.width", data.line.width - 2)
        } 
        Plotly.restyle(currDomRef, updateHighlight, [...curveNumber]);
      });
    }
  };

  // 清除高亮数据
  const clearHighlight = ({ uuid = "", clearhighlight = false }) => {
    if (!isEmpty(uuid)) {
      clearAllHighlight({ uuid, clearhighlight });
      hasHeightMap.delete(uuid);
    } else {
      clearAllHighlight({ clearhighlight });
      hasHeightMap.clear();
    }
  };

  // 设置线宽
  const setLineWidth = ({
    domRef,
    lineWidth,
    name = "",
  }) => {
    if (isEmpty(lineWidth) && isEmpty(domRef)) return;
    const curveNumberList = [...hasHeightMap.values()].map(
      (item) => item.curveNumber
    );
    const updateLineWidth = {
      "line.width": lineWidth,
      "marker.size": lineWidth,
      "marker.line.width": lineWidth ,
    };
    if(name === "lingji") {
      Reflect.deleteProperty(updateLineWidth, "line.width");
      Reflect.deleteProperty(updateLineWidth, "marker.line.width");
    }
    if(["chongji", "jieyue"].includes(name)) {
      Reflect.deleteProperty(updateLineWidth, "line.width");
    }
    clearHighlight({});
    Plotly.restyle(domRef, updateLineWidth, flattenArray(curveNumberList, 1));
  };

  // 设置线形
  const setLineStyle = ({
    domRef,
    lineStyle,
  }) => {
    if (isEmpty(lineStyle) && isEmpty(domRef)) return;
    const curveNumberList = [...hasHeightMap.values()].map(
      (item) => item.curveNumber
    );
    const updateLineStyle = {
      "line.dash": lineStyle,
    };
    Plotly.restyle(domRef, updateLineStyle, flattenArray(curveNumberList, 1));
  };

  // 设置点形
  const setDotStyle = ({
    domRef,
    dotStyle,
  }) => {
    if (isEmpty(dotStyle) && isEmpty(domRef)) return;
    const curveNumberList = [...hasHeightMap.values()].map(
      (item) => item.curveNumber
    );
    const updateLineStyle = {
      "marker.symbol": dotStyle,
    };
    Plotly.restyle(domRef, updateLineStyle, flattenArray(curveNumberList, 1));
  };


  // 设置线的颜色
  const setLineColor = ({
    domRef,
    lineColor,
    uuid,
    name = "",
  }) => {
    if (isEmpty(lineColor) && isEmpty(domRef)) return;
    const curveNumberList = [...hasHeightMap.values()].map(
      (item) => {
        if (isEmpty(uuid)) {
          return item.curveNumber;
        }
        if (item.data.uuid === uuid) {
          return item.curveNumber;
        }
      }
    );
    const updateLineColor = {
      "line.color": lineColor,
      "marker.color": lineColor,
      "marker.line.color": lineColor,
    };
    if(name === "lingji") {
      Reflect.deleteProperty(updateLineColor, "line.color");
      Reflect.deleteProperty(updateLineColor, "marker.line.color");
    }
    if(["chongji", "jieyue"].includes(name)) {
      Reflect.deleteProperty(updateLineColor, "line.color");
    }
    Plotly.restyle(domRef, updateLineColor, flattenArray(curveNumberList, 1));
  };

  // 删除线
  const deleteLine = ({
    domRef,
    type = "allSelect",
  }) => {
    if (isEmpty(domRef)) return;
    if (type === "currLine") {
      const uuid = [...hasHeightMap.keys()].pop();
      if (isEmpty(uuid)) return;
      const { curveNumber } = hasHeightMap.get(uuid);
      Plotly.deleteTraces(domRef, curveNumber);
      clearHighlight({ uuid });
      cancelDotClick({ domRef, type: "uuidStr", uuidStr: uuid });
      return;
    }
    const curveNumberList = [...hasHeightMap.values()].map(
      (item) => item.curveNumber
    );
    Plotly.deleteTraces(domRef, flattenArray(curveNumberList, 1));
    clearHighlight({});
    cancelDotClick({ domRef, type: "clearAll" });
  };

  // 复制绘制好的图表
  const copyChart = ({ domRef }) => {
    if (isEmpty(domRef)) return;
    // 生成图表图像数据
    Plotly.toImage(domRef, { format: "svg", height: 800, width: 1200 })
      .then((chartData) => {
        // 创建一个新的图像
        const img = new Image();
        img.src = chartData;
        return new Promise((resolve) => {
          img.onload = resolve;
        }).then(() => {
          const canvas = document.createElement("canvas");
          canvas.width = img.width;
          canvas.height = img.height;
          const ctx = canvas.getContext("2d");
          ctx?.drawImage(img, 0, 0);
          canvas.toBlob((blob) => {
            if (blob) {
              const item = new ClipboardItem({ "image/png": blob });
              navigator.clipboard
                .write([item])
                .then((res) => {
                  console.log("复制成功", res);
                })
                .catch((err) => {
                  console.error("复制失败", err);
                });
            }
          }, "image/png");
        });
      })
      .catch((e) => {
        console.error("图表转换为图片失败", e);
      });
  };

  // 转换为后端要的Blob
  const uploadPlotlyToBlob = async ({ domRef, fileName = 'chart.svg', format = "svg" }) => {
    try {
      const svgData = await Plotly.toImage(domRef, { format: format, height: 800, width: 1200 });
      const svgBlob = await fetch(svgData).then(res => res.blob());
      // 2. 转换为 File 并添加文件名
      const svgFile = new File([svgBlob], fileName, {
        type: {"png":'image/png', "svg":'image/svg+xml'}[format], // 明确 MIME 类型
        lastModified: Date.now()
      });
      return svgFile
    } catch (error) {
      console.error("图表转换为Blob失败", error);
      return null;
    }
  };


  // 设置网格线
  const setGridLine = ({ domRef, showgrid = false, dataLayout }) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {
      xaxis: { ...dataLayout.xaxis, showgrid },
      yaxis: { ...dataLayout.yaxis, showgrid }
    }
    Plotly.relayout(domRef, updateLayout);
  };

  // 判断是否显示网格线
  const isShowGrid = ({ showgrid }) => {
    return (typeof showgrid !== 'boolean') ? !isEmpty(showgrid) : showgrid;
  };

  // 设置图例
  const setLegend = ({ domRef, showlegend = false }) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {
      showlegend,
    };
    Plotly.relayout(domRef, updateLayout);
  };

  // 判断是否显示图例
  const isShowLegend = ({ showlegend }) => {
    return (typeof showlegend !== 'boolean') ? !isEmpty(showlegend) : showlegend;
  };

  // 自动缩放
  const setAutoScale = ({ domRef, dataLayout }) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {
      xaxis: { ...dataLayout.xaxis, autorange: true },
      yaxis: { ...dataLayout.yaxis, autorange: true }
    }
    if(!isEmpty(dataLayout.yaxis2)) {
      updateLayout.yaxis2 = { ...dataLayout.yaxis2, autorange: true }
    }
    Plotly.relayout(domRef, updateLayout);
  };

  // 打开平移
  const setPan = ({ domRef, pan = false}) => {
    if (isEmpty(domRef)) return;
    Plotly.relayout(domRef, { dragmode: pan });
  };

  // 打开缩放
  const setZoom = ({ domRef, zoom = false }) => {
    if (isEmpty(domRef)) return;
    Plotly.relayout(domRef, { dragmode: zoom });
  };

  const isPanOrZoom = ({ panOrZoom }) => {
     let dragmode = false;
      if (panOrZoom === "Pan") {
        dragmode = "pan";
      } else if (panOrZoom === "Zoom_In") {
        dragmode = "zoom";
      }
      return dragmode;
  };

  // 固定显示的区间
  const setFixedRange = ({ domRef, fixedrange = false, dataLayout }) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {
      xaxis: { ...dataLayout.xaxis, fixedrange },
      yaxis: { ...dataLayout.yaxis, fixedrange }
    }
    if(!isEmpty(dataLayout.yaxis2)) {
      updateLayout.yaxis2 = { ...dataLayout.yaxis2, fixedrange }
    }
    Plotly.relayout(domRef, updateLayout);
  };

  const isFixedRange = ({ fixedrange }) => {
    return (typeof fixedrange !== 'boolean') ? isEmpty(fixedrange) : fixedrange;
  };

  // 设置对数显示x轴
  const setLogXY = ({ domRef , logXY = false, dataLayout}) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {
      xaxis: { ...dataLayout.xaxis, type: logXY ? "log" : "linear" },
    }
    Plotly.relayout(domRef, updateLayout);
  };

  // 更新x轴y轴的title
  const setXYTitle = ({ domRef , dataLayout, xtitle = {}, ytitle = {}, ytitle2 = {} }) => {
    if (isEmpty(domRef)) return;
    const updateLayout = {}
    if(!isEmpty(xtitle)) {
      updateLayout.xaxis = { 
        ...dataLayout.xaxis, 
        title: {...dataLayout.xaxis.title, ...xtitle} 
      }
    }
    if(!isEmpty(ytitle)) {
      updateLayout.yaxis = { 
        ...dataLayout.yaxis, 
        title: {...dataLayout.yaxis.title, ...ytitle}
      }
    }
    if(!isEmpty(ytitle2) && !isEmpty(dataLayout.yaxis2)) {
      updateLayout.yaxis2 = { 
        ...dataLayout.yaxis2, 
        title: {...dataLayout.yaxis2.title, ...ytitle2}
      }
    }
    if(isEmpty(updateLayout)) return;
    Plotly.relayout(domRef, updateLayout);
  };

  return {
    isPanOrZoom,
    setFixedRange,
    isShowGrid,
    isFixedRange,
    copyChart,
    deleteLine,
    setLineColor,
    setDotStyle,
    setLineWidth,
    setLineStyle,
    isHasDot,
    isShowLegend,
    clearHighlight,
    handleDotClick,
    isHighlight,
    cancelDotClick,
    setGridLine,
    setLegend,
    setAutoScale,
    setPan,
    setZoom,
    setLogXY,
    setXYTitle,
    uploadPlotlyToBlob
  };
};
