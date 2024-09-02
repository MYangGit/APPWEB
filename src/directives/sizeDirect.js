/**
 * @description 自定义监听dom尺寸变化指令
 * @author MY
 * @data 2024-08-06 14:00:00
 * @param {HTMLElement} el 需要监听的dom元素
 * @param {Function} binding 传入的回调函数
 * @returns {width height} 变动后的宽高
*/
const map = new WeakMap();
const ob = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const handler = map.get(entry.target);
    if (handler) {
      const borderBoxSize = entry.borderBoxSize[0];
      const { inlineSize, blockSize } = borderBoxSize;
      const computedStyle = window.getComputedStyle(entry.target);
      const writingMode = computedStyle.writingMode;
      let width = 0, height = 0;
      if (writingMode === 'vertical-rl' || writingMode === 'vertical-lr') {
        width = blockSize;
        height = inlineSize;
      } else {
        width = inlineSize;
        height = blockSize;
      }
      handler({ width, height });
    }
  }
});

export default {
  mounted(el, binding) {
    map.set(el, binding.value);
    ob.observe(el);
  },
  unmounted(el) {
    ob.unobserve(el);
  },
}