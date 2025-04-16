export default {
  component: 'ErTree',
  label: '树形控件',
  propValue: {
    options: [
        {
            id: 1,
            label: '一级 1',
            children: [
                {
                    id: 4,
                    label: '二级 1-1',
                    children: [
                        {
                            id: 9,
                            label: '三级 1-1-1'
                        },
                        {
                            id: 10,
                            label: '三级 1-1-2'
                        }
                    ]
                }
            ],
        },
        {
            id: 2,
            label: '一级 2',
            children: [
                {
                    id: 5,
                    label: '二级 2-1'
                },
                {
                    id: 6,
                    label: '二级 2-2'
                }
            ],
        }, 
    ],
    disabled: false,
    activateText: "",
    value:[],
    nodeKey: "id"
  },
  icon: 'select',
  type: 'errantia',
  style: {
    width: 200,
    height: 34,
    fontSize: '',
    fontWeight: 400,
    lineHeight: '',
    letterSpacing: 0,
    fixedWidth: '',
    fixedHeight: '',
    textAlign: '',
    color: '',
    backgroundColor: '',
  },
  actionBinds: {
    click: ''
  }
}