export default {
  component: 'ErCollapse',
  label: '折叠面板',
  icon: 'VPanel',
  type: 'errantia',
  propValue: {
    accordion: true,
    arrowPosition: 'right',
    arrowNear: false,
    panelLists: [
        {
            name: '1',
            title: '面板1',
            height: 100,
        }
    ],
  },
  style: {
    width: 400,
    height: 300,
    backgroundColor: '#fff',
    display: 'block',
    borderWidth: 0,
    borderColor: '#ffffff',
    borderStyle: 'solid',
  },
  childs: [],
  position: 'top',
  actionBinds: {
    change: ''
  }
}