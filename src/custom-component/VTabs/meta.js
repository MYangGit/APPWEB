export default {
  component: 'VTabs',
  label: '标签页',
  icon: 'tabs',
  type: 'box',
  propValue: {
    visibleName: 'visibleName',
    autoActiveName: "autoActiveName"
  },
  style: {
    width: 400,
    height: 200,
    fixedWidth: '100%',
    fixedHeight: '100%',
    display: 'block',
  },
  childs: [],
  tabs: [
    {
      name: 'tmp1',
      label: 'Tab1',
    }
  ],
  position: 'top'
}