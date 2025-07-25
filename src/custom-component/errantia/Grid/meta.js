import { pad } from "lodash";

export default {
  component: 'ErGrid',
  label: 'Grid容器',
  icon: 'grid',
  type: 'errantia',
  propValue: {
    autoFlowRow: true,
    cgap: 5,
    rgap: 5,
    cols: 2,
    rows: 2,
    gridItems: [
        {
            name: 'ErGrid1',
            visible: true,
            cSpan: 1,
            rSpan: 1,
        },
        {
            name: 'ErGrid2',
            visible: true,
            cSpan: 1,
            rSpan: 1,
        },
    ]
  },
  style: {
    width: '400',
    height: '400',
    fixedWidth: '100%',
    fixedHeight: '100%',
    backgroundColor: '#fff',
    borderWidth: 0,
    borderColor: '#ffffff',
    borderStyle: 'solid',
    padding: 0,
  },
  childs: [],
  items: [],
}