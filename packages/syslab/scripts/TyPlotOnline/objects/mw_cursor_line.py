from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.objects.mw_annotation import mw_annotate
# from TyPlotOnline.mw_actions import action_pan, action_zoom

from matplotlib.backend_tools import Cursors
from datetime import datetime
from datetime import timedelta
import numpy as np

def mw_cursor(ax):
    """
    显示或关闭游标

    Args:
        ax: 坐标轴对象

    Returns:
    Raises:
    """
    # 构造一个游标线对象
    cax = mw_get_cax(ax)
    lst_lines = []
    lst_ax = []
    lines = cax.get_all_lines()
    lst_ax.append(ax)
    lst_lines.append(lines)

    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
    if isinstance(cax, CAxesYyaxis):
        lst_ax.clear()
        lst_ax.append(cax.ax)
        lst_ax.append(cax.ax2)
        lines_2 = cax.cax2.get_all_lines()
        lst_lines.append(lines_2)

    not_change_lst = change_autoscalex(ax, auto = False)
    cursor_line = mw_cursor_line(lst_ax, lst_lines)
    # plt.pause(0.001)
    import time
    time.sleep(0.001)
    change_autoscalex(ax, not_change_lst = not_change_lst)

    return cursor_line

class mw_cursor_line(object):
    """
    游标线类，用于拖拽与曲线产生交点

    Attributes:
        ax：需要添加游标的坐标轴
    """
    def __init__(self, axs, lst_lines):
        # 画一条竖线，游标线
        self.axs = axs
        self.ax = axs[-1]
        left, right = self.ax.get_xlim()
        self.line = self.ax.axvline(x = (left + right)/2,
                                color='c',linewidth=1)
        self.line.set_animated(False)
        self.canvas = self.line.figure.canvas
        self.toolbar = self.canvas.manager.toolbar
        self.fig = self.ax.figure
        self.press = False
        self.pick = False
        self.points = []
        self.lst_lines = lst_lines
        self.lines = lst_lines[0]
        self.connect()
        self.linecolors=[]
        self.background = None
        # 该图形是否为闭合曲线
        self.closed_curve = self.have_closed_curve()

        for lines in lst_lines:
            for line in lines:
                self.linecolors.append(line.get_color())

        # 注释框
        self.bbox_args = dict(boxstyle="round,pad=0.3,rounding_size=0", fc="w", ec = "black", alpha = 0.5)
        self.annotation = mw_annotate(self.ax,'', xy=(0, 0),linecolors=self.linecolors,
             xycoords='axes fraction',
             xytext=(10, 10), textcoords='offset points',
             ha="left", va="bottom",
             bbox = self.bbox_args,
             visible = True,
             zorder = 10)
        self.annotation.set_animated(False)
        self.annotation.set_in_layout(False)

        if self.closed_curve:
            self.get_pixels_datas()
            self.init_annotation_have_closed_curve(left, right)
        else:
            self.init_annotation(left, right)

    # 判读曲线中是否有闭合曲线
    def have_closed_curve(self):
        for lines in self.lst_lines:
            for line in lines:
                data_x = line.get_xdata()
                data_x = self.convert_data(data_x)
                data_y = line.get_ydata()
                data_y = self.convert_data(data_y)
                if len(data_x) != len(data_y):
                    return False
                # positive_order = all([data_x[i] < data_x[i+1] for i in range(len(data_x)-1)])
                # reverse_order = all([data_x[i] > data_x[i+1] for i in range(len(data_x)-1)])
                positive_order = all([((data_x[i] < data_x[i+1]) or (data_x[i] == data_x[i+1] and data_y[i] == data_y[i+1])) for i in range(len(data_x)-1)])
                reverse_order = all([((data_x[i] > data_x[i+1]) or (data_x[i] == data_x[i+1] and data_y[i] == data_y[i+1])) for i in range(len(data_x)-1)])
                if not positive_order and not reverse_order:
                    return True

        return False

    def init_annotation(self, left, right):
        # 初始化annotation
        text = ''
        x = (left + right)/2

        index0, index, index1 = self._get_min_index(x)

        # 如果x没有穿过一条线，则在所有的线端点招一个最近的点
        if index0 == -1 and index == -1 and index1 == -1:
            index0, index, index1 = self._get_closest_Endpoint(x)

        xdata = self.lst_lines[index0][index].get_xdata()
        xdata_origin = self.convert_data(xdata)
        xdata = self.convert_data(xdata_origin)
        
        x_new = xdata_origin[index1]

        self.annotation.init_linecolors()
        text += self.parse_text(x_new,'x')

        for i in range(0, len(self.lst_lines)):
            lines = self.lst_lines[i]
            points = []
            for j in range(0, len(lines)):
                xdata_new = lines[j].get_xdata()
                xdata_new = self.convert_data(xdata_new)
                ydata_new = lines[j].get_ydata()
                ydata_new = self.convert_data(ydata_new)

                positive_order = True
                # 判断是正序还是逆序
                if xdata[len(xdata) - 1] - xdata[0] < 0:
                    positive_order = False

                if positive_order:
                    index_new = np.searchsorted(xdata_new, [x_new])[0]
                    # 溢出处理
                    if index_new >= len(xdata_new):
                        _point, = self.axs[i].plot(xdata_new[0], ydata_new[0], color=lines[j].get_color(), marker='o', markersize = 4, visible=False)
                        _point.set_animated(False)
                        points.append(_point)
                        continue
                    elif x_new > xdata_new[index_new]:
                        _point, = self.axs[i].plot(xdata_new[len(xdata_new)-1], ydata_new[len(xdata_new)-1], color=lines[j].get_color(), marker='o', markersize = 4, visible=False)
                        _point.set_animated(False)
                        points.append(_point)
                        continue
                    elif x_new < xdata_new[0]:
                        _point, = self.axs[i].plot(xdata_new[0], ydata_new[0], color=lines[j].get_color(), marker='o', markersize = 4, visible=False)
                        _point.set_animated(False)
                        points.append(_point)
                        continue
                else:
                    datax_sort = np.copy(xdata_new)
                    datax_sort.sort()
                    datay_sort = np.copy(ydata_new)
                    datay_sort.sort()

                    index_new = np.searchsorted(datax_sort, [x_new])[0]
                    # 溢出处理
                    if index_new >= len(datax_sort):
                        _point, = self.axs[i].plot(datax_sort[0], datay_sort[0], color=lines[j].get_color(), marker='o', markersize = 4, visible=False)
                        _point.set_animated(False)
                        points.append(_point)
                        continue
                    elif x_new > datax_sort[index_new]:
                        _point, = self.axs[i].plot(xdata_new[len(xdata_new)-1], ydata_new[len(xdata_new)-1], color=lines[j].get_color(), marker='o', markersize = 4, visible=False)
                        _point.set_animated(False)
                        points.append(_point)
                        continue
                    elif x_new < datax_sort[0]:
                        x_new = datax_sort[0]

                if len(xdata_new) == 1:
                    x_new = xdata_new[index_new]
                    y_new = ydata_new[index_new]
                else:
                    x_right = xdata_new[index_new]
                    y_right = ydata_new[index_new]
                    x_left = xdata_new[index_new - 1]
                    y_left = ydata_new[index_new - 1]
                    y_new = (y_right - y_left) / (x_right - x_left) * (x_new - x_left) + y_left

                # 添加点
                _point, = self.axs[i].plot(x_new, y_new, color=lines[j].get_color(), marker='o', markersize = 4, visible=True)
                _point.set_animated(False)
                points.append(_point)

                # 添加注释
                label = lines[j].get_label()
            
                # 标签文本，显示点坐标
                text += self.parse_text(y_new, label, 'y')
                    
                self.annotation._linecolors.append(lines[j].get_color())

            self.points.append(points)

        self.annotation.set_text(text)
        self.line.set_xdata(x_new)
        self.annotation.draggable(True)

    def init_annotation_have_closed_curve(self, left, right):
        # 初始化annotation
        text = ''
        x = (left + right)/2
        buttom, top = self.ax.get_ylim()
        y = (buttom + top)/2

        # 获取最近点的坐标
        x, y = self.ax.transData.transform((x, y))
        index0, index, index1 = self._get_closest_point(x, y)
        self.clost_point = (index, index1, index0)
        line = self.lst_lines[index0][index]
        xdata_origin = line.get_xdata()
        xdata = self.convert_data(xdata_origin)
        ydata_origin = line.get_ydata()
        ydata = self.convert_data(ydata_origin)
        x_new = xdata_origin[index1]
        y_new = ydata_origin[index1]

        # 处理游标线
        self.hline = self.ax.axhline(y = y_new,
                                color='c',linewidth=1)
        self.hline.set_animated(False)

        self.annotation.init_linecolors()
        # 标签文本，显示点坐标
        y_label = line.get_label()
        text += self.parse_text(x_new,'x')
        text += self.parse_text(y_new, y_label, 'y')

        self.annotation._linecolors.append(line.get_color())

        # 游标与曲线交点
        points = self.axs[index0].plot(x_new, y_new, color=line.get_color(), marker='o', markersize = 4, visible=True)
        points[0].set_animated(False)
        self.points.append(points)

        self.annotation.set_text(text)
        self.line.set_xdata(x_new)
        self.hline.set_ydata(y_new)
        self.annotation.draggable(True)

    def get_pixels_datas(self):
        self.pixels = []
        self.indexs = []

        for i in range(0, len(self.lst_lines)):
            lines = self.lst_lines[i]
            for j in range(0, len(lines)):
                xdata = lines[j].get_xdata()
                xdata = self.convert_data(xdata)
                ydata = lines[j].get_ydata()
                ydata = self.convert_data(ydata)
                for k in range(0, len(xdata)):
                    pos = self.ax.transData.transform((xdata[k], ydata[k]))
                    self.pixels.append(pos)
                    self.indexs.append((i,j,k))

    def connect(self):
        """连接事件信号槽"""
        self.cid_press = self.line.figure.canvas.mpl_connect(
            'button_press_event', self.mouse_press)
        self.cid_motion = self.line.figure.canvas.mpl_connect(
            'motion_notify_event', self.mouse_move)
        self.cid_release = self.line.figure.canvas.mpl_connect(
            'button_release_event', self.mouse_release)
        # self.cid_draw = self.line.figure.canvas.mpl_connect(
        #     'draw_event', self.on_draw)
        self.cid_key_press = self.fig.canvas.mpl_connect(
            'key_press_event', self.on_key_press)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

        self.draw_self()

    def draw_self(self):
        self.ax.draw_artist(self.line)
        self.ax.draw_artist(self.annotation)
        if self.closed_curve:
            self.ax.draw_artist(self.hline)
        for points in self.points:
            for point in points:
                point.axes.draw_artist(point)

    def mouse_press(self, event):
        if self.press:
            return

        if mw_get_cax(self.line.axes) != mw_get_cax(event.inaxes):
            return

        contains, attrd = self.line.contains(event)

        if not contains:
            return

        self.press = True

        # 由于在拖拽游标线时，有可能光标拖至其他坐标轴，与数据提示事件冲突
        # 故在游标press时禁用数据提示功能,在release时取消禁用
        mw_get_cfig().current_mplcursor.checked_tool_num += 1

        mw_get_cfig().zoom_flag = False
        mw_get_cfig().pan_flag = False
        self._update()

    def mouse_release(self, event):
        if not self.press:
            return

        self.press = False

        mw_get_cfig().current_mplcursor.checked_tool_num -= 1

        # # 重新使能工具栏
        # if mw_get_cfig().zoom_flag:
        #     action_zoom()

        # if mw_get_cfig().pan_flag:
        #     action_pan()

    def mouse_move(self, event):
        if not self.press:
            if not event.inaxes:
                # self.line.figure.canvas.setCursor(Qt.ArrowCursor)
                self.line.figure.canvas.set_cursor(Cursors.POINTER)
                self.canvas.send_event({"cursor":"auto"})
                return
            elif mw_get_cax(event.inaxes) == None:
                return
            elif not mw_get_cax(event.inaxes).cursor or mw_get_cax(event.inaxes) != mw_get_cax(self.line.axes):
                return

            contains, attrd = self.line.contains(event)

            if contains:
                self.canvas.send_event("cursor",cursor = "e-resize")
                # self.line.figure.canvas.setCursor(Qt.SizeHorCursor)
                # self.line.figure.canvas.set_cursor(Cursors.RESIZE_HORIZONTAL)
                #self.pick = True
            else:
                self.canvas.send_event({"cursor":"auto"})
                
                mode = self.toolbar.mode.name
                if mode == "ZOOM":
                    self.line.figure.canvas.set_cursor(Cursors.SELECT_REGION)
                elif mode == "PAN":
                    self.line.figure.canvas.set_cursor(Cursors.MOVE)
                else:
                    self.line.figure.canvas.set_cursor(Cursors.POINTER)
                # zoom_status = mw_get_cax().
                # zoom_button = mw_get_toolbutton(plt.gcf(), 'zoom')
                # pan_button = mw_get_toolbutton(plt.gcf(), 'pan')
                # if zoom_button.isChecked():
                #     self.canvas.send_event({"cursor":"crosshair"})
                #     # self.line.figure.canvas.setCursor(Qt.CrossCursor)
                # elif pan_button.isChecked():
                #     self.canvas.send_event({"cursor":"move"})
                #     # self.line.figure.canvas.setCursor(Qt.SizeAllCursor)
                # else:
                #     self.canvas.send_event({"cursor":"auto"})
                #     # self.line.figure.canvas.setCursor(Qt.ArrowCursor)
                # #self.pick = False
        # elif self.pick:
        else:
            # 设置zoom工具栏的开关

            # mode = self.toolbar.mode.name

            # mw_get_cfig().zoom_flag = mw_get_cfig().zoom_flag | (mode=="ZOOM")
            # if mw_get_cfig().zoom_flag:
            #     action_zoom()

            # mw_get_cfig().pan_flag = mw_get_cfig().pan_flag | (mode=="PAN")
            # if mw_get_cfig().pan_flag:
            #     action_pan()

            # 设置光标模式
            # self.line.figure.canvas.setCursor(Qt.SizeHorCursor)
            self.line.figure.canvas.set_cursor(Cursors.RESIZE_HORIZONTAL)
            self.canvas.send_event({"cursor":"col-resize"})
            pos_x, pos_y = event.x, event.y
            x, y = self.ax.transData.inverted().transform([pos_x, pos_y])

            self.annotation.init_linecolors()
            text = ''
            if self.closed_curve:
                index0, index, index1  = self._get_closest_point(pos_x, pos_y)
                self.clost_point = (index, index1, index0)
                line = self.lst_lines[index0][index]
                xdata_origin = line.get_xdata()
                xdata = self.convert_data(xdata_origin)
                ydata_origin = line.get_ydata()
                ydata = self.convert_data(ydata_origin)
                x_new = xdata_origin[index1]
                y_new = ydata_origin[index1]

                # 标签文本，显示点坐标
                text += self.parse_text(x_new,'x')
                text += self.parse_text(y_new,'y','y')

                self.annotation._linecolors.append(line.get_color())

                #隐藏原来的数据点
                for points in self.points:
                    for point in points:
                        point._visible = False

                # 处理游标线
                self.points[0][0]._visible = True
                self.points[0][0].set_data([x_new], [y_new])
                self.points[0][0].set_color(line.get_color())

                # self.line.set_xdata(x_new)
                self.hline.set_ydata(y_new)
                # self.annotation.set_text(text)
            else:
                index0, index, index1 = self._get_min_index(x)

                # 如果x没有穿过一条线，则在所有的线端点找一个最近的点
                if index0 == -1 and index == -1 and index1 == -1:
                    index0, index, index1 = self._get_closest_Endpoint(x)
                    xdata = self.lst_lines[index0][index].get_xdata()
                    xdata = self.convert_data(xdata)
                    x_new = xdata[index1]
                else:
                    xdata = self.lst_lines[index0][index].get_xdata()
                    xdata = self.convert_data(xdata)
                    x_new = xdata[index1]

                #隐藏原来的数据点
                for points in self.points:
                    for point in points:
                        point._visible = False

                text += self.parse_text(x_new,'x')

                for j in range(0, len(self.lst_lines)):
                    self.lines = self.lst_lines[j]
                    for i in range(0, len(self.lines)):
                        xdata_new = self.lines[i].get_xdata()
                        xdata_new = self.convert_data(xdata_new)
                        ydata_new = self.lines[i].get_ydata()
                        ydata_new = self.convert_data(ydata_new)

                        positive_order = True
                        # 判断是正序还是逆序
                        if xdata[len(xdata) - 1] - xdata[0] < 0:
                            positive_order = False

                        if positive_order:
                            index_new = np.searchsorted(xdata_new, [x_new])[0]

                            # 溢出处理
                            if index_new >= len(xdata_new):
                                continue
                            elif x_new > xdata_new[index_new]:
                                continue
                            elif x_new < xdata_new[0]:
                                continue
                            elif x_new > xdata_new[len(xdata_new) - 1]:
                                if  xdata_new[len(xdata_new) - 1] == x_new:
                                    label = self.lines[i].get_label()
                                    y_new = ydata_new[len(xdata_new) - 1]
                                    text += self.parse_text(y_new,label,'y')
                                    continue
                            elif x_new < xdata_new[0]:
                                if  xdata_new[len(xdata_new) - 1] == x_new:
                                    label = self.lines[i].get_label()
                                    y_new = ydata_new[0]
                                    text += self.parse_text(y_new,label,'y')
                                    continue
                        else:
                            datax_sort = np.copy(xdata_new)
                            datax_sort.sort()
                            datay_sort = np.copy(ydata_new)
                            datay_sort.sort()

                            index_new = np.searchsorted(datax_sort, [x_new])[0]

                            # 溢出处理
                            if index_new >= len(datax_sort):
                                continue
                            elif x_new > datax_sort[index_new]:
                                continue
                            elif x_new < datax_sort[0]:
                                continue
                            elif x_new > datax_sort[len(datax_sort) - 1]:
                                if  datax_sort[len(datax_sort) - 1] == x_new:
                                    label = self.lines[i].get_label()
                                    y_new = datay_sort[len(datax_sort) - 1]
                                    text += self.parse_text(y_new,label,'y')
                                    self.annotation._linecolors.append(self.lines[i].get_color())
                                    continue
                            elif x_new < datax_sort[0]:
                                if  datax_sort[len(datax_sort) - 1] == x_new:
                                    label = self.lines[i].get_label()
                                    y_new = datay_sort[0]
                                    text += self.parse_text(y_new,label,'y')
                                    self.annotation._linecolors.append(self.lines[i].get_color())
                                    continue

                        if len(xdata_new) == 1:
                            x_new = xdata_new[index_new]
                            y_new = ydata_new[index_new]
                        else:
                            x_right = xdata_new[index_new]
                            y_right = ydata_new[index_new]
                            x_left = xdata_new[index_new - 1]
                            y_left = ydata_new[index_new - 1]
                            y_new = (y_right - y_left) / (x_right - x_left) * (x_new - x_left) + y_left

                        # 添加点
                        self.points[j][i].set_data([x_new], [y_new])
                        self.points[j][i]._visible = True
                        # _point = self.ax.plot(x_new, y_new, color=self.lines[i].get_color(), marker='o', visible=True)
                        # self.points.append(_point)

                        # 添加注释
                        label = self.lines[i].get_label()
                        text += self.parse_text(y_new,label,'y')
                        self.annotation._linecolors.append(self.lines[i].get_color())

            #self.annotation.set_text(text)
            self.annotation._text = text
            self.line.set_xdata(x_new)
            self._update()
            # self.line.figure.canvas.draw()

    def on_key_press(self, event):
        if self.press:
            return

        if event.key in ['left', 'up']:
            self.current_selection_pos_sub(event)
            return
        elif event.key in ['right', 'down']:
            self.current_selection_pos_add(event)
            return

    # 游标右移
    def current_selection_pos_add(self, event):
        """
        键盘右键或下键使游标右移
        """
        if mw_get_cax(self.line.axes) != mw_get_cax(plt.gca()):
            return

        if self.closed_curve:
            text = ''
            index, index1, index0 = self.clost_point
            length = len(self.lst_lines[index0][index].get_xdata())
            index1 = index1 + 1
            if index1 > length - 1:
                index1 = 0

            self.clost_point = index, index1, index0

            line = self.lst_lines[index0][index]
            xdata_origin = line.get_xdata()
            xdata = self.convert_data(xdata_origin)
            ydata_origin = line.get_ydata()
            ydata = self.convert_data(ydata_origin)
            x_new = xdata_origin[index1]
            y_new = ydata_origin[index1]

            self.annotation.init_linecolors()
            # 标签文本，显示点坐标
            text += self.parse_text(x_new,'x')
            text += self.parse_text(y_new, 'y', 'y')

            self.annotation._linecolors.append(line.get_color())

            #隐藏原来的数据点
            for points in self.points:
                for point in points:
                    point._visible = False

            # 处理游标线
            self.points[0][0]._visible = True
            self.points[0][0].set_data([x_new], [y_new])

            # self.line.set_xdata(x_new)
            self.hline.set_ydata(y_new)
            # self.annotation.set_text(text)

        else:
            # 先获取当前游标所在位置
            x = self.line.get_xdata()

            # 找出右侧最接近的点
            # 先找出每条线右侧最接近的点
            lst_min = []
            for lines in self.lst_lines:
                for line in lines:
                    xdata = line.get_xdata()
                    xdata = self.convert_data(xdata)
                    datax_sort = np.copy(xdata)
                    datax_sort.sort()
                    data_min = np.searchsorted(datax_sort,x)
                    if data_min > len(datax_sort) - 1:
                        continue

                    if datax_sort[data_min] != x:
                        lst_min.append(datax_sort[data_min])
                    elif len(datax_sort) > data_min + 1:
                        lst_min.append(datax_sort[data_min + 1])

            # 在找出所有点中最接近的点作为x_new
            if len(lst_min) > 0:
                lst_min.sort()
                x_next_index = np.searchsorted(lst_min,x)
                if x_next_index > len(lst_min):
                    return
                else:
                    x_new = lst_min[x_next_index]
            else:
                return

            #隐藏原来的数据点
            for points in self.points:
                for point in points:
                    point._visible = False

            self.annotation.init_linecolors()
            # 标签文本，显示点坐标
            text = self.parse_text(x_new, 'x')

            for j in range(0, len(self.lst_lines)):
                self.lines = self.lst_lines[j]
                for i in range(0, len(self.lines)):
                    xdata = self.lines[i].get_xdata()
                    xdata = self.convert_data(xdata)
                    ydata = self.lines[i].get_ydata()
                    ydata = self.convert_data(ydata)

                    positive_order = True
                    # 判断是正序还是逆序
                    if xdata[len(xdata) - 1] - xdata[0] < 0:
                        positive_order = False

                    if positive_order:
                        index_new = np.searchsorted(xdata, [x_new])[0]
                        # index_new = index + 1

                        # 溢出处理
                        if index_new > len(xdata) - 1:
                            continue
                        elif x_new > xdata[index_new]:
                            continue
                        elif x_new < xdata[0]:
                            continue
                    else:
                        datax_sort = np.copy(xdata)
                        datax_sort.sort()
                        index_new = np.searchsorted(datax_sort, [x_new])[0]

                        # 溢出处理
                        if index_new > len(datax_sort) - 1:
                            continue
                        elif x_new > datax_sort[index_new]:
                            continue
                        elif x_new < datax_sort[0]:
                            continue

                        index_new = len(datax_sort) - index_new - 1

                    x_right = xdata[index_new]
                    y_right = ydata[index_new]
                    x_left = xdata[index_new - 1]
                    y_left = ydata[index_new - 1]
                    y_new = (y_right - y_left) / (x_right - x_left) * (x_new - x_left) + y_left

                    # 添加点
                    self.points[j][i].set_data([x_new], [y_new])
                    self.points[j][i]._visible = True

                    # 添加注释
                    label = self.lines[i].get_label()
                    text += self.parse_text(y_new,label,'y')
                    self.annotation._linecolors.append(self.lines[i].get_color())

        self.annotation._text = text
        self.line.set_xdata(x_new)
        self._update()

    # 游标左移
    def current_selection_pos_sub(self, event):
        """
        键盘左键或上键使游标左移
        """
        if mw_get_cax(self.line.axes) != mw_get_cax(plt.gca()):
            return

        if self.closed_curve:
            text = ''
            index, index1, index0 = self.clost_point
            length = len(self.lst_lines[index0][index].get_xdata())
            index1 = index1 - 1
            if index1 < 0:
                index1 = length - 1

            self.clost_point = index, index1, index0

            line = self.lst_lines[index0][index]
            xdata_origin = line.get_xdata()
            xdata = self.convert_data(xdata_origin)
            ydata_origin = line.get_ydata()
            ydata = self.convert_data(ydata_origin)
            x_new = xdata_origin[index1]
            y_new = ydata_origin[index1]


            self.annotation.init_linecolors()
            # 标签文本，显示点坐标
            text += self.parse_text(x_new, 'x')
            text += self.parse_text(y_new, 'y', 'y')
            
            self.annotation._linecolors.append(line.get_color())

            #隐藏原来的数据点
            for points in self.points:
                for point in points:
                    point._visible = False

            # 处理游标线
            self.points[0][0]._visible = True
            self.points[0][0].set_data([x_new], [y_new])

            # self.line.set_xdata(x_new)
            self.hline.set_ydata(y_new)
            # self.annotation.set_text(text)
        else:
            # 先获取当前游标所在位置
            x = self.line.get_xdata()

            # 找出左侧最接近的点
            # 先找出每条线左侧最接近的点
            lst_min = []
            for lines in self.lst_lines:
                for line in lines:
                    xdata = line.get_xdata()
                    xdata = self.convert_data(xdata)
                    datax_sort = np.copy(xdata)
                    datax_sort.sort()
                    data_min = np.searchsorted(datax_sort,x) - 1
                    # data_min = np.searchsorted(xdata,x) - 1
                    if data_min < 0:
                        continue

                    lst_min.append(datax_sort[data_min])

            # 在找出所有点中最接近的点作为x_new
            if len(lst_min) > 0:
                lst_min.sort()
                x_new = lst_min[len(lst_min) - 1]
            else:
                return

            #隐藏原来的数据点
            for points in self.points:
                for point in points:
                    point._visible = False

            has_datetime_x = self.lines_has_datetime_x()
            self.annotation.init_linecolors()
            # 标签文本，显示点坐标
            
            text = self.parse_text(x_new, 'x')

            for j in range(0, len(self.lst_lines)):
                self.lines = self.lst_lines[j]
                for i in range(0, len(self.lines)):
                    xdata = self.lines[i].get_xdata()
                    xdata = self.convert_data(xdata)
                    ydata = self.lines[i].get_ydata()
                    ydata = self.convert_data(ydata)
                    # index = np.searchsorted(xdata, [x_new])[0]

                    positive_order = True
                    # 判断是正序还是逆序
                    if xdata[len(xdata) - 1] - xdata[0] < 0:
                        positive_order = False

                    if positive_order:
                        index = np.searchsorted(xdata, [x_new])[0]

                        # 溢出处理
                        if index > len(xdata) - 1:
                            continue
                        elif index < 0:
                            continue
                        elif x_new > xdata[index]:
                            continue
                        elif x_new < xdata[0]:
                            continue
                    else:
                        datax_sort = np.copy(xdata)
                        datax_sort.sort()
                        index = np.searchsorted(datax_sort, [x_new])[0]

                        # 溢出处理
                        if index > len(datax_sort) - 1:
                            continue
                        elif index < 0:
                            continue
                        elif x_new > datax_sort[index]:
                            continue
                        elif x_new < datax_sort[0]:
                            continue

                        index = len(datax_sort) - index - 1

                    x_right = xdata[index]
                    y_right = ydata[index]
                    x_left = xdata[index - 1]
                    y_left = ydata[index - 1]
                    y_new = (y_right - y_left) / (x_right - x_left) * (x_new - x_left) + y_left

                    # 添加点
                    self.points[j][i].set_data([x_new], [y_new])
                    self.points[j][i]._visible = True

                    # 添加注释
                    label = self.lines[i].get_label()

                    text += self.parse_text(y_new, label, 'y')

                    self.annotation._linecolors.append(self.lines[i].get_color())

        self.annotation._text = text
        self.line.set_xdata(x_new)
        self._update()

    def _get_min_index(self, x):
        """
            获取所有曲线中,最接近游标的x坐标的曲线index,以及当前x坐标所在数据的index1
        """
        lst = []
        dict = {}
        dict1 = {}
        for i in range(0, len(self.lst_lines)):
            self.lines = self.lst_lines[i]
            _dict = {}
            _dict1 = {}
            _lst = []
            for j in range(0, len(self.lines)):
                xdata = self.lines[j].get_xdata()
                xdata = self.convert_data(xdata)
                xdata = self.ax._validate_converted_limits(xdata, self.ax.convert_xunits)

                positive_order = True
                # 判断是正序还是逆序
                if xdata[len(xdata) - 1] < xdata[0]:
                    positive_order = False

                if positive_order:
                    index = np.searchsorted(xdata, [x])[0]
                    # 溢出处理，当x不在xdata范围内时，跳过这条曲线
                    if index >= len(xdata):
                        continue
                    elif x > xdata[index]:
                        continue
                    elif x < xdata[0]:
                        continue

                    # 找到该线上距离x最近的一个点
                    if index + 1 >= len(xdata):
                        _lst.append(xdata[index])
                        _dict[j] = index
                        _dict1[j] = xdata[index]
                    elif (x - xdata[index - 1]) >= (xdata[index] - x):
                        _lst.append(xdata[index])
                        _dict[j] = index
                        _dict1[j] = xdata[index]
                    else:
                        _lst.append(xdata[index - 1])
                        _dict[j] = index - 1
                        _dict1[j] = xdata[index - 1]
                else:
                    data_sort = np.copy(xdata)
                    data_sort.sort()

                    index = np.searchsorted(data_sort, [x])[0]
                    # 溢出处理，当x不在xdata范围内时，跳过这条曲线
                    if index >= len(data_sort):
                        continue
                    elif x > data_sort[index]:
                        continue
                    elif x < data_sort[0]:
                        continue

                    # 找到该线上距离x最近的一个点
                    if index + 1 > len(data_sort):
                        _lst.append(data_sort[index])
                        _dict[j] = len(data_sort) - index - 1
                        _dict1[j] = data_sort[index]
                    elif (x - data_sort[index - 1]) >= (data_sort[index] - x):
                        _lst.append(data_sort[index])
                        _dict[j] = len(data_sort) - index - 1
                        _dict1[j] = data_sort[index]
                    else:
                        _lst.append(data_sort[index - 1])
                        _dict[j] = len(data_sort) - (index - 1) - 1
                        _dict1[j] = data_sort[index - 1]

            dict[i] = _dict
            dict1[i] = _dict1
            lst.append(_lst)

        min = 0
        index = -1
        index1 = -1
        index0 = -1

        if len(dict)>0:
            for i in range(0, len(self.lst_lines)):
                self.lines = self.lst_lines[i]
                _dict = dict[i]
                _lst = lst[i]
                for j in range(0, len(self.lines)):
                    if j in _dict.keys():
                        index1 = _dict[j]
                        index = j
                        index0 = i
                        min = abs(x - _lst[0])
                        break
        else:
            index1 = -1

        # 在所有的点中找到与x最接近的点的横坐标作为游标线的横坐标
        for i in range(0, len(lst)):
            _lst = lst[i]
            _dict1 = dict1[i]
            _dict = dict[i]
            for j in range(0, len(_lst)):
                if abs(x - _lst[j]) < min:
                    min = abs(x - _lst[j])
                    # for j in range(0, len(self.lst_lines)):
                    #     self.lines = self.lst_lines[j]
                    # for j in range(0, len(self.lines)):
                    if j in _dict1.keys():
                        if _dict1[j] == _lst[j]:
                            index1 = _dict[j]
                            index = j
                            index0 = i
                            break

        # index0: 第index0个lines数组，index: 数组中第index条曲线，index1: 曲线上第index1个点
        return index0, index, index1

    def _get_closest_point(self, x, y):
        min_distance = np.inf
        index = -1
        index1 = -1
        index0 = -1
        for i in range(0, len(self.pixels)):
            pos = self.pixels[i]
            indexs = self.indexs[i]
            distance = (x - pos[0])**2 + (y - pos[1])**2
            if distance == 0:
                return indexs
            elif min_distance > distance:
                index0 = indexs[0]
                index = indexs[1]
                index1 = indexs[2]
                min_distance = distance

        return index0, index, index1

    def _get_closest_Endpoint(self, x):
        index0 = -1
        index = -1
        index1 = -1
        x_min = np.inf
        for i in range(0, len(self.lst_lines)):
            lines = self.lst_lines[i]
            for j in range(0, len(lines)):
                xdata = lines[j].get_xdata()
                xdata = self.convert_data(xdata)
                xdata = self.ax._validate_converted_limits(xdata, self.ax.convert_xunits)
                
                x_start = xdata[0]
                x_end = xdata[-1]
                if abs(x_start - x) < x_min:
                    x_min = abs(x_start - x)
                    index0 = i
                    index = j
                    index1 = 0

                if abs(x_end - x) < x_min:
                    x_min = abs(x_end - x)
                    index0 = i
                    index = j
                    index1 = len(xdata) - 1

        return index0, index, index1

    def _update(self):
        self.fig.canvas.draw_idle()
        # update_all(self.fig)

    def convert_data(self,data):
        if data is None:
            return []

        if np.isscalar(data):
            return self.ax._validate_converted_limits(data, self.ax.convert_xunits)
        elif isinstance(data[0], datetime):
            return self.ax._validate_converted_limits(data, self.ax.convert_xunits)
        else:
            return data

    def lines_has_datetime_x(self):
        for line in self.lines:
            xdata = line.get_xdata()
            if ((np.isscalar(xdata) and isinstance(xdata, datetime))
                or isinstance(xdata[0], datetime)):
                return True
        
        return False

    def lines_has_datetime_y(self):
        for line in self.lines:
            ydata = line.get_ydata()
            if ((np.isscalar(ydata) and isinstance(ydata, datetime))
                or isinstance(ydata[0], datetime)):
                return True
        
        return False

    def float2datetime(self, val):
        return str(datetime(1970, 1, 1, 0, 0) + (timedelta(val)))

    def parse_text(self, value, label='', axis = 'x'):
        if axis == 'x':
            has_datetime = self.lines_has_datetime_x()
        else:
            label = '\n(' + label + ')'
            has_datetime = self.lines_has_datetime_y()

        # 标签文本，显示点坐标
        if isinstance(value,datetime):
            text = label + '=' + str(value)
        elif has_datetime: 
            text = label + '=' + self.float2datetime(value)
        else:
            text = str_remove_zeros('%s=%1.6g' % (label, value))

        return text
