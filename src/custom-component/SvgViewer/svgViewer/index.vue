<template>
  <div
    id="svgViewer"
    :class="{ empty: isEmpty }"
    style="width: 100%; height: 100%"
  ></div>
</template>

<script>
import 'svg.js';
import 'svg.panzoom.js';
import { render } from '@/core/render.js';
import { urlToBase64 } from '@/core/utils';
export default {
  props: {
    value: {
      type: [String, Object], // String | Object,
      default: () => {}
    }
  },
  data() {
    return {
      isCLick: false,
      clickComponent: {},
      selectComponent: '',
      flag: 0,
      svgElement: null,
      isEmpty: false
    };
  },
  watch: {
    value(n, o) {
      this.init(n);
    }
  },
  mounted() {
    this.init(this.value);
  },
  methods: {
    async init(value) {
      try {
        // 清空
        const root = document.getElementById('svgViewer');
        root.innerHTML = '';
        this.svgElement = null;
        this.isEmpty = false;
        let res = value;
        // 判断结果是xml字符串还是json对象
        if (typeof value !== 'string') {
          res = new render(value).xml;
        }
        if (!res) {
          this.isEmpty = true;
          root.innerHTML = this.$t('common.noData');
          return;
        }
        const draw = SVG('svgViewer').attr({ height: '100%', width: '100%' });
        draw.panZoom({ zoomMin: 0.5, zoomMax: 20, zoomFactor: 0.3 });
        draw.svg(res);
        this.setImageContent();
        this.svgElement = draw;
        // 兼容处理JSON和SVG
        if (typeof value !== 'string') {
          this.autoFit(draw);
        } else {
          this.autoFitSvg(draw);
        }
        // 点击空白区域清空选择
        root.onclick = e => {
          if (e.target.nodeName == 'svg') {
            this.clearSelect();
          }
        };
        this.addEvent();
      } catch (err) {
        console.log(err, 'err');
      }
    },
    // 自适应大小
    autoFit(draw) {
      try {
        const len = draw.node.childNodes.length;
        const el = draw.node.childNodes[len - 1];
        if (!el) {
          return;
        }
        // 计算根节点的图形信息
        const root = document.getElementById('svgViewer');
        const bounds = root.getBoundingClientRect();
        // 计算插入图形的图形信息
        const svgBBounds = el.getBoundingClientRect();
        const sx = (bounds.width * 0.8) / svgBBounds.width;
        const sy = (bounds.height * 0.8) / svgBBounds.height;
        const scale = Math.min(sx, sy);
        const viewMode = localStorage.getItem('viewMode');
        draw.zoom(scale);
        const tx =
          (draw.node.clientWidth - svgBBounds.width) / 2 -
          (svgBBounds.x - bounds.x);
        const ty =
          (draw.node.clientHeight - svgBBounds.height) / 2 -
          (svgBBounds.y - bounds.y);
        el.style.transform =
          'translate(' +
          tx +
          'px' +
          ',' +
          (viewMode == 'mobile' ? 160 : ty) +
          'px' +
          ')';
      } catch (err) {
        console.log(err, 'err');
      }
    },
    // 自适应大小SVG
    autoFitSvg(draw) {
      try {
        let el;
        draw.node.childNodes.forEach(node => {
          if (node.nodeName == 'svg') {
            el = node;
          }
        });
        if (!el) {
          return;
        }
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.appendChild(el);
        draw.node.appendChild(g);
        // 计算根节点的图形信息
        const root = document.getElementById('svgViewer');
        const bounds = root.getBoundingClientRect();
        // 计算插入图形的图形信息
        const svgBBounds = el.getBoundingClientRect();
        const sx = (bounds.width * 0.8) / svgBBounds.width;
        const sy = (bounds.height * 0.8) / svgBBounds.height;
        const scale = Math.min(sx, sy);
        draw.zoom(scale);
        const tx =
          (draw.node.clientWidth - svgBBounds.width) / 2 -
          (svgBBounds.x - bounds.x);
        const ty =
          (draw.node.clientHeight - svgBBounds.height) / 2 -
          (svgBBounds.y - bounds.y);
        g.style.transform = 'translate(' + tx + 'px' + ',' + ty + 'px' + ')';
      } catch (err) {
        console.log(err, 'err');
      }
    },
    setImageContent() {
      const imageList = SVG.select('image').members;
      imageList.forEach(image => {
        const href = image.attr()['xlink:href'];
        if (href) {
          image.attr('xlink:href', urlToBase64(href));
        }
      });
    },
    // 添加点击事件
    addEvent() {
      const componentArr = SVG.select('.component').members;
      componentArr.forEach(component => {
        if (!component.group) {
          return;
        }
        const componentBBox = component.bbox();
        const group = component.group().attr({
          id: component.attr().id + '-frame',
          frame: 'true',
          display: 'block',
          fill: '#ffffff'
        });
        group
          .rect(componentBBox.width, componentBBox.height)
          .addClass('whiteBox')
          .move(componentBBox.x, componentBBox.y);
        group
          .rect(componentBBox.width, componentBBox.height)
          .addClass('hiddenBox')
          .move(componentBBox.x, componentBBox.y);
        const _this = this;
        component.click(function(evt) {
          _this.clickEvent(evt);
        });
        component.dblclick(function(evt) {
          _this.clickEvent(evt);
        });
      });
    },
    clickEvent(evt) {
      const currentTarget = evt.currentTarget;
      if (!this.flag) {
        setTimeout(() => {
          this.doClick(currentTarget);
        }, 300);
      }
      this.flag++;
    },
    doClick(currentTarget) {
      if (this.flag == 1) {
        this.singleClick(currentTarget);
      } else {
        this.doubleClick(currentTarget);
      }
      this.flag = 0;
    },
    // 单击
    singleClick(currentTarget) {
      console.log('单击');
      this.fillComponnet(currentTarget.id);
      this.$emit('click', currentTarget.id);
    },
    // 双击
    doubleClick(currentTarget) {
      console.log('双击');
      this.$emit('dbclick', currentTarget.id);
    },
    // 选中效果
    fillComponnet(id) {
      let component = SVG.get(id);
      if (component) {
        this.clickComponent = component;
        if (this.selectComponent != '') {
          if (SVG.get(this.selectComponent) == null) {
          } else {
            SVG.get(this.selectComponent)
              .children()[0]
              .attr({ class: 'whiteBox' });
          }
        }
        this.selectComponent = component.attr().id + '-frame';
        if (this.isCLick && component == this.clickComponent) {
          return;
        }
        if (this.clickComponent != undefined) {
          SVG.get(this.selectComponent)
            .children()[0]
            .attr({ class: 'redBox', 'fill-rule': 'evenodd' });
        }
      } else {
        if (this.clickComponent.node) {
          this.clearSelect();
          this.clickComponent = {};
        }
      }
    },
    // 清空选中
    clearSelect() {
      if (this.clickComponent && this.clickComponent.attr) {
        const selectComponent = this.clickComponent.attr().id + '-frame';
        if (SVG.get(selectComponent)) {
          SVG.get(selectComponent)
            .children()[0]
            .attr({ class: 'whiteBox' });
        }
      }
    },
    // 放大
    zoomIn() {
      if (!this.svgElement) return;
      let level = this.svgElement.zoom() + 1;
      if (level % 1 >= 19) return;
      this.svgElement.zoom(level);
    },
    // 缩小
    zoomOut() {
      if (!this.svgElement) return;
      let level;
      if (this.svgElement.zoom() > 1) {
        level = this.svgElement.zoom() - 1;
      } else {
        level = this.svgElement.zoom() - 0.1;
      }
      if (level <= 0.5) return;
      this.svgElement.zoom(level);
    },
    // 重置视图
    zoomRecovery() {
      if (!this.svgElement) return;
      this.svgElement.zoom(1, new SVG.Point(300, 300));
      this.svgElement.viewbox({ x: 0, y: 0, width: 500, height: 500 });
    }
  }
};
</script>

<style lang="less">
.empty {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
}

.redBox {
  fill: none;
  stroke-width: 5;
  stroke: red;
}

.whiteBox {
  fill: none;
  stroke-width: 0;
}

.hiddenBox {
  fill: #ffffff;
  stroke-width: 0;
  stroke: #fff;
  fill-opacity: 1;
  opacity: 0;
  stroke-opacity: 0;
}
</style>
