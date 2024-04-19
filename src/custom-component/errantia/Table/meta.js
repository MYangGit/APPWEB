export default {
  component: 'ErTable',
  label: '表格',
  propValue: {
    showBorder: false,
    activeClickRow: false,
    showOperate: false,
    serialNumber: false,
    textAlign: 'left',
    columns: [
        {
          title: '姓名',
          key: 'name',
        },
        {
          title: '年龄',
          key: 'age',
        },
        {
          title: '性别',
          key: 'sex',
        },
    ],
    dataSource: [
      {
        name: '小杨',
        age: 18,
        sex: '男'
      },
      {
        name: '小芳',
        age: 18,
        sex: '女'
      }
    ],
  },
  hideCustomAttrKeys: ['showBorder', 'activeClickRow'],
  icon: 'table',
  type: 'errantia',
  style: {
    width: 300,
    height: 200,
    borderWidth: 0,
    borderColor: '#ffffff',
    borderStyle: 'solid',
  },
  actionBinds: {
    onClickRow: '',
    onClickDelete: ''
  }
}