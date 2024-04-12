import { h } from "vue";

export default {
  component: 'ErLayout',
  label: 'Layout容器',
  icon: 'VPanel',
  type: 'errantia',
  propValue: {
    showHeader: true,
    showLeftSidebar: true,
    showRightSidebar: true,
    showFooter: true,
    heightHeader: 100,
    widthLeftSidebar: 150,
    widthRightSidebar: 150,
    heightFooter: 30,
    headerColor: 'lightpink',
    leftSidebarColor: 'lightblue',
    mainColor: 'coral',
    rightSidebarColor: 'yellow',
    footerColor: 'wheat',
  },
  style: {
    width: "100%",
    height: "100%",
    backgroundColor: '#fff',
    display: 'block',
    borderWidth: 0,
    borderColor: '#ffffff',
    borderStyle: 'solid',
  },
  childs: [],
  position: 'top',
}