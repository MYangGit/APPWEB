"""
名称：mw_draw_graphics
功能：绘制图形
实现：每一个类型的图形的插入都用一个类实现，包括：线条、箭头、文本箭头、双箭头、文本框、矩形、圆形等
接口：插入图形类DrawLines、CDrawLine、DrawRect、DrawEllipse、CDrawGraphics
依赖：mw_interface
"""
from matplotlib.patches import Rectangle,Ellipse
from matplotlib.backend_bases import MouseButton
# from settings.mw_setting_base import CPropertySetting
from matplotlib.text import Annotation,Text
import numpy as np

from TyPlotOnline.objects.mw_interface import *

# 用户绘制线条图形的类
class DrawLines(object):
    """
    绘制线条、箭头、文本箭头、双箭头类
    """

    lock = None
    motion_lock = None

    def __init__(self, fig, line_type = 'line'):
        """
        Parameters:
        -------------------------
        fig : 图窗对象
        line_type : 线类型str
            {'line', 'arrow', 'textarrow', 'doubl_arrow'}
        """
        self.fig = fig
        self.canvas = self.fig.canvas
        self.press = False
        self.start = None
        self.picked = True
        self.background = None
        self.move = False

        self.line = None
        self.start_point = None
        self.end_point = None

        self.line_type = line_type
        self.dict_type_style = {'line' : '-',
                    'arrow' : '->',
                    'doublearrow' : '<->',
                    'textarrow' : '->'}
        self.style = self.dict_type_style[self.line_type]

        # self.canvas.setCursor(Qt.CrossCursor)
        # self.canvas.send_event({"cursor":"crosshair"})
        self.canvas.send_event("cursor", cursor = "crosshair")

    def create_pick_state(self):
        """
        创建直线两端的缩放点
        """
        # x = self.start[0]
        # y = self.start[1]
        (x,y) = self.fig.transFigure.inverted().transform((self.start[0],self.start[1]))
        self.start_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
        self.end_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')

        self.start_point.set_animated(True)
        self.end_point.set_animated(True)
        # self.start_point.set_transform(self.fig.get_transform())
        # self.end_point.set_transform(self.fig.get_transform())
        self.start_point.set_transform(self.fig.transFigure)
        self.end_point.set_transform(self.fig.transFigure)

        self.fig.add_artist(self.start_point)
        self.fig.add_artist(self.end_point)

    # 绘制图形的事件函数
    def connect_draw(self):
        """连接事件信号槽"""
        self.cid_draw_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_draw_press)
        self.cid_draw_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_draw_release)
        self.cid_draw_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_draw_motion)
        # self.cid_draw = self.line.figure.canvas.mpl_connect(
        #     'draw_event', self.on_draw)

    def disconnect_draw(self):
        """断开信号槽连接"""
        self.fig.canvas.mpl_disconnect(self.cid_draw_press)
        self.fig.canvas.mpl_disconnect(self.cid_draw_release)
        self.fig.canvas.mpl_disconnect(self.cid_draw_motion)

    def on_draw_press(self, event):
        if self.press:
            return

        if not mw_get_cfig().edit_mode:
            return

        self.press = True
        self.start = (event.x, event.y)

        self.line = Annotation('',
                    xy=self.start, xycoords='figure pixels',
                    xytext=self.start, textcoords='figure pixels',
                    arrowprops=dict(arrowstyle=self.style,
                                    connectionstyle="arc3"),
                    # bbox=dict(fc="none", ec="none"),
                    annotation_clip=False,)
        self.line.set_animated(True)
        self.line.set_in_layout(False)
        self.fig.add_artist(self.line)

        # 由于原线难以选中，故绘制一条隐藏的辅助线帮助选中
        self.auxiliary_line = Line2D([event.x,event.x], [event.y,event.y], clip_on = False, linestyle = '-',linewidth=10)
        self.auxiliary_line.set_transform(self.fig.get_transform())
        self.auxiliary_line.set_animated(True)
        self.auxiliary_line.set_in_layout(False)
        self.auxiliary_line.set_visible(False)
        self.fig.add_artist(self.auxiliary_line)

        self.create_pick_state()

        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self._update()

    def on_draw_motion(self, event):
        if not self.press:
            return

        self.line.xy = (event.x, event.y)
        end_pos = self.end_point.get_transform().inverted().transform((event.x,event.y))
        self.end_point.set_data([end_pos[0]], [end_pos[1]])
        self.auxiliary_line.set_data([self.start[0],event.x],[self.start[1],event.y])

        self.move = True
        self._update()

    def on_draw_release(self, event):
        if not self.press:
            return

        if not self.move:
            end_pos = (self.start[0] + 90, self.start[1] + 30)
            self.line.xy = end_pos
            end_pos_normalized = self.end_point.get_transform().inverted().transform((end_pos[0],end_pos[1]))
            self.end_point.set_data([end_pos_normalized[0]], [end_pos_normalized[1]])
            self.auxiliary_line.set_data([self.start[0],end_pos[0]],[self.start[1],end_pos[1]])
            self._update()

        self.press_point = None
        self.press = False

        self.disconnect_draw()
        self.fig.canvas.send_event("toolbar_update", action="Draw", active=False)

        update_draw_button_status(self.fig, '')

        if self.line_type == 'line':
            dline = CDLine(self.fig, self.line, self.start_point, self.end_point, self.auxiliary_line, self.line_type)
        elif self.line_type == 'arrow':
            dline = CDArrow(self.fig, self.line, self.start_point, self.end_point, self.auxiliary_line, self.line_type)
        elif self.line_type == 'textarrow':
            dline = CDTextArrow(self.fig, self.line, self.start_point, self.end_point, self.auxiliary_line, self.line_type)
        elif self.line_type == 'doublearrow':
            dline = CDDoubleArrow(self.fig, self.line, self.start_point, self.end_point, self.auxiliary_line, self.line_type)

        dline.connect()
        mw_get_cfig().draw_lines.append(dline)
        mw_get_cfig().current_objs.append(dline)
        self.fig.canvas.draw_idle()

    def draw_self(self):
        self.fig.draw_artist(self.line)
        self.fig.draw_artist(self.start_point)
        self.fig.draw_artist(self.end_point)
        self.fig.draw_artist(self.auxiliary_line)

    def _update(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)

        # for dline in mw_get_cfig().draw_lines:
        #     dline.draw_self()

        self.draw_self()

        self.canvas.blit(self.fig.bbox)

class CDrawLine(object):
    """
    直线、箭头、双箭头、文本箭头类
    管理对象属性
    """
    lock = None
    motion_lock = None

    def __init__(self, fig, line, start_point, end_point, auxiliary_line, line_type):
        """
        Parameters:
        -------------------------
        fig : 图窗对象
        line : 线对象
        start_point : 缩放起始点
        end_point : 缩放终止点
        auxiliary_line : 辅助线，用于辅助选中
        line_type : 线类型str
            {'line', 'arrow', 'textarrow', 'doublearrow'}
        """
        self.fig = fig
        self.canvas = self.fig.canvas
        self.press = False
        self.start = None
        self.picked = True
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self.fix_ax_start = None
        self.fix_ax_end = None

        self.line = line
        self.start_point = start_point
        self.end_point = end_point
        self.auxiliary_line = auxiliary_line
        self.line_type = line_type

        self.contains_line = False
        self.contains_start = False
        self.contains_end = False

        self.units = 'normalized'
        self.linestyle = self.line.arrow_patch.get_linestyle()

        self.dict_style = {'实线' : ['-', 'solid'],
                    '虚线' : ['--', 'dashed'],
                    '点线' : [':', 'dotted'],
                    '点划线' : ['-.', 'dashdot'],
                    '无' : ['None', ' ', '', 'none']}

        self.init_line()
        
    def before_export(self):
        self.canvas = None
        self.background = None
        if self.cid_draw:
            self.fig.canvas.mpl_disconnect(self.cid_draw)

    def after_export(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()

    def after_import(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()
        
    # 操作图形的事件函数
    def init_line(self):
        if self.line_type == 'textarrow':
            self.text = Text(x=10,y=10,
                            text='text',
                            bbox=dict(fc="none", ec="none"),)
                            # verticalalignment='baseline',)
                            # horizontalalignment='center',)
            self.text.set_transform(self.fig.get_transform())
            self.text.set_animated(True)
            self.text.set_in_layout(False)
            self.fig.add_artist(self.text)

    def update_line_by_points_pos(self, start_pos = None, end_pos = None):
        """
        根据线两端端点的左边更新线的位置

        Parameters:
        ------------------------------
        start_pos : 起始点坐标（像素）
        end_pos : 终止点坐标（像素）
        """

        if start_pos == None:
            start_pos = self.start_point.get_transform().transform((self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        if end_pos == None:
            end_pos = self.end_point.get_transform().transform((self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        self.line.xy = tuple(end_pos)
        self.line._x = start_pos[0]
        self.line._y = start_pos[1]
        self.auxiliary_line.set_data([start_pos[0], end_pos[0]],[start_pos[1], end_pos[1]])

    def connect(self):
        self.cid_press = self.line.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cid_release = self.line.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cid_motion = self.line.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        self.cid_draw = self.line.figure.canvas.mpl_connect(
            'draw_event', self.on_draw)
        self.cid_key_press = self.fig.canvas.mpl_connect(
            'key_press_event', self.on_key_press)

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_press)
        self.fig.canvas.mpl_disconnect(self.cid_release)
        self.fig.canvas.mpl_disconnect(self.cid_motion)
        self.fig.canvas.mpl_disconnect(self.cid_draw)
        self.fig.canvas.mpl_disconnect(self.cid_key_press)

    def on_press(self, event):
        if not mw_get_cfig(self.fig).edit_mode:
            return

        if (CDrawLine.lock is not None):
            return

        if event.button is MouseButton.RIGHT:
            return

        contains_start, attrd = self.start_point.contains(event)
        contains_end, attrd = self.end_point.contains(event)
        contains_line, attrd = self.auxiliary_line.contains(event)
        if contains_start:
            self.contains_start = True
            self.contains_end = False
            self.contains_line = False
            # event.canvas.setCursor(Qt.SizeBDiagCursor)
            event.canvas.send_event({"cursor":"ne-resize"})
        elif contains_end:
            self.contains_start = False
            self.contains_end = True
            self.contains_line = False
            # event.canvas.setCursor(Qt.SizeBDiagCursor)
            self.canvas.send_event({"cursor":"ne-resize"})
        elif contains_line:
            self.contains_start = False
            self.contains_end = False
            self.contains_line = True
            # event.canvas.setCursor(Qt.SizeAllCursor)
            self.canvas.send_event({"cursor":"move"})
        elif self.line_type == 'textarrow':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                self.contains_start = False
                self.contains_end = False
                self.contains_line = True
                # event.canvas.setCursor(Qt.SizeAllCursor)
                self.canvas.send_event({"cursor":"ne-resize"})
            else:
                return
        else:
            return

        self.start = (event.x, event.y)
        # 按下时获取两端端点的像素坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        self.press = True
        CDrawLine.lock = self
        self.adjust_order()

        # self.canvas.draw()
        self._update()

        if event.dblclick:
            return
            if self.line_type == 'textarrow':
                self.action_edit()
            else:
                self.action_prop()

            self.contains_line = False
            self.contains_start = False
            self.contains_end = False

            self.press = False
            CDrawLine.lock = None
            CDrawLine.motion_lock = None

    def on_motion(self, event):
        if not self.picked:
            return

        if not self.press:
            self.motion_status(event)
        else:
            if self.contains_start:
                # 先把像素坐标转换为端点的坐标系坐标
                pos_start = self.start_point.get_transform().inverted().transform((event.x, event.y))
                self.start_point.set_data([pos_start[0]], [pos_start[1]])
                # self.line.xy = (event.x, event.y)
                self.line._x = event.x
                self.line._y = event.y
                self.auxiliary_line.set_data([event.x, self.line.xy[0]], [event.y, self.line.xy[1]])
                # self._update()
            elif self.contains_end:
                # 先把像素坐标转换为端点的坐标系坐标
                pos_end = self.end_point.get_transform().inverted().transform((event.x, event.y))
                self.end_point.set_data([pos_end[0]], [pos_end[1]])
                # self.line._x = event.x
                # self.line._y = event.y
                self.line.xy = (event.x, event.y)
                self.auxiliary_line.set_data([self.line._x, event.x], [self.line._y, event.y])
                # self._update()
            elif self.contains_line:
                dx = event.x - self.start[0]
                dy = event.y - self.start[1]

                # 先把像素坐标转换为端点的坐标系坐标
                pos_start_pixels = (self.start_pos[0] + dx, self.start_pos[1] + dy)
                pos_end_pixels = (self.end_pos[0] + dx, self.end_pos[1] + dy)
                pos_start = self.start_point.get_transform().inverted().transform(pos_start_pixels)
                pos_end = self.end_point.get_transform().inverted().transform(pos_end_pixels)

                self.start_point.set_data([pos_start[0]], [pos_start[1]])
                self.end_point.set_data([pos_end[0]], [pos_end[1]])

                self.update_line_by_points_pos(pos_start_pixels, pos_end_pixels)

            self.calculate_text_position()

            self.outrange_cancel_fix()

            self._update()

    def on_release(self, event):
        if CDrawLine.lock is not self:
            return

        self.contains_line = False
        self.contains_start = False
        self.contains_end = False

        self.press = False
        CDrawLine.lock = None
        CDrawLine.motion_lock = None

        # self.background = None

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

        if self.background is not None:
            self.canvas.restore_region(self.background)

        self.update_line_by_points_pos()
        self.calculate_text_position()
        self.draw_self()

    def on_key_press(self, event):
        if not self.picked:
            return

        # 先把像素坐标转换为端点的坐标系坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        if event.key == 'left':
            pos_start_pixels = (self.start_pos[0] - 1, self.start_pos[1])
            pos_end_pixels = (self.end_pos[0] - 1, self.end_pos[1])
        elif event.key == 'right':
            pos_start_pixels = (self.start_pos[0] + 1, self.start_pos[1])
            pos_end_pixels = (self.end_pos[0] + 1, self.end_pos[1])
        elif event.key == 'up':
            pos_start_pixels = (self.start_pos[0], self.start_pos[1] + 1)
            pos_end_pixels = (self.end_pos[0], self.end_pos[1] + 1)
        elif event.key == 'down':
            pos_start_pixels = (self.start_pos[0], self.start_pos[1] - 1)
            pos_end_pixels = (self.end_pos[0], self.end_pos[1] - 1)
        elif event.key == 'delete':
            self.action_delete()
            return
        else:
            return

        pos_start = self.start_point.get_transform().inverted().transform(pos_start_pixels)
        pos_end = self.end_point.get_transform().inverted().transform(pos_end_pixels)

        self.start_point.set_data([pos_start[0]], [pos_start[1]])
        self.end_point.set_data([pos_end[0]], [pos_end[1]])

        self.update_line_by_points_pos(pos_start_pixels, pos_end_pixels)
        self.calculate_text_position()
        self.outrange_cancel_fix()
        self._update()

    def contains_self(self, event):
        if self.start_point == None:
            return False

        contains_start, attrd = self.start_point.contains(event)
        contains_end, attrd = self.end_point.contains(event)
        # contains_line, attrd = self.line.contains(event)
        contains_line, attrd = self.auxiliary_line.contains(event)

        if self.line_type == 'textarrow':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                return True

        return (contains_start or contains_end or contains_line)

    def motion_status(self, event):
        """
        鼠标移动时，鼠标状态的切换
        """
        if self.start_point == None or self.start_point == None or self.line == None:
            return False

        contains_start, attrd = self.start_point.contains(event)
        contains_end, attrd = self.end_point.contains(event)

        if contains_start or contains_end:
            # event.canvas.setCursor(Qt.SizeBDiagCursor)
            self.canvas.send_event({"cursor":"ne-resize"})
            return True

        # contains_line, attrd = self.line.contains(event)
        contains_line, attrd = self.auxiliary_line.contains(event)
        if contains_line:
            # event.canvas.setCursor(Qt.SizeAllCursor)
            self.canvas.send_event("cursor", cursor = "move")
            return True

        if self.line_type == 'textarrow':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                # event.canvas.setCursor(Qt.SizeAllCursor)
                return True

        # event.canvas.setCursor(Qt.ArrowCursor)
        self.canvas.send_event("cursor", cursor="default")
        return False

    def on_pick(self):
        """
        选中对象
        """
        if not mw_get_cfig().edit_mode:
            return

        if not self.picked:
            mw_clear_status()
            self.pick_self()
            cfig = mw_get_cfig(self.fig)
            if "Line" in cfig.prop_objs and cfig.prop_objs["Line"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Line")
            else:
                # 处理没有坐标轴的情况
                if len(self.fig.axes) > 0:
                    cax = mw_get_cax(self.fig.gca())
                else:
                    cax = None

                props = get_property(cfig, cax, self, "Line")
                self.fig.canvas.send_event("property_init", props=props, current_prop="Line", font_list = get_font_lst())

    def pick_self(self, pick_only = False):
        """选中状态"""
        self.start_point.set_visible(True)
        self.end_point.set_visible(True)
        self.fig.canvas.draw_idle()
        self.picked = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        self.start_point.set_visible(False)
        self.end_point.set_visible(False)
        self.fig.canvas.draw_idle()
        self.picked = False

    def context_menu(self):
        return

    def action_delete(self):
        self.disconnect()
        mw_get_cfig().draw_lines.remove(self)
        mw_get_cfig().current_objs.clear()
        self.line.remove()
        self.auxiliary_line.remove()
        self.start_point.remove()
        self.end_point.remove()
        if self.line_type == "textarrow":
            self.text.remove()

        # 在删除图形的同时删除对应的属性面板tab页，并切换到Figure的属性面板tab页
        self.fig.canvas.send_event("property_remove", current_prop="Figure",del_prop="Line")

        # self.canvas.setCursor(Qt.ArrowCursor)
        self.canvas.send_event({"cursor":"default"})
        mw_get_cfig().pick_self()

    def action_fix_to_axes(self):
        self.fix_ax_start = None
        self.fix_ax_end = None
        for cax in mw_get_cfig().axs:
            range = cax.ax.get_window_extent()
            if (self.start_pos[0] > range.x0
                and self.start_pos[0] < range.x1
                and self.start_pos[1] > range.y0
                and self.start_pos[1] < range.y1):
                self.fix_ax_start = cax.ax
            if (self.end_pos[0] > range.x0
                and self.end_pos[0] < range.x1
                and self.end_pos[1] > range.y0
                and self.end_pos[1] < range.y1):
                self.fix_ax_end = cax.ax

        if self.fix_ax_start != None:
            new_pos_start = self.fix_ax_start.transData.inverted().transform((self.start_pos[0], self.start_pos[1]))
            self.start_point.set_transform(self.fix_ax_start.transData)
            self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])
            self.start_point.set_markerfacecolor("#000000")
            self.start_point.set_markeredgecolor("#ffff00")
            self.start_point.set_markersize(7)

        if self.fix_ax_end != None:
            new_pos_end = self.fix_ax_end.transData.inverted().transform((self.end_pos[0], self.end_pos[1]))
            self.end_point.set_transform(self.fix_ax_end.transData)
            self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])
            self.end_point.set_markerfacecolor("#000000")
            self.end_point.set_markeredgecolor("#ffff00")
            self.end_point.set_markersize(7)

        self.canvas.draw_idle()

    def action_fix_cancel(self):
        # if self.fix_ax_start != None:
        #     new_pos_start = self.start_point.get_transform().transform((self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        #     self.start_point.set_transform(self.fig.get_transform())
        #     self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])
        #     self.start_point.set_markerfacecolor("#c0e7ff")
        #     self.start_point.set_markeredgecolor("#005a96")
        #     self.start_point.set_markersize(6)

        #     if self.units == 'normalized':
        #         new_pos_start = self.fig.transFigure.inverted().transform(
        #             (self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        #         self.start_point.set_transform(self.fig.transFigure)
        #         self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])

        # if self.fix_ax_end != None:
        #     new_pos_end = self.end_point.get_transform().transform((self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
        #     self.end_point.set_transform(self.fig.get_transform())
        #     self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])
        #     self.end_point.set_markerfacecolor("#c0e7ff")
        #     self.end_point.set_markeredgecolor("#005a96")
        #     self.end_point.set_markersize(6)

        #     if self.units == 'normalized':
        #         new_pos_end = self.fig.transFigure.inverted().transform(
        #             (self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
        #         self.end_point.set_transform(self.fig.transFigure)
        #         self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])

        self.fix_cancel_point(self.start_point)
        self.fix_cancel_point(self.end_point)

        self.fix_ax_start = None
        self.fix_ax_end = None
        self.canvas.draw_idle()

    def fix_cancel_point(self, point):
        if point == self.start_point:
            fix_ax = self.fix_ax_start
        else:
            fix_ax = self.fix_ax_end

        if fix_ax != None:
            new_pos_start = point.get_transform().transform((point.get_xdata()[0], point.get_ydata()[0]))
            point.set_transform(self.fig.get_transform())
            point.set_data([new_pos_start[0]], [new_pos_start[1]])
            point.set_markerfacecolor("#c0e7ff")
            point.set_markeredgecolor("#005a96")
            point.set_markersize(6)

            if self.units == 'normalized':
                new_pos_start = self.fig.transFigure.inverted().transform(
                    (point.get_xdata()[0], point.get_ydata()[0]))
                point.set_transform(self.fig.transFigure)
                point.set_data([new_pos_start[0]], [new_pos_start[1]])

    def action_color(self):
        line_color = self.line.arrow_patch.get_edgecolor()
        dlg_color = DlgColor(color_to_qcolor(line_color))
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            if self.linestyle in self.dict_style['无']:
                select_color = mcolors.to_rgba(select_color, 0.0)
            self.line.arrow_patch.set_color(select_color)
            if self.line_type == 'textarrow':
                self.text.set_color(select_color)
            self.fig.canvas.draw_idle()

    def action_linewidth(self):
        action = QAction()
        sender = action.sender()
        linewidth = float(sender.text())
        self.line.arrow_patch.set_linewidth(linewidth)
        self.canvas.draw_idle()

    def action_linestyle(self):
        action = QAction()
        sender = action.sender()
        style = self.dict_style[sender.text()][0]
        self.linestyle = style
        if style == 'None':
            current_color = color_to_qcolor(self.line.arrow_patch.get_edgecolor())
            self.line.arrow_patch.set_edgecolor(mcolors.to_rgba(current_color.name(), 0.0))
        else:
            current_color = color_to_qcolor(self.line.arrow_patch.get_edgecolor())
            self.line.arrow_patch.set_edgecolor(mcolors.to_rgba(current_color.name(), 1.0))
            self.line.arrow_patch.set_linestyle(style)

        self.canvas.draw_idle()

    def action_prop(self):
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.line]])
        prop_dlg.set_current_index(1)
        prop_dlg.connect()
        prop_dlg.exec_()

    def action_reverse(self):
        start_pos = self.start_point.get_transform().transform(
            (self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        end_pos = self.end_point.get_transform().transform(
            (self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        self.start_pos = self.start_point.get_transform().inverted().transform(end_pos)
        self.end_pos = self.end_point.get_transform().inverted().transform(start_pos)

        self.start_point.set_data([self.start_pos[0]], [self.start_pos[1]])
        self.end_point.set_data([self.end_pos[0]], [self.end_pos[1]])

        self.update_line_by_points_pos()
        self.calculate_text_position()
        self.outrange_cancel_fix()
        self._update()
        # old_style = self.line.arrow_patch.get_arrowstyle()
        # old_style = self.line.arrowprops['arrowstyle']
        # if old_style == '->':
        #     new_style = '<-'
        # else:
        #     new_style = '->'
        # self.line.arrowprops['arrowstyle'] = new_style
        # self.line.arrow_patch.set_arrowstyle(new_style)
        # self.canvas.draw_idle()

    def action_edit(self):
        self.text_edit=DlgEditGraphicsText(self, self.text)
        self.text_edit.exec()

    def action_background_color(self):
        '''字体背景颜色设置动作'''
        background_color='none'
        if not self.text._bbox_patch is None:
            tuple_background_color = self.text._bbox_patch.get_facecolor()
            background_color = color_to_qcolor(tuple_background_color)
            if tuple_background_color[3]==0.0:
                background_color='none'
        dlg_color = DlgColor(background_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            if self.text._bbox_patch is None:
                self.text.set_bbox(dict(facecolor=select_color, edgecolor = 'none'))
            else:
                self.text._bbox_patch.update(dict(facecolor=select_color))
            self.text._update_clip_properties()

        self.text.figure.canvas.draw_idle()

    def action_font(self):
        '''设置字体动作'''
        self.font=DlgTitlebaseFont(self,self.text)
        self.font.exec()

    def calculate_text_position(self, start_pos = None, end_pos = None):
        """
        根据线两端端点的坐标更新text的位置
        ------------------------------
        start_pos : 起始点坐标（像素）
        end_pos : 终止点坐标（像素）
        """
        if self.line_type != 'textarrow':
            return

        # 获取文本的位置大小
        if start_pos == None:
            start_pos = self.start_point.get_transform().transform((self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        if end_pos == None:
            end_pos = self.end_point.get_transform().transform((self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        text_pos = (self.text.get_window_extent().x0, self.text.get_window_extent().y0,
                    self.text.get_window_extent().x1, self.text.get_window_extent().y1)
        text_width = text_pos[2] - text_pos[0]
        text_height = text_pos[3] - text_pos[1]
        # text_pos = self.text.get_position()

        # 根据线起止点的相对位置调整文本的位置，共八个方位
        cur_tan = (end_pos[1] - start_pos[1]) / (end_pos[0] - start_pos[0])
        cur_deg = np.rad2deg(np.arctan(cur_tan))
        if cur_deg > -30 and cur_deg < 30 and (end_pos[0] - start_pos[0]) < 0:
            self.text._x = start_pos[0]
            self.text._y = start_pos[1] - text_height/2
        elif cur_deg > 30 and cur_deg < 60 and (end_pos[0] - start_pos[0]) < 0:
            self.text._x = start_pos[0]
            self.text._y = start_pos[1]
        elif (cur_deg > 60 and (end_pos[0] - start_pos[0]) < 0) or (cur_deg < -60 and (end_pos[0] - start_pos[0]) > 0):
            self.text._x = start_pos[0] - text_width/2
            self.text._y = start_pos[1]
        elif cur_deg > -60 and cur_deg < -30 and (end_pos[0] - start_pos[0]) > 0:
            self.text._x = start_pos[0] - text_width
            self.text._y = start_pos[1]
        elif cur_deg > -30 and cur_deg < 30 and (end_pos[0] - start_pos[0]) > 0:
            self.text._x = start_pos[0] - text_width
            self.text._y = start_pos[1] - text_height/2
        elif cur_deg > 30 and cur_deg < 60 and (end_pos[0] - start_pos[0]) > 0:
            self.text._x = start_pos[0] - text_width
            self.text._y = start_pos[1] - text_height
        elif (cur_deg > 60 and (end_pos[0] - start_pos[0]) > 0) or (cur_deg < -60 and (end_pos[0] - start_pos[0]) < 0):
            self.text._x = start_pos[0] - text_width/2
            self.text._y = start_pos[1] - text_height
        elif cur_deg > -60 and cur_deg < -30 and (end_pos[0] - start_pos[0]) < 0:
            self.text._x = start_pos[0]
            self.text._y = start_pos[1] - text_height

    def adjust_order(self):
        for dline in mw_get_cfig().draw_lines:
            if dline == self:
                mw_get_cfig().draw_lines.remove(dline)
                mw_get_cfig().draw_lines.append(self)
                break

    def set_transform_normalized(self, transform):
        if self.fix_ax_start == None:
            new_pos_start = transform.inverted().transform(
                (self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
            self.start_point.set_transform(transform)
            self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])

        if self.fix_ax_end == None:
            new_pos_end = transform.inverted().transform(
                (self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
            self.end_point.set_transform(transform)
            self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])

    def set_transform_pixels(self, transform):
        if self.fix_ax_start == None:
            if transform == self.start_point.get_transform():
                return

            new_pos_start = self.fig.transFigure.transform(
                (self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
            self.start_point.set_transform(transform)
            self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])

        if self.fix_ax_end == None:
            if transform == self.end_point.get_transform():
                return

            new_pos_end = self.fig.transFigure.transform(
                (self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
            self.end_point.set_transform(transform)
            self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])

    def outrange_cancel_fix(self):
        if self.fix_ax_start != None:
            inrange = self.detect_point_out_of_range(self.start_point)
            if not inrange:
                self.fix_cancel_point(self.start_point)
                self.fix_ax_start = None
        if self.fix_ax_end != None:
            inrange = self.detect_point_out_of_range(self.end_point)
            if not inrange:
                self.fix_cancel_point(self.end_point)
                self.fix_ax_end = None

    def detect_point_out_of_range(self, point, pos = None):
        if pos == None:
            pos = point.get_transform().transform((
                point.get_xdata()[0], point.get_ydata()[0]))

        for cax in mw_get_cfig().axs:
            range = cax.ax.get_window_extent()
            if (pos[0] > range.x0
                and pos[0] < range.x1
                and pos[1] > range.y0
                and pos[1] < range.y1):
                return True

        return False

    def draw_self(self):
        self.fig.draw_artist(self.line)
        self.fig.draw_artist(self.auxiliary_line)
        if self.line_type == 'textarrow':
            self.fig.draw_artist(self.text)
        self.fig.draw_artist(self.start_point)
        self.fig.draw_artist(self.end_point)

    def _update(self):
        if not self.picked:
            return

        self.fig.canvas.draw_idle()
        # update_all(self.fig)

    # 颜色
    def get_color(self):
        return color_to_hex(self.line.arrow_patch.get_edgecolor())

    def set_color(self, color):
        if self.linestyle == 'none':
            color = mcolors.to_rgba(color, 0.0)
        self.line.arrow_patch.set_color(color)
        self.canvas.draw_idle()

    def get_linestyle(self):
        return self.linestyle

    def set_linestyle(self, linestyle):
        invalid = True
        for key, value in self.dict_style.items():
            if linestyle in value:
                invalid = False
                break
        if invalid:
            return

        self.linestyle = linestyle
        # if linestyle in self.dict_style['无']:
        #     current_color = color_to_qcolor(self.line.arrow_patch.get_edgecolor())
        #     self.line.arrow_patch.set_edgecolor(mcolors.to_rgba(current_color.name(), 0.0))
        # else:
        #     current_color = color_to_qcolor(self.line.arrow_patch.get_edgecolor())
        #     self.line.arrow_patch.set_edgecolor(mcolors.to_rgba(current_color.name(), 1.0))
        self.line.arrow_patch.set_linestyle(linestyle)
        self.fig.canvas.draw_idle()

    def get_linewidth(self):
        return self.line.arrow_patch.get_linewidth()

    def set_linewidth(self, linewidth):
        try:
            linewidth=float(linewidth)
        except Exception as e:
            return

        if linewidth <= 0:
            return

        self.line.arrow_patch.set_linewidth(linewidth)
        self.fig.canvas.draw_idle()

    # 位置
    def get_x(self):
        start_pos,end_pos = self.get_position_common()
        x = str(round(start_pos[0],4)) + ',' + str(round(end_pos[0],4))
        return x

    def set_x(self, x):
        # 传入的新x坐标
        new_x=(
            float(x[0:x.index(',')])
            ,float(x[x.index(',')+1:])
            )
        # 未修改的y坐标
        new_y=(
            float(self.y[0:self.y.index(',')])
            ,float(self.y[self.y.index(',')+1:])
        )
        pos_start = (new_x[0],new_y[0])
        pos_end = (new_x[1],new_y[1])
        # 坐标更新
        self.start_point.set_data([pos_start[0]], [pos_start[1]])
        self.end_point.set_data([pos_end[0]], [pos_end[1]])
        self.update_line_by_points_pos()
        self._update()
        # 更新pos x y变量
        self.pos = (str(round(pos_start[0],4)) + ','
                + str(round(pos_start[1],4)) + ','
                + str(round(pos_end[0] - pos_start[0],4)) + ','
                + str(round(pos_end[1] - pos_start[1],4)))
        self.x= (str(round(pos_start[0],4)) + ',' + str(round(pos_end[0],4)))
        self.y= (str(round(pos_start[1],4)) + ',' + str(round(pos_end[1],4)))

    def get_y(self):
        start_pos,end_pos = self.get_position_common()
        y = str(round(start_pos[1],4)) + ',' + str(round(end_pos[1],4))
        return y

    def set_y(self, y):
        # 未修改的x坐标
        new_x=(
            float(self.x[0:self.x.index(',')])
            ,float(self.x[self.x.index(',')+1:])
            )
        # 传入的新y坐标
        new_y=(
            float(y[0:y.index(',')])
            ,float(y[y.index(',')+1:])
        )
        pos_start = (new_x[0],new_y[0])
        pos_end = (new_x[1],new_y[1])
        # 坐标更新
        self.start_point.set_data([pos_start[0]], [pos_start[1]])
        self.end_point.set_data([pos_end[0]], [pos_end[1]])
        self.update_line_by_points_pos()
        self._update()
        # 更新pos x y变量
        self.pos = (str(round(pos_start[0],4)) + ','
                + str(round(pos_start[1],4)) + ','
                + str(round(pos_end[0] - pos_start[0],4)) + ','
                + str(round(pos_end[1] - pos_start[1],4)))
        self.x= (str(round(pos_start[0],4)) + ',' + str(round(pos_end[0],4)))
        self.y= (str(round(pos_start[1],4)) + ',' + str(round(pos_end[1],4)))

    def pixels_to_normalized(self,pos):
        return tuple(self.fig.transFigure.inverted().transform(pos))

    def get_position_common(self):
        # 获取两端点的像素坐标
        start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
        # 进行坐标转换
        start_pos = self.pixels_to_normalized(start_pos)
        end_pos = self.pixels_to_normalized(end_pos)
        return start_pos,end_pos

    def get_position(self):
        start_pos,end_pos = self.get_position_common()
        # 宽  单机版宽与高存在负数，因此此处不取绝对值
        width = end_pos[0] - start_pos[0]
        # 高
        height = end_pos[1] - start_pos[1]
        # 最终展现 x y width height
        position = (round(start_pos[0],4),round(start_pos[1],4),round(width,4),round(height,4))
        return position

    # 将前端传回的字符串坐标数据进行转换
    def str_to_data(self,position):
        x0, y0, width, height = position.split(',')
        # position为[x0, y0, width, height]形式的字符串，因此需对x0与height做处理
        x0 = x0[1:]
        height=height[:-1]
        self.pos = (float(x0), float(y0), float(width) + float(x0), float(height) + float(y0))

    def set_position(self, position):
        # 字符串坐标数据转换
        self.str_to_data(position)
        # 新坐标
        new_pos_start = (self.pos[0], self.pos[1])
        new_pos_end = (self.pos[2], self.pos[3])
        # 坐标转换
        new_pos_start_pixels = tuple(self.fig.transFigure.transform((self.pos[0], self.pos[1])))
        new_pos_end_pixels = tuple(self.fig.transFigure.transform((self.pos[2], self.pos[3])))
        if self.fix_ax_start != None:
            new_pos_start = self.fix_ax_start.transData.inverted().transform(new_pos_start_pixels)

        if self.fix_ax_end != None:
            new_pos_end = self.fix_ax_end.transData.inverted().transform(new_pos_end_pixels)
        # 坐标更新
        self.start_point.set_data([new_pos_start[0]], [new_pos_start[1]])
        self.end_point.set_data([new_pos_end[0]], [new_pos_end[1]])
        self.update_line_by_points_pos()
        self._update()

    def get_units(self):
        return

    def set_units(self, units):
        return

    def delete_self(self):
        self.action_delete()

class CDLine(CDrawLine):
    def __init__(self, fig, line, start_point, end_point, auxiliary_line, line_type):
        super().__init__(fig, line, start_point, end_point, auxiliary_line, line_type)

    # 右键菜单
    def context_menu(self):

        # 右键时先获取两端端点的像素坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        menu_list = []

        # 删除
        menu_list.append({"value": "line_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "line_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "line_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "linewidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "linestyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextBox"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    # 接受前端返回数据，并进行相应操作
    def set_prop(self,name,value):
        # name = name.lower()
        name = name.lower()
        
        if name == "line_delete":
            self.action_delete()
        elif name == "line_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "line_fix_cancel":
            self.action_fix_cancel()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["color", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())
                    
        return None
            
    def get_all_props(self):
        prop_name = {"ColorAndStyle":["Color", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name
        
        return props
    
    def get_colorandstyle_props(self):
        prop_names = ["Color", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

class CDArrow(CDrawLine):
    def __init__(self, fig, line, start_point, end_point, auxiliary_line, line_type):
        super().__init__(fig, line, start_point, end_point, auxiliary_line, line_type)

    # 右键菜单
    def context_menu(self):
        # 右键时先获取两端端点的像素坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
        
        menu_list = []

        # 删除
        menu_list.append({"value": "arrow_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "arrow_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "arrow_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
         # 反向
        menu_list.append({"value": "arrow_reverse", "label": "反向", "children": [], "default_value": ""})

        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "LineWidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "LineStyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextBox"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    # 接受前端返回数据，并进行相应操作
    def set_prop(self,name,value):
        # name = name.lower()
        name = name.lower()
        
        if name == "arrow_delete":
            self.action_delete()
        elif name == "arrow_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "arrow_fix_cancel":
            self.action_fix_cancel()
        elif name == "arrow_reverse":
            self.action_reverse()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["color", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())
                    
        return None
            
    def get_all_props(self):
        prop_name = {"ColorAndStyle":["Color", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name

        return props
    
    def get_colorandstyle_props(self):
        prop_names = ["Color", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

class CDTextArrow(CDrawLine):
    def __init__(self, fig, line, start_point, end_point, auxiliary_line, line_type):
        super().__init__(fig, line, start_point, end_point, auxiliary_line, line_type)
        # 处理规则：当用户在属性面板上修改过textcolor,则修改箭头颜色时，不会同步修改文本颜色
        self.textcolor_change = False

    def context_menu(self):
        
        # 右键时先获取两端端点的像素坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))

        menu_list = []

        # 删除
        menu_list.append({"value": "textarrow_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "textarrow_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "textarrow_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 反向
        menu_list.append({"value": "textarrow_reverse", "label": "反向", "children": [], "default_value": ""})
        
        # 编辑文本
        # 接收当前文本作为默认值
        text = self.get_string()
        menu_list.append({"value": "text_edit", "label": "编辑文本", "children": [], "default_value": text})
        
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 文本背景颜色
        # textbackgroundcolor = self.get_textbackgroundcolor()
        # menu_list.append({"value": "textbackgroundcolor", "label": "文本背景颜色", "children": [], "default_value": textbackgroundcolor})
        
        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "linewidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "linestyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextArrow"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    # 接受前端返回数据，并进行相应操作
    def set_prop(self,name,value):
        name = name.lower()
        if name == "textarrow_delete":
            self.action_delete()
        elif name == "textarrow_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "textarrow_fix_cancel":
            self.action_fix_cancel()
        elif name == "textarrow_reverse":
            self.action_reverse()
        elif name == "text_edit":
            self.set_string(value)
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["text_edit"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "Text", value = self.get_text_props())
        elif name in ["color"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "Text", value = self.get_text_props())
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_colorandstyle_props()) 
        elif name in ["linestyle","linewidth"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())    

        return None
    
    def get_all_props(self):
        prop_name = {"Text":["String", "TextRotation", "TextColor", "TextEdgeColor","TextBackgroundColor", "TextLineWidth","TextMargin"],
                     "Fonts":["FontName", "FontAngle", "FontWeight", "FontSize"],
                     "ColorAndStyle":["Color", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name
        
        return props

    def set_color(self, color):
        if not self.textcolor_change:
            self.text.set_color(color)
        if self.linestyle == 'none':
            color = mcolors.to_rgba(color, 0.0)
        self.line.arrow_patch.set_color(color)
        self.canvas.draw_idle()

    def get_text_props(self):
        prop_names = ["String", "TextRotation", "TextColor", "TextEdgeColor","TextBackgroundColor", "TextLineWidth","TextMargin"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

    def get_colorandstyle_props(self):
        prop_names = ["Color", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

    # 文本
    def get_string(self):
        return self.text.get_text()

    def set_string(self,string):
        self.text.set_text(string)
        self.canvas.draw_idle()

    def get_textrotation(self):
        return self.text.get_rotation()

    def set_textrotation(self, rotation):
        self.text.set_rotation(rotation)
        self.canvas.draw_idle()

    def get_textcolor(self):
        return color_to_hex(mcolors.to_rgb(self.text.get_color()))

    def set_textcolor(self, text_color):
        if text_color == self.get_textcolor():
            return
        self.textcolor_change = True
        self.text.set_color(text_color)
        self.canvas.draw_idle()

    def get_textedgecolor(self):
        edge_color = 'none'
        if self.text._bbox_patch is not None:
            tuple_edge_color = self.text._bbox_patch.get_edgecolor()
            edge_color = tuple_edge_color
            if tuple_edge_color[3]==0.0:
                edge_color='none'
        return color_to_hex(edge_color)

    def set_textedgecolor(self, text_edgecolor):
        if self.text._bbox_patch is None:
            self.text.set_bbox(dict(facecolor='none', edgecolor=text_edgecolor))
        else:
            self.text._bbox_patch.update(dict(edgecolor=text_edgecolor))
        self.text._update_clip_properties()
        self.canvas.draw_idle()

    def get_textbackgroundcolor(self):
        face_color = 'none'
        if self.text._bbox_patch is not None:
            tuple_face_color = self.text._bbox_patch.get_facecolor()
            face_color = tuple_face_color
            if tuple_face_color[3]==0.0:
                face_color='none'
        return color_to_hex(face_color)

    def set_textbackgroundcolor(self, text_backgroundcolor):
        if self.text._bbox_patch is None:
            self.text.set_bbox(dict(facecolor=text_backgroundcolor, edgecolor = 'none'))
        else:
            self.text._bbox_patch.update(dict(facecolor=text_backgroundcolor))
        self.text._update_clip_properties()
        self.canvas.draw_idle()

    def get_textlinewidth(self):
        return self.text._bbox_patch.get_linewidth()

    def set_textlinewidth(self, text_linewidth):
        self.text._bbox_patch.set_linewidth(text_linewidth)
        self.canvas.draw_idle()

    def get_textmargin(self):
        return self.text.get_bbox_patch().get_boxstyle().pad

    def set_textmargin(self, text_margin):
        try:
            text_margin=float(text_margin)
        except Exception as e:
            return
        self.text.get_bbox_patch().set_boxstyle("square",pad=text_margin)
        self.canvas.draw_idle()

    # 字体
    def get_fontsize(self):
        return self.text.get_fontsize()

    def set_fontsize(self, fontsize):
        fontdict={'size': fontsize}
        self.text.update(fontdict)
        self.canvas.draw_idle()

    def get_fontangle(self):
        if self.text.get_fontstyle() == 'normal':
            return False
        else:
            return True 

    def set_fontangle(self, fontangle):
        if fontangle == 'True':
            fontangle = 'italic'
            fontdict={'style': fontangle}
            self.text.update(fontdict)
            self.canvas.draw_idle()
        else:
            fontangle = 'normal'
            fontdict={'style': fontangle}
            self.text.update(fontdict)
            self.canvas.draw_idle()

    def get_fontname(self):
        return self.text.get_fontname()

    def set_fontname(self, fontname):
        fontname = get_real_name(fontname)
        fontdict={'family': fontname}
        self.text.update(fontdict)
        self.canvas.draw_idle()

    def get_fontweight(self):
        if self.text.get_fontweight() == 'normal':
            return False
        else:
            return True 

    def set_fontweight(self, fontweight):
        if fontweight == 'True':
            fontweight = 'bold'
            fontdict={'weight': fontweight}
            self.text.update(fontdict)
            self.canvas.draw_idle()
        else:
            fontweight = 'normal'
            fontdict={'weight': fontweight}
            self.text.update(fontdict)
            self.canvas.draw_idle()

class CDDoubleArrow(CDrawLine):
    def __init__(self, fig, line, start_point, end_point, auxiliary_line, line_type):
        super().__init__(fig, line, start_point, end_point, auxiliary_line, line_type)

    # 右键菜单
    def context_menu(self):

        # 右键时先获取两端端点的像素坐标
        self.start_pos = self.start_point.get_transform().transform((
            self.start_point.get_xdata()[0], self.start_point.get_ydata()[0]))
        self.end_pos = self.end_point.get_transform().transform((
            self.end_point.get_xdata()[0], self.end_point.get_ydata()[0]))
        
        menu_list = []

        # 删除
        menu_list.append({"value": "doublearrow_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "doublearrow_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "doublearrow_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "LineWidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "LineStyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextBox"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    # 接受前端返回数据，并进行相应操作
    def set_prop(self,name,value):
        # name = name.lower()
        name = name.lower()
        
        if name == "doublearrow_delete":
            self.action_delete()
        elif name == "doublearrow_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "doublearrow_fix_cancel":
            self.action_fix_cancel()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["color", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())
                    
        return None
            
    def get_all_props(self):
        prop_name = {"ColorAndStyle":["Color", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name

        return props
    
    def get_colorandstyle_props(self):
        prop_names = ["Color", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle


class DrawRect(object):
    lock = None
    motion_lock = None

    def __init__(self, fig, graphics_type = 'rectangle'):
        """
        初始化函数

        arg:
            fig:    图窗对象
        """
        self.fig = fig
        self.canvas = self.fig.canvas
        self.press = False
        self.start = None
        self.picked = True
        self.background = None

        self.graphics = None
        self.start_point = None
        self.end_point = None

        self.move = False

        self.graphics_type = graphics_type

        # self.canvas.setCursor(Qt.CrossCursor)
        # self.canvas.send_event({"cursor":"crosshair"})
        # self.canvas.set_cursor("crosshair")
        self.canvas.send_event('cursor', cursor="crosshair")

    def create_pick_state(self):
        x = self.start[0]
        y = self.start[1]
        self.side_points = []
        self.angle_points = []
        for i in range (0, 4):
            side_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
            side_point.set_animated(True)
            side_point.set_transform(self.fig.get_transform())
            self.fig.add_artist(side_point)
            self.side_points.append(side_point)

            angle_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
            angle_point.set_animated(True)
            angle_point.set_transform(self.fig.get_transform())
            self.fig.add_artist(angle_point)
            self.angle_points.append(angle_point)

    # 绘制图形的事件函数
    def connect_draw(self):
        """连接事件信号槽"""
        self.cid_draw_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_draw_press)
        self.cid_draw_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_draw_release)
        self.cid_draw_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_draw_motion)

    def disconnect_draw(self):
        """断开信号槽连接"""
        self.fig.canvas.mpl_disconnect(self.cid_draw_press)
        self.fig.canvas.mpl_disconnect(self.cid_draw_release)
        self.fig.canvas.mpl_disconnect(self.cid_draw_motion)

    def on_draw_press(self, event):
        """鼠标按下获取起始坐标"""
        if self.press:
            return

        if not mw_get_cfig().edit_mode:
            return

        self.press = True
        self.start = (event.x, event.y)

        self.rect = Rectangle(self.start, 0, 0,
                        edgecolor = 'black',
                        facecolor = 'none',
                        fill=True,
                        lw=1,
                        ls='-')

        self.rect.set_transform(self.fig.get_transform())
        self.rect.set_animated(True)
        self.rect.set_in_layout(False)
        self.fig.add_artist(self.rect)

        self.create_pick_state()

        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self._update()

    def on_draw_motion(self, event):
        """连接事件信号槽"""
        if not self.press:
            return

        # self.line._x = event.x
        # self.line._y = event.y
        # self.line.xy = (event.x, event.y)
        # self.end_point.set_data([event.x], [event.y])

        (xpress, ypress) = self.start
        dx = event.x - xpress
        dy = event.y - ypress

        self.rect._height = dy
        self.rect._width = dx

        self.side_points[0].set_data([xpress], [ypress + dy/2])
        self.side_points[1].set_data([xpress + dx/2], [ypress + dy])
        self.side_points[2].set_data([xpress + dx], [ypress + dy/2])
        self.side_points[3].set_data([xpress + dx/2], [ypress])

        self.angle_points[0].set_data([xpress], [ypress])
        self.angle_points[1].set_data([xpress], [ypress + dy])
        self.angle_points[2].set_data([xpress + dx], [ypress + dy])
        self.angle_points[3].set_data([xpress + dx], [ypress])

        # self.rect.set_height(dy)
        # self.rect.set_width(dx)

        self.move = True
        self._update()

    def on_draw_release(self, event):
        """连接事件信号槽"""
        if not self.press:
            return

        if not self.move:
            end_pos = (self.start[0] + 90, self.start[1] + 30)
            (xpress, ypress) = self.start
            dx = end_pos[0] - xpress
            dy = end_pos[1] - ypress
            self.rect._height = dy
            self.rect._width = dx

            self.side_points[0].set_data([xpress], [ypress + dy/2])
            self.side_points[1].set_data([xpress + dx/2], [ypress + dy])
            self.side_points[2].set_data([xpress + dx], [ypress + dy/2])
            self.side_points[3].set_data([xpress + dx/2], [ypress])

            self.angle_points[0].set_data([xpress], [ypress])
            self.angle_points[1].set_data([xpress], [ypress + dy])
            self.angle_points[2].set_data([xpress + dx], [ypress + dy])
            self.angle_points[3].set_data([xpress + dx], [ypress])
            self._update()

        self.press_point = None
        self.press = False

        self.disconnect_draw()
        self.fig.canvas.send_event("toolbar_update", action="Draw", active=False)

        update_draw_button_status(self.fig, '')

        if self.graphics_type == 'rectangle':
            drect = CDRectangle(self.fig, self.rect, self.side_points, self.angle_points, self.graphics_type)
        else:
            drect = CDTextBox(self.fig, self.rect, self.side_points, self.angle_points, self.graphics_type)

        drect.init_points()
        drect.connect()
        mw_get_cfig().lst_draw_graphics.append(drect)
        mw_get_cfig().current_objs.append(drect)
        self.fig.canvas.draw_idle()

    def draw_self(self):
        self.fig.draw_artist(self.rect)
        for i in range(0, 4):
            self.fig.draw_artist(self.side_points[i])
            self.fig.draw_artist(self.angle_points[i])

    def _update(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)

        # for dline in mw_get_cfig().draw_lines:
        #     dline.draw_self()

        self.draw_self()

        self.canvas.blit(self.fig.bbox)

class DrawEllipse(object):
    lock = None
    motion_lock = None

    def __init__(self, fig, graphics_type = 'ellipse'):
        """
        初始化函数

        arg:
            fig:    图窗对象
        """
        self.fig = fig
        self.canvas = self.fig.canvas
        self.press = False
        self.start = None
        self.picked = True
        self.background = None

        self.graphics = None
        self.start_point = None
        self.end_point = None

        self.move = False

        self.graphics_type = graphics_type

        # self.canvas.setCursor(Qt.CrossCursor)
        self.canvas.send_event({"cursor":"crosshair"})

    def create_pick_state(self):
        x = self.start[0]
        y = self.start[1]
        self.side_points = []
        self.angle_points = []
        for i in range (0, 4):
            side_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
            side_point.set_animated(True)
            side_point.set_transform(self.fig.get_transform())
            self.fig.add_artist(side_point)
            self.side_points.append(side_point)

            angle_point = Line2D([x], [y], marker = 's', clip_on = False, linestyle = 'none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
            angle_point.set_animated(True)
            angle_point.set_transform(self.fig.get_transform())
            self.fig.add_artist(angle_point)
            self.angle_points.append(angle_point)

    # 绘制图形的事件函数
    def connect_draw(self):
        """连接事件信号槽"""
        self.cid_draw_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_draw_press)
        self.cid_draw_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_draw_release)
        self.cid_draw_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_draw_motion)

    def disconnect_draw(self):
        """断开信号槽连接"""
        self.fig.canvas.mpl_disconnect(self.cid_draw_press)
        self.fig.canvas.mpl_disconnect(self.cid_draw_release)
        self.fig.canvas.mpl_disconnect(self.cid_draw_motion)

    def on_draw_press(self, event):
        """鼠标按下获取起始坐标"""
        if self.press:
            return

        if not mw_get_cfig().edit_mode:
            return

        self.press = True
        self.start = (event.x, event.y)

        self.ellipse = Ellipse(self.start, 0, 0,
                        edgecolor = 'black',
                        facecolor = 'none',
                        fill=True,
                        lw=1,
                        ls='-')

        self.ellipse.set_transform(self.fig.get_transform())
        self.ellipse.set_animated(True)
        self.ellipse.set_in_layout(False)
        self.fig.add_artist(self.ellipse)

        self.create_pick_state()

        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self._update()

    def on_draw_motion(self, event):
        """连接事件信号槽"""
        if not self.press:
            return

        (xpress, ypress) = self.start
        dx = event.x - xpress
        dy = event.y - ypress

        self.ellipse.set_center((xpress + dx/2, ypress + dy/2))
        self.ellipse.set_width(dx)
        self.ellipse.set_height(dy)

        self.side_points[0].set_data([xpress], [ypress + dy/2])
        self.side_points[1].set_data([xpress + dx/2], [ypress + dy])
        self.side_points[2].set_data([xpress + dx], [ypress + dy/2])
        self.side_points[3].set_data([xpress + dx/2], [ypress])

        self.angle_points[0].set_data([xpress], [ypress])
        self.angle_points[1].set_data([xpress], [ypress + dy])
        self.angle_points[2].set_data([xpress + dx], [ypress + dy])
        self.angle_points[3].set_data([xpress + dx], [ypress])

        self.move = True
        self._update()

    def on_draw_release(self, event):
        """连接事件信号槽"""
        if not self.press:
            return

        if not self.move:
            end_pos = (self.start[0] + 90, self.start[1] + 30)
            (xpress, ypress) = self.start
            dx = end_pos[0] - xpress
            dy = end_pos[1] - ypress
            self.ellipse.set_center((xpress + dx/2, ypress + dy/2))
            self.ellipse.set_width(dx)
            self.ellipse.set_height(dy)

            self.side_points[0].set_data([xpress], [ypress + dy/2])
            self.side_points[1].set_data([xpress + dx/2], [ypress + dy])
            self.side_points[2].set_data([xpress + dx], [ypress + dy/2])
            self.side_points[3].set_data([xpress + dx/2], [ypress])

            self.angle_points[0].set_data([xpress], [ypress])
            self.angle_points[1].set_data([xpress], [ypress + dy])
            self.angle_points[2].set_data([xpress + dx], [ypress + dy])
            self.angle_points[3].set_data([xpress + dx], [ypress])
            self._update()

        self.press_point = None
        self.press = False

        self.disconnect_draw()
        self.fig.canvas.send_event("toolbar_update", action="Draw", active=False)

        update_draw_button_status(self.fig, '')

        drect = CDEllipse(self.fig, self.ellipse, self.side_points, self.angle_points, self.graphics_type)
        drect.init_points()
        drect.connect()
        mw_get_cfig().lst_draw_graphics.append(drect)
        mw_get_cfig().current_objs.append(drect)

    def draw_self(self):
        self.fig.draw_artist(self.ellipse)
        for i in range(0, 4):
            self.fig.draw_artist(self.side_points[i])
            self.fig.draw_artist(self.angle_points[i])

    def _update(self):
        if self.background is not None:
            self.canvas.restore_region(self.background)

        # for dline in mw_get_cfig().draw_lines:
        #     dline.draw_self()

        self.draw_self()

        self.canvas.blit(self.fig.bbox)

class CDrawGraphics(object):
    lock = None
    motion_lock = None

    def __init__(self, fig, graphics, side_points, angle_points, graphics_type):
        """
        初始化函数

        arg:
            fig:    图窗对象
        """
        self.fig = fig
        self.canvas = self.fig.canvas
        self.press = False
        self.start = []
        self.picked = True
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self.fix_ax = None
        self.contains_rect = False

        # 每个点的拖拽单独处理
        self.graphics = graphics
        self.side_points = side_points
        self.point_left = self.side_points[0]
        self.point_top = self.side_points[1]
        self.point_right = self.side_points[2]
        self.point_bottom = self.side_points[3]

        self.angle_points = angle_points
        self.point_left_bottom = self.angle_points[0]
        self.point_left_top = self.angle_points[1]
        self.point_right_top = self.angle_points[2]
        self.point_right_bottom = self.angle_points[3]

        self.graphics_type = graphics_type

        self.units = 'normalized'
        self.margin = 5
        self.fit_box_to_text = False
        self.facealpha = 1.0
        self.facecolor = 'none'
        self.edgecolor = self.graphics.get_edgecolor()
        self.linestyle = self.graphics.get_linestyle()

        self.h_alignment = 'left'
        self.v_alignment = 'top'

        # 当前图形坐标
        self.pos = None

        self.dict_style = {'实线' : ['-', 'solid'],
                    '虚线' : ['--', 'dashed'],
                    '点线' : [':', 'dotted'],
                    '点划线' : ['-.', 'dashdot'],
                    '无' : ['None', ' ', '', 'none']}

        self.init_text()
        
    def before_export(self):
        self.canvas = None
        self.background = None
        if self.cid_draw:
            self.fig.canvas.mpl_disconnect(self.cid_draw)

    def after_export(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()

    def after_import(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()
        
    # 将缩放点的坐标系改为normalized
    def init_points(self):
        for i in range(0, 4):
            point_side = self.side_points[i]
            point_angle = self.angle_points[i]

            new_pos_side = self.fig.transFigure.inverted().transform(
                (point_side.get_xdata()[0], point_side.get_ydata()[0]))
            point_side.set_transform(self.fig.transFigure)
            point_side.set_data([new_pos_side[0]], [new_pos_side[1]])

            new_pos_angle = self.fig.transFigure.inverted().transform(
                (point_angle.get_xdata()[0], point_angle.get_ydata()[0]))
            point_angle.set_transform(self.fig.transFigure)
            point_angle.set_data([new_pos_angle[0]], [new_pos_angle[1]])

    # 操作图形的事件函数
    def init_text(self):
        if self.graphics_type == 'textbox':
            self.text = Text(x=10,y=10,
                            text='text',
                            bbox=dict(fc="none", ec="none"),
                            verticalalignment='top',
                            wrap=True)
                            # horizontalalignment='center',)
            self.text.set_transform(self.fig.get_transform())
            self.text.set_animated(True)
            self.text.set_in_layout(False)
            self.fig.add_artist(self.text)
            self.text.text_box = self.graphics.get_window_extent()

            self.text._get_wrapped_text = self._get_wrapped_text
            self.text._get_wrap_line_width = self._get_wrap_line_width

    def connect(self):
        self.cid_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        self.cid_draw = self.fig.canvas.mpl_connect(
            'draw_event', self.on_draw)
        self.cid_key_press = self.fig.canvas.mpl_connect(
            'key_press_event', self.on_key_press)

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_press)
        self.fig.canvas.mpl_disconnect(self.cid_release)
        self.fig.canvas.mpl_disconnect(self.cid_motion)
        self.fig.canvas.mpl_disconnect(self.cid_draw)
        self.fig.canvas.mpl_disconnect(self.cid_key_press)

    def on_press(self, event):
        if not mw_get_cfig(self.fig).edit_mode:
            return

        if (CDrawGraphics.lock is not None):
            return

        if event.button is MouseButton.RIGHT:
            return

        # 判读每个点是否被选中，若被选中，切换相应鼠标状态
        self.press_left, attrd = self.point_left.contains(event)
        self.press_top, attrd = self.point_top.contains(event)
        self.press_right, attrd = self.point_right.contains(event)
        self.press_bottom, attrd = self.point_bottom.contains(event)
        self.press_left_bottom, attrd = self.point_left_bottom.contains(event)
        self.press_left_top, attrd = self.point_left_top.contains(event)
        self.press_right_top, attrd = self.point_right_top.contains(event)
        self.press_right_bottom, attrd = self.point_right_bottom.contains(event)
        self.contains_rect, attrd = self.graphics.contains(event)

        if self.press_left or self.press_right:
            # event.canvas.setCursor(Qt.SizeHorCursor)
            self.canvas.send_event({"cursor":"e-resize"})
        elif self.press_top or self.press_bottom:
            # event.canvas.setCursor(Qt.SizeVerCursor)
            self.canvas.send_event({"cursor":"n-resize"})
        elif self.press_right_top or self.press_left_bottom:
            right_top_pos_x = self.point_right_top.get_xdata()[0]
            right_top_pos_y = self.point_right_top.get_ydata()[0]
            left_bottom_pos_x = self.point_left_bottom.get_xdata()[0]
            left_bottom_pos_y = self.point_left_bottom.get_ydata()[0]
            if (right_top_pos_x - left_bottom_pos_x) * (right_top_pos_y - left_bottom_pos_y) > 0:
                # event.canvas.setCursor(Qt.SizeBDiagCursor)
                self.canvas.send_event({"cursor":"ne_resize"})
            else:
                # event.canvas.setCursor(Qt.SizeFDiagCursor)
                self.canvas.send_event({"cursor":"nw_resize"})
        elif self.press_right_bottom or self.press_left_top:
            right_bottom_pos_x = self.point_right_bottom.get_xdata()[0]
            right_bottom_pos_y = self.point_right_bottom.get_ydata()[0]
            left_top_pos_x = self.point_left_top.get_xdata()[0]
            left_top_pos_y = self.point_left_top.get_ydata()[0]
            if (right_bottom_pos_x - left_top_pos_x) * (right_bottom_pos_y - left_top_pos_y) < 0:
                # event.canvas.setCursor(Qt.SizeFDiagCursor)
                self.canvas.send_event({"cursor":"nw_resize"})
            else:
                # event.canvas.setCursor(Qt.SizeBDiagCursor)
                self.canvas.send_event({"cursor":"ne_resize"})
        elif self.contains_rect:
            # event.canvas.setCursor(Qt.SizeAllCursor)
            self.canvas.send_event({"cursor":"move"})
        elif self.graphics_type == 'textbox':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                # event.canvas.setCursor(Qt.SizeAllCursor)
                self.canvas.send_event({"cursor":"move"})
            else:
                return
        else:
            return

        # self.start = (event.x, event.y)
        self.start = self.point_left_bottom.get_transform().inverted().transform((event.x, event.y))

        # 按下时获取各个端点的像素坐标
        self.side_pos = []
        self.angle_pos = []
        for i in range(0, 4):
            self.side_pos.append((self.side_points[i].get_xdata()[0],
                                        self.side_points[i].get_ydata()[0]))
            self.angle_pos.append((self.angle_points[i].get_xdata()[0],
                                        self.angle_points[i].get_ydata()[0]))

        self.start_width = self.graphics.get_width()
        self.start_height = self.graphics.get_height()

        self.press = True
        CDrawGraphics.lock = self
        # self.adjust_order()

        # self.canvas.draw()
        self._update()

        if event.dblclick:
            return
            if self.graphics_type == 'textbox':
                self.action_edit()
            else:
                self.action_prop()

            self.contains_rect = False
            self.press = False
            CDrawGraphics.lock = None
            CDrawGraphics.motion_lock = None

    def on_motion(self, event):
        if not self.picked:
            return

        if not self.press:
            self.motion_status(event)
        else:
            current_pos_x, current_pos_y = self.point_left_bottom.get_transform().inverted().transform((event.x, event.y))
            start_x = self.start[0]
            dx = current_pos_x - start_x
            # 先更新缩放点位置
            # 再调用函数更新图形对象的位置大小
            if self.press_left:
                self.point_left.set_xdata([current_pos_x])
                self.point_left_top.set_xdata([current_pos_x])
                self.point_left_bottom.set_xdata([current_pos_x])
                right_pos = self.point_right.get_xdata()[0]
                self.point_top.set_xdata([(current_pos_x + right_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + right_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_top:
                self.point_top.set_ydata([current_pos_y])
                self.point_left_top.set_ydata([current_pos_y])
                self.point_right_top.set_ydata([current_pos_y])
                bottom_pos = self.point_bottom.get_ydata()[0]
                self.point_left.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_right:
                self.point_right.set_xdata([current_pos_x])
                self.point_right_top.set_xdata([current_pos_x])
                self.point_right_bottom.set_xdata([current_pos_x])
                left_pos = self.point_left.get_xdata()[0]
                self.point_top.set_xdata([(current_pos_x + left_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + left_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_bottom:
                self.point_bottom.set_ydata([current_pos_y])
                self.point_left_bottom.set_ydata([current_pos_y])
                self.point_right_bottom.set_ydata([current_pos_y])
                top_pos = self.point_top.get_ydata()[0]
                self.point_left.set_ydata([(current_pos_y + top_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + top_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_left_bottom:
                self.point_left_bottom.set_data([current_pos_x], [current_pos_y])
                self.point_left.set_xdata([current_pos_x])
                self.point_left_top.set_xdata([current_pos_x])
                self.point_bottom.set_ydata([current_pos_y])
                self.point_right_bottom.set_ydata([current_pos_y])
                right_pos = self.point_right.get_xdata()[0]
                top_pos = self.point_top.get_ydata()[0]
                self.point_top.set_xdata([(current_pos_x + right_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + right_pos) / 2])
                self.point_left.set_ydata([(current_pos_y + top_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + top_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_left_top:
                self.point_left_top.set_data([current_pos_x], [current_pos_y])
                self.point_left.set_xdata([current_pos_x])
                self.point_left_bottom.set_xdata([current_pos_x])
                self.point_top.set_ydata([current_pos_y])
                self.point_right_top.set_ydata([current_pos_y])
                right_pos = self.point_right.get_xdata()[0]
                bottom_pos = self.point_bottom.get_ydata()[0]
                self.point_top.set_xdata([(current_pos_x + right_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + right_pos) / 2])
                self.point_left.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_right_top:
                self.point_right_top.set_data([current_pos_x], [current_pos_y])
                self.point_right.set_xdata([current_pos_x])
                self.point_right_bottom.set_xdata([current_pos_x])
                self.point_top.set_ydata([current_pos_y])
                self.point_left_top.set_ydata([current_pos_y])
                left_pos = self.point_left.get_xdata()[0]
                bottom_pos = self.point_bottom.get_ydata()[0]
                self.point_top.set_xdata([(current_pos_x + left_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + left_pos) / 2])
                self.point_left.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + bottom_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.press_right_bottom:
                self.point_right_bottom.set_data([current_pos_x], [current_pos_y])
                self.point_right.set_xdata([current_pos_x])
                self.point_right_top.set_xdata([current_pos_x])
                self.point_bottom.set_ydata([current_pos_y])
                self.point_left_bottom.set_ydata([current_pos_y])
                left_pos = self.point_left.get_xdata()[0]
                top_pos = self.point_top.get_ydata()[0]
                self.point_top.set_xdata([(current_pos_x + left_pos) / 2])
                self.point_bottom.set_xdata([(current_pos_x + left_pos) / 2])
                self.point_left.set_ydata([(current_pos_y + top_pos) / 2])
                self.point_right.set_ydata([(current_pos_y + top_pos) / 2])
                self.fit_box_to_text = False
                self.update_graphics_position()
            elif self.contains_rect:
                dx = current_pos_x - self.start[0]
                dy = current_pos_y - self.start[1]
                for i in range(0, 4):
                    self.side_points[i].set_data([self.side_pos[i][0] + dx],
                                                [self.side_pos[i][1] + dy])
                    self.angle_points[i].set_data([self.angle_pos[i][0] + dx],
                                                [self.angle_pos[i][1] + dy])

                self.update_graphics_position()

            self.calculate_text_position()
            self.update_left_bottom_color()
            self.outrange_cancel_fix()
            self._update()

    def on_release(self, event):
        if CDrawGraphics.lock is not self:
            return

        self.contains_rect = False

        self.press = False
        CDrawGraphics.lock = None
        CDrawGraphics.motion_lock = None

        # self.background = None

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

        if self.background is not None:
            self.canvas.restore_region(self.background)

        self.update_graphics_position()
        self.calculate_text_position()
        self.draw_self()

    def on_key_press(self, event):
        if not self.picked:
            return

        # 先把像素坐标转换为端点的坐标系坐标
        lst_side_pos = []
        lst_angle_pos = []
        for i in range(0, 4):
            side_pos = self.side_points[i].get_transform().transform(
                (self.side_points[i].get_xdata()[0], self.side_points[i].get_ydata()[0]))
            lst_side_pos.append(side_pos)
            angle_pos = self.angle_points[i].get_transform().transform(
                (self.angle_points[i].get_xdata()[0], self.angle_points[i].get_ydata()[0]))
            lst_angle_pos.append(angle_pos)

        if event.key == 'left':
            for i in range(0, 4):
                lst_side_pos[i] = (lst_side_pos[i][0] - 1, lst_side_pos[i][1])
                lst_angle_pos[i] = (lst_angle_pos[i][0] - 1, lst_angle_pos[i][1])
        elif event.key == 'right':
            for i in range(0, 4):
                lst_side_pos[i] = (lst_side_pos[i][0] + 1, lst_side_pos[i][1])
                lst_angle_pos[i] = (lst_angle_pos[i][0] + 1, lst_angle_pos[i][1])
        elif event.key == 'up':
            for i in range(0, 4):
                lst_side_pos[i] = (lst_side_pos[i][0], lst_side_pos[i][1] + 1)
                lst_angle_pos[i] = (lst_angle_pos[i][0], lst_angle_pos[i][1] + 1)
        elif event.key == 'down':
            for i in range(0, 4):
                lst_side_pos[i] = (lst_side_pos[i][0], lst_side_pos[i][1] - 1)
                lst_angle_pos[i] = (lst_angle_pos[i][0], lst_angle_pos[i][1] - 1)
        elif event.key == 'delete':
            self.action_delete()
            return
        else:
            return

        for i in range(0, 4):
            pos_side = self.side_points[i].get_transform().inverted().transform(lst_side_pos[i])
            pos_angle = self.angle_points[i].get_transform().inverted().transform(lst_angle_pos[i])
            self.side_points[i].set_data([pos_side[0]], [pos_side[1]])
            self.angle_points[i].set_data([pos_angle[0]], [pos_angle[1]])

        self.update_graphics_position()
        self.calculate_text_position()
        self.outrange_cancel_fix()
        self._update()

    def calculate_text_position(self):
        """
        更新text的位置
        ------------------------------
        """
        if self.graphics_type != 'textbox':
            return

        pos_left_bottom = self.point_left_bottom.get_transform().transform(
            (self.get_left_bottom_point().get_xdata()[0],self.get_left_bottom_point().get_ydata()[0]))

        rect_height = abs(self.graphics.get_height())
        rect_width = abs(self.graphics.get_width())

        # 计算文本水平方向位置
        if self.h_alignment == 'left':
            pos_h = pos_left_bottom[0] + self.margin*1.5
        elif self.h_alignment == 'center':
            pos_h = pos_left_bottom[0] + rect_width/2
        elif self.h_alignment == 'right':
            pos_h = pos_left_bottom[0] + rect_width - self.margin*1.5
        else:
            pos_h = self.text._x

        # 计算文本垂直方向位置
        if self.v_alignment == 'top' or self.v_alignment == 'cap':
            pos_v = pos_left_bottom[1] + rect_height - self.margin*1.5
        elif self.v_alignment == 'middle':
            pos_v = pos_left_bottom[1] + rect_height/2
        elif self.v_alignment == 'baseline' or self.v_alignment == 'bottom':
            pos_v = pos_left_bottom[1] + self.margin*1.5
        else:
            pos_v = self.text._y

        self.text._x = pos_h
        self.text._y = pos_v

        self.text.text_box = self.graphics.get_window_extent()

    def update_graphics_position(self):
        if self.graphics_type == 'ellipse':
            left_bottom_x, left_bottom_y = self.point_left_bottom.get_transform().transform(
                (self.point_left_bottom.get_xdata()[0], self.point_left_bottom.get_ydata()[0]))
            right_top_x, right_top_y = self.point_left_bottom.get_transform().transform(
                (self.point_right_top.get_xdata()[0], self.point_right_top.get_ydata()[0]))

            self.graphics._center = ((left_bottom_x + right_top_x)/2, (left_bottom_y + right_top_y)/2)
            self.graphics._width = right_top_x - left_bottom_x
            self.graphics._height = right_top_y - left_bottom_y
        else:
            left_bottom_x, left_bottom_y = self.point_left_bottom.get_transform().transform(
                (self.point_left_bottom.get_xdata()[0], self.point_left_bottom.get_ydata()[0]))
            right_top_x, right_top_y = self.point_left_bottom.get_transform().transform(
                (self.point_right_top.get_xdata()[0], self.point_right_top.get_ydata()[0]))

            self.graphics._x0 = left_bottom_x
            self.graphics._y0 = left_bottom_y
            self.graphics._width = right_top_x - left_bottom_x
            self.graphics._height = right_top_y - left_bottom_y

    def update_left_bottom_color(self):
        if self.fix_ax == None:
            return

        for i in range(0, 4):
            point_angle = self.angle_points[i]
            point_angle.set_markerfacecolor("#c0e7ff")
            point_angle.set_markeredgecolor("#005a96")
            point_angle.set_markersize(6)

        left_bottom_point = self.get_left_bottom_point()
        left_bottom_point.set_markerfacecolor("#000000")
        left_bottom_point.set_markeredgecolor("#ffff00")
        left_bottom_point.set_markersize(7)

    def update_position_loc_left_bottom(self, pos, width, height):
        """
        以左下角点为基准点对对象的位置和大小进行更新
        """
        pos_x, pos_y = pos
        height = abs(height)
        width = abs(width)

        left_bottom_point = self.get_left_bottom_point()
        if left_bottom_point == self.point_left_bottom:
            self.point_left_bottom.set_data([pos_x], [pos_y])
            self.point_left.set_data([pos_x], [pos_y + height/2])
            self.point_left_top.set_data([pos_x], [pos_y + height])
            self.point_top.set_data([pos_x + width/2], [pos_y + height])
            self.point_right_top.set_data([pos_x + width], [pos_y + height])
            self.point_right.set_data([pos_x + width], [pos_y + height/2])
            self.point_right_bottom.set_data([pos_x + width], [pos_y])
            self.point_bottom.set_data([pos_x + width/2], [pos_y])
            self.update_graphics_position()
        elif left_bottom_point == self.point_left_top:
            self.point_left_top.set_data([pos_x], [pos_y])
            self.point_top.set_data([pos_x + width/2], [pos_y])
            self.point_right_top.set_data([pos_x + width], [pos_y])
            self.point_right.set_data([pos_x + width], [pos_y + height/2])
            self.point_right_bottom.set_data([pos_x + width], [pos_y + height])
            self.point_bottom.set_data([pos_x + width/2], [pos_y + height])
            self.point_left_bottom.set_data([pos_x], [pos_y + height])
            self.point_left.set_data([pos_x], [pos_y + height/2])
            self.update_graphics_position()
        elif left_bottom_point == self.point_right_top:
            self.point_right_top.set_data([pos_x + width], [pos_y])
            self.point_right.set_data([pos_x + width], [pos_y + height/2])
            self.point_right_bottom.set_data([pos_x + width], [pos_y + height])
            self.point_bottom.set_data([pos_x + width/2], [pos_y + height])
            self.point_left_bottom.set_data([pos_x], [pos_y + height])
            self.point_left.set_data([pos_x], [pos_y + height/2])
            self.point_left_top.set_data([pos_x], [pos_y])
            self.point_top.set_data([pos_x + width/2], [pos_y])
            self.update_graphics_position()
        elif left_bottom_point == self.point_right_bottom:
            self.point_right_bottom.set_data([pos_x + width], [pos_y])
            self.point_bottom.set_data([pos_x + width/2], [pos_y])
            self.point_left_bottom.set_data([pos_x], [pos_y])
            self.point_left.set_data([pos_x], [pos_y + height/2])
            self.point_left_top.set_data([pos_x], [pos_y + height])
            self.point_top.set_data([pos_x + width/2], [pos_y + height])
            self.point_right_top.set_data([pos_x + width], [pos_y + height])
            self.point_right.set_data([pos_x + width], [pos_y + height/2])
            self.update_graphics_position()
        else:
            return

    def motion_status(self, event):
        # 判读每个点是否被选中，若被选中，切换相应鼠标状态
        self.press_left, attrd = self.point_left.contains(event)
        self.press_top, attrd = self.point_top.contains(event)
        self.press_right, attrd = self.point_right.contains(event)
        self.press_bottom, attrd = self.point_bottom.contains(event)
        self.press_left_bottom, attrd = self.point_left_bottom.contains(event)
        self.press_left_top, attrd = self.point_left_top.contains(event)
        self.press_right_top, attrd = self.point_right_top.contains(event)
        self.press_right_bottom, attrd = self.point_right_bottom.contains(event)
        self.contains_rect, attrd = self.graphics.contains(event)

        if self.press_left or self.press_right:
            # event.canvas.setCursor(Qt.SizeHorCursor)
            self.canvas.send_event({"cursor":"e_resize"})
            return
        elif self.press_top or self.press_bottom:
            # event.canvas.setCursor(Qt.SizeVerCursor)
            self.canvas.send_event({"cursor":"n_resize"})
            return
        elif self.press_right_top or self.press_left_bottom:
            right_top_pos_x = self.point_right_top.get_xdata()[0]
            right_top_pos_y = self.point_right_top.get_ydata()[0]
            left_bottom_pos_x = self.point_left_bottom.get_xdata()[0]
            left_bottom_pos_y = self.point_left_bottom.get_ydata()[0]
            if (right_top_pos_x - left_bottom_pos_x) * (right_top_pos_y - left_bottom_pos_y) > 0:
                # event.canvas.setCursor(Qt.SizeBDiagCursor)
                event.canvas.send_event({"cursor":"ne-resize"})
            else:
                # event.canvas.setCursor(Qt.SizeFDiagCursor)
                event.canvas.send_event({"cursor":"nw-resize"})
            return
        elif self.press_right_bottom or self.press_left_top:
            right_bottom_pos_x = self.point_right_bottom.get_xdata()[0]
            right_bottom_pos_y = self.point_right_bottom.get_ydata()[0]
            left_top_pos_x = self.point_left_top.get_xdata()[0]
            left_top_pos_y = self.point_left_top.get_ydata()[0]
            if (right_bottom_pos_x - left_top_pos_x) * (right_bottom_pos_y - left_top_pos_y) < 0:
                # event.canvas.setCursor(Qt.SizeFDiagCursor)
                event.canvas.send_event({"cursor":"nw-resize"})
            else:
                # event.canvas.setCursor(Qt.SizeBDiagCursor)
                event.canvas.send_event({"cursor":"ne-resize"})
            return
        elif self.contains_rect:
            # event.canvas.setCursor(Qt.SizeAllCursor)
            event.canvas.send_event({"cursor":"move"})
            return
        elif self.graphics_type == 'textbox':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                # event.canvas.setCursor(Qt.SizeAllCursor)
                event.canvas.send_event({"cursor":"move"})
                return

        # event.canvas.setCursor(Qt.ArrowCursor)
        event.canvas.send_event({"cursor":"default"})

    def get_left_bottom_point(self):
        height = self.graphics.get_height()
        width = self.graphics.get_width()
        if height >= 0 and width >= 0:
            return self.point_left_bottom
        elif height >= 0 and width <= 0:
            return self.point_right_bottom
        elif height <= 0 and width >= 0:
            return self.point_left_top
        elif height <= 0 and width <= 0:
            return self.point_right_top

    def contains_self(self, event):
        self.press_left, attrd = self.point_left.contains(event)
        self.press_top, attrd = self.point_top.contains(event)
        self.press_right, attrd = self.point_right.contains(event)
        self.press_bottom, attrd = self.point_bottom.contains(event)
        self.press_left_bottom, attrd = self.point_left_bottom.contains(event)
        self.press_left_top, attrd = self.point_left_top.contains(event)
        self.press_right_top, attrd = self.point_right_top.contains(event)
        self.press_right_bottom, attrd = self.point_right_bottom.contains(event)
        self.contains_rect, attrd = self.graphics.contains(event)

        if self.graphics_type == 'textbox':
            contains_text, attrd = self.text.contains(event)
            if contains_text:
                return True

        return (self.press_left or self.press_top or self.press_right
                or self.press_bottom or self.press_left_bottom or self.press_left_top
                or self.press_right_top or self.press_right_bottom or self.contains_rect)

    def on_pick(self):
        if not mw_get_cfig().edit_mode:
            return
        
        if not self.picked:
            mw_clear_status()
            self.pick_self()

    def pick_self(self, pick_only = False):
        """选中状态"""
        for i in range(0, 4):
            self.side_points[i].set_visible(True)
            self.angle_points[i].set_visible(True)
        self.fig.canvas.draw_idle()
        self.picked = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        for i in range(0, 4):
            self.side_points[i].set_visible(False)
            self.angle_points[i].set_visible(False)
        self.fig.canvas.draw_idle()
        self.picked = False

    def context_menu(self):
        pass

    def action_delete(self):
        self.disconnect()
        mw_get_cfig().lst_draw_graphics.remove(self)
        mw_get_cfig().current_objs.clear()
        self.graphics.remove()
        for i in range(0, 4):
            self.side_points[i].set_visible(False)
            self.angle_points[i].set_visible(False)
        self.side_points.clear()
        self.angle_points.clear()
        if self.graphics_type == "textbox":
            self.text.remove()

        # 在删除图形的同时，删除对应的属性面板tab页，并切换到Figure的tab页
        if self.graphics_type == "textbox":
            del_prop = "TextBox"
        elif self.graphics_type == "rectangle":
            del_prop = "Rectangle"
        elif self.graphics_type == "ellipse":
            del_prop = "Ellipse"
        self.fig.canvas.send_event("property_remove", current_prop="Figure",del_prop=del_prop)

        # self.canvas.setCursor(Qt.ArrowCursor)
        self.canvas.send_event({"cursor":"default"})
        mw_get_cfig().pick_self()

    def action_fix_to_axes(self):
        left_bottom_point = self.get_left_bottom_point()
        rect_pos = self.point_left_bottom.get_transform().transform(
            (left_bottom_point.get_xdata()[0], left_bottom_point.get_ydata()[0]))

        self.fix_ax = None
        for cax in mw_get_cfig().axs:
            ax_range = cax.ax.get_window_extent()
            if (rect_pos[0] > ax_range.x0
                and rect_pos[0] < ax_range.x1
                and rect_pos[1] > ax_range.y0
                and rect_pos[1] < ax_range.y1):
                self.fix_ax = cax.ax

        if self.fix_ax != None:
            for i in range(0, 4):
                point_side = self.side_points[i]
                point_angle = self.angle_points[i]

                pos_side = point_side.get_transform().transform(
                    (point_side.get_xdata()[0], point_side.get_ydata()[0]))
                new_pos_side = self.fix_ax.transData.inverted().transform(
                    (pos_side[0], pos_side[1]))
                point_side.set_transform(self.fix_ax.transData)
                point_side.set_data([new_pos_side[0]], [new_pos_side[1]])

                pos_angle = point_angle.get_transform().transform(
                    (point_angle.get_xdata()[0], point_angle.get_ydata()[0]))
                new_pos_angle = self.fix_ax.transData.inverted().transform(
                    (pos_angle[0], pos_angle[1]))
                point_angle.set_transform(self.fix_ax.transData)
                point_angle.set_data([new_pos_angle[0]], [new_pos_angle[1]])

            left_bottom_point.set_markerfacecolor("#000000")
            left_bottom_point.set_markeredgecolor("#ffff00")
            left_bottom_point.set_markersize(7)
            self.calculate_text_position()

            self.canvas.draw_idle()

    def action_fix_cancel(self):
        if self.fix_ax != None:
            for i in range(0, 4):
                point_side = self.side_points[i]
                point_angle = self.angle_points[i]
                new_pos_side = self.fix_ax.transData.transform(
                    (point_side.get_xdata()[0], point_side.get_ydata()[0]))
                point_side.set_transform(self.fig.get_transform())
                point_side.set_data([new_pos_side[0]], [new_pos_side[1]])

                new_pos_angle = self.fix_ax.transData.transform(
                    (point_angle.get_xdata()[0], point_angle.get_ydata()[0]))
                point_angle.set_transform(self.fig.get_transform())
                point_angle.set_data([new_pos_angle[0]], [new_pos_angle[1]])

            left_bottom_point = self.get_left_bottom_point()
            left_bottom_point.set_markerfacecolor("#c0e7ff")
            left_bottom_point.set_markeredgecolor("#005a96")
            left_bottom_point.set_markersize(6)

            if self.units == 'normalized':
                self.init_points()

        self.fix_ax = None
        self.canvas.draw_idle()

    def action_color(self):
        if self.graphics_type == 'textbox':
            color = self.text.get_color()
            dlg_color = DlgColor(color_to_qcolor(color))
            if dlg_color.exec_() == QDialog.Accepted:
                select_color = dlg_color.get_color()
                self.text.set_color(select_color.name())
                self.fig.canvas.draw_idle()
        else:
            color = self.graphics.get_edgecolor()
            dlg_color = DlgColor(color_to_qcolor(color))
            if dlg_color.exec_() == QDialog.Accepted:
                select_color = dlg_color.get_color().name()
                if self.linestyle in self.dict_style['无']:
                    select_color = mcolors.to_rgba(select_color, 0.0)
                self.graphics.update(dict(edgecolor=select_color))
                self.edgecolor = select_color
                self.fig.canvas.draw_idle()

    def action_linewidth(self):
        action = QAction()
        sender = action.sender()
        linewidth = float(sender.text())
        self.graphics.set_linewidth(linewidth)
        self.canvas.draw_idle()

    def action_linestyle(self):
        action = QAction()
        sender = action.sender()
        linestyle = self.dict_style[sender.text()][0]
        if linestyle == 'None':
            current_color = color_to_qcolor(self.graphics.get_edgecolor())
            self.graphics.set_edgecolor(mcolors.to_rgba(current_color.name(), 0.0))
        else:
            current_color = color_to_qcolor(self.graphics.get_edgecolor())
            self.graphics.set_edgecolor(mcolors.to_rgba(current_color.name(), 1.0))
            self.graphics.set_linestyle(linestyle)

        self.graphics.set_linestyle(linestyle)
        self.linestyle = linestyle
        self.canvas.draw_idle()

    def action_prop(self):
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.graphics]])
        prop_dlg.set_current_index(1)
        prop_dlg.connect()
        prop_dlg.exec_()

    def action_edit(self):
        self.text_edit=DlgEditGraphicsText(self, self.text)
        self.text_edit.exec()
        self.box_adaptive()

    def action_box_adaptive(self):
        self.fit_box_to_text = not self.fit_box_to_text
        self.box_adaptive()

    def box_adaptive(self):
        if not self.fit_box_to_text:
            return

        text_pos = (self.text.get_window_extent().x0, self.text.get_window_extent().y0,
                    self.text.get_window_extent().x1, self.text.get_window_extent().y1)
        text_width = text_pos[2] - text_pos[0]
        text_height = text_pos[3] - text_pos[1]

        text_origin_pos = (self.text._x, self.text._y)
        # 计算水平方向框位置
        if self.h_alignment == 'left':
            left_pos = text_origin_pos[0] - self.margin*1.5
            right_pos = text_origin_pos[0] + text_width + self.margin*1.5
        elif self.h_alignment == 'center':
            left_pos = text_origin_pos[0] - self.margin*1.5 - text_width/2
            right_pos = text_origin_pos[0] + self.margin*1.5 + text_width/2
        elif self.h_alignment == 'right':
            left_pos = text_origin_pos[0] - self.margin*1.5 - text_width
            right_pos = text_origin_pos[0] + self.margin*1.5
        else:
            return

        # 计算垂直方向框位置
        if self.v_alignment == 'top' or self.v_alignment == 'cap':
            bottom_pos = text_origin_pos[1] - text_height - self.margin*1.5
            top_pos = text_origin_pos[1] + self.margin*1.5
        elif self.v_alignment == 'middle':
            bottom_pos = text_origin_pos[1] - text_height/2 - self.margin*1.5
            top_pos = text_origin_pos[1] + text_height/2 + self.margin*1.5
        elif self.v_alignment == 'baseline' or self.v_alignment == 'bottom':
            bottom_pos = text_origin_pos[1] - self.margin*1.5
            top_pos = text_origin_pos[1] + text_height + self.margin*1.5
        else:
            return

        if self.fix_ax != None:
            left_pos,bottom_pos = self.point_left_bottom.get_transform().inverted().transform((left_pos,bottom_pos))
            right_pos,top_pos = self.point_left_bottom.get_transform().inverted().transform((right_pos,top_pos))
        elif self.units == 'normalized':
            left_pos,bottom_pos = self.fig.transFigure.inverted().transform((left_pos,bottom_pos))
            right_pos,top_pos = self.fig.transFigure.inverted().transform((right_pos,top_pos))

        self.point_left_bottom.set_data([left_pos], [bottom_pos])
        self.point_left.set_data([left_pos], [(bottom_pos + top_pos)/2])
        self.point_left_top.set_data([left_pos], [top_pos])
        self.point_top.set_data([(left_pos + right_pos)/2], [top_pos])
        self.point_right_top.set_data([right_pos], [top_pos])
        self.point_right.set_data([right_pos], [(bottom_pos + top_pos)/2])
        self.point_right_bottom.set_data([right_pos], [bottom_pos])
        self.point_bottom.set_data([(left_pos + right_pos)/2], [bottom_pos])
        self.update_graphics_position()
        self.update_left_bottom_color()
        self._update()

    def action_background_color(self):
        '''字体背景颜色设置动作'''
        tuple_background_color = self.graphics.get_facecolor()
        background_color = color_to_qcolor(tuple_background_color)
        # if tuple_background_color[3]==0.0:
        #     background_color='none'
        dlg_color = DlgColor(background_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            self.facecolor = mcolors.to_rgba(select_color, self.facealpha)
            self.graphics.update(dict(facecolor=self.facecolor))

        self.text.figure.canvas.draw_idle()

    def action_edgecolor(self):
        tuple_edgecolor = self.graphics.get_edgecolor()
        edgecolor = color_to_qcolor(tuple_edgecolor)
        # if tuple_edgecolor[3]==0.0:
        #     edgecolor='none'
        dlg_color = DlgColor(edgecolor)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            if self.linestyle in self.dict_style['无']:
                select_color = mcolors.to_rgba(select_color, 0.0)
            self.graphics.update(dict(edgecolor=select_color))
            self.edgecolor = select_color

        self.fig.canvas.draw_idle()

    def action_facecolor(self):
        tuple_facecolor = self.graphics.get_facecolor()
        facecolor = color_to_qcolor(tuple_facecolor)
        # if tuple_facecolor[3]==0.0:
        #     facecolor='none'
        dlg_color = DlgColor(facecolor)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            self.facecolor = mcolors.to_rgba(select_color, self.facealpha)
            self.graphics.update(dict(facecolor=self.facecolor))

        self.fig.canvas.draw_idle()

    def action_font(self):
        '''设置字体动作'''
        self.font=DlgTitlebaseFont(self,self.text)
        self.font.exec()
        self.box_adaptive()

    def set_transform_normalized(self, transform):
        if self.fix_ax != None:
            return

        for i in range(0, 4):
            point_side = self.side_points[i]
            point_angle = self.angle_points[i]

            # self.side_points[i].set_transform(transform)
            # self.angle_points[i].set_transform(transform)
            new_pos_side = transform.inverted().transform(
                (point_side.get_xdata()[0], point_side.get_ydata()[0]))
            point_side.set_transform(transform)
            point_side.set_data([new_pos_side[0]], [new_pos_side[1]])

            new_pos_angle = transform.inverted().transform(
                (point_angle.get_xdata()[0], point_angle.get_ydata()[0]))
            point_angle.set_transform(transform)
            point_angle.set_data([new_pos_angle[0]], [new_pos_angle[1]])

    def set_transform_pixels(self, transform):
        if self.fix_ax != None:
            return

        if transform == self.point_left_bottom.get_transform():
            return

        for i in range(0, 4):
            point_side = self.side_points[i]
            point_angle = self.angle_points[i]

            new_pos_side = self.fig.transFigure.transform(
                (point_side.get_xdata()[0], point_side.get_ydata()[0]))
            point_side.set_transform(transform)
            point_side.set_data([new_pos_side[0]], [new_pos_side[1]])

            new_pos_angle = self.fig.transFigure.transform(
                (point_angle.get_xdata()[0], point_angle.get_ydata()[0]))
            point_angle.set_transform(transform)
            point_angle.set_data([new_pos_angle[0]], [new_pos_angle[1]])

    def outrange_cancel_fix(self):
        if self.fix_ax != None:
            inrange = self.detect_point_out_of_range()
            if not inrange:
                if len(self.start) == 2:
                    self.start = self.point_left_bottom.get_transform().transform(self.start)

                    for i in range(0, 4):
                        self.side_pos[i] = self.point_left_bottom.get_transform().transform(self.side_pos[i])
                        self.angle_pos[i] = self.point_left_bottom.get_transform().transform(self.angle_pos[i])

                self.action_fix_cancel()

                if len(self.start) == 2:
                    self.start = self.point_left_bottom.get_transform().inverted().transform(self.start)

                    for i in range(0, 4):
                        self.side_pos[i] = self.point_left_bottom.get_transform().inverted().transform(self.side_pos[i])
                        self.angle_pos[i] = self.point_left_bottom.get_transform().inverted().transform(self.angle_pos[i])

    def detect_point_out_of_range(self, pos = None):
        if pos == None:
            point = self.get_left_bottom_point()
            pos = point.get_transform().transform((
                point.get_xdata()[0], point.get_ydata()[0]))

        for cax in mw_get_cfig().axs:
            range = cax.ax.get_window_extent()
            if (pos[0] > range.x0
                and pos[0] < range.x1
                and pos[1] > range.y0
                and pos[1] < range.y1):
                return True

        return False

    def draw_self(self):
        self.fig.draw_artist(self.graphics)
        if self.graphics_type == 'textbox':
            self.fig.draw_artist(self.text)
        for i in range(0, 4):
            self.fig.draw_artist(self.side_points[i])
            self.fig.draw_artist(self.angle_points[i])
        
    def _update(self):
        if not self.picked:
            return

        self.fig.canvas.draw_idle()
        # update_all(self.fig)

    def _get_wrap_line_width(self):
        """
        Return the maximum line width for wrapping text based on the current
        orientation.
        """
        x0, y0 = self.text.get_transform().transform(self.text.get_position())
        if hasattr(self.text, 'text_box') and self.text.text_box != None:
            text_box = self.text.text_box
        else:
            text_box = self.text.get_figure().get_window_extent()

        # Calculate available width based on text alignment
        alignment = self.text.get_horizontalalignment()
        self.text.set_rotation_mode('anchor')
        rotation = self.text.get_rotation()

        left = self.text._get_dist_to_box(rotation, x0, y0, text_box)
        right = self.text._get_dist_to_box(
            (180 + rotation) % 360, x0, y0, text_box)

        if alignment == 'left':
            line_width = left
        elif alignment == 'right':
            line_width = right
        else:
            line_width = 2 * min(left, right)

        return line_width

    def _get_wrapped_text(self):
        """
        Return a copy of the text with new lines added, so that
        the text is wrapped relative to the parent figure.
        """
        # Not fit to handle breaking up latex syntax correctly, so
        # ignore latex for now.
        if self.text.get_usetex():
            return self.text.get_text()

        # Build the line incrementally, for a more accurate measure of length
        line_width = self.text._get_wrap_line_width()
        wrapped_lines = []

        # New lines in the user's text force a split
        unwrapped_lines = self.text.get_text().split('\n')

        # Now wrap each individual unwrapped line
        for unwrapped_line in unwrapped_lines:

            sub_words = unwrapped_line.split(' ')
            # Remove items from sub_words as we go, so stop when empty
            while len(sub_words) > 0:
                if len(sub_words) == 1:
                    # Only one word, so just add it to the end
                    wrapped_lines.append(sub_words.pop(0))
                    continue

                for i in range(2, len(sub_words) + 1):
                    # Get width of all words up to and including here
                    line = ' '.join(sub_words[:i])
                    current_width = self.text._get_rendered_text_width(line)

                    # If all these words are too wide, append all not including
                    # last word
                    if current_width > line_width:
                        wrapped_lines.append(' '.join(sub_words[:i - 1]))
                        sub_words = sub_words[i - 1:]
                        break

                    # Otherwise if all words fit in the width, append them all
                    elif i == len(sub_words):
                        wrapped_lines.append(' '.join(sub_words[:i]))
                        sub_words = []
                        break

        return '\n'.join(wrapped_lines)

    # 属性
    # 颜色和样式
    def get_edgecolor(self):
        return self.edgecolor

    def set_edgecolor(self, color):
        if self.linestyle in self.dict_style['无']:
            color = mcolors.to_rgba(color, 0.0)
        self.graphics.update(dict(edgecolor=color))
        self.edgecolor = color
        self.canvas.draw_idle()

    def get_color(self):
        return self.facecolor

    def set_color(self, color):
        self.facecolor = mcolors.to_rgba(color, self.facealpha)
        self.graphics.update(dict(facecolor=self.facecolor))
        self.canvas.draw_idle()

    def get_facealpha(self):
        return self.facealpha

    def set_facealpha(self, alpha):
        try:
            facealpha=float(alpha)
        except Exception as e:
            return

        if facealpha < 0 or facealpha > 1:
            return

        self.facealpha = facealpha
        if self.facecolor != 'none':
            facecolor = mcolors.to_rgba(self.graphics.get_facecolor(), facealpha)
            self.graphics.set_facecolor(facecolor)
        self.canvas.draw_idle()

    def get_linestyle(self):
        return self.linestyle

    def set_linestyle(self, linestyle):
        invalid = True
        for key, value in self.dict_style.items():
            if linestyle in value:
                invalid = False
                break
        if invalid:
            return

        if linestyle in self.dict_style['无']:
            current_color = color_to_qcolor(self.graphics.get_edgecolor())
            self.graphics.set_edgecolor(mcolors.to_rgba(current_color.name(), 0.0))
        else:
            current_color = self.graphics.get_edgecolor()
            self.graphics.set_edgecolor(mcolors.to_rgba(current_color, 1.0))
            self.graphics.set_linestyle(linestyle)

        self.graphics.set_linestyle(linestyle)
        self.linestyle = linestyle
        self.canvas.draw_idle()

    def get_linewidth(self):
        return self.graphics.get_linewidth()

    def set_linewidth(self, linewidth):
        try:
            linewidth=float(linewidth)
        except Exception as e:
            return

        if linewidth <= 0:
            return

        self.graphics.set_linewidth(linewidth)
        self.canvas.draw_idle()

    def pixels_to_normalized(self,pos):
        return tuple(self.fig.transFigure.inverted().transform(pos))

    # 获取位置
    def get_position(self):
        # 获取当前的graphics左下角点
        left_bottom_point = self.get_left_bottom_point()
        # 通过左下角点获取左下角坐标
        pos_left_bottom = left_bottom_point.get_transform().transform((left_bottom_point.get_xdata()[0], left_bottom_point.get_ydata()[0]))
        # 再获取宽与高
        height = abs(self.graphics.get_height())
        width = abs(self.graphics.get_width())
        # 将pixel单位换算为normalized单位
        pos_right_top = self.pixels_to_normalized((pos_left_bottom[0] + width, pos_left_bottom[1] + height))
        pos_left_bottom = self.pixels_to_normalized(pos_left_bottom)
        # 最终展现的为x y width height
        position = (round(pos_left_bottom[0],4), round(pos_left_bottom[1],4),
                    round((pos_right_top[0]-pos_left_bottom[0]),4),
                    round(((pos_right_top[1]-pos_left_bottom[1])),4))
        return position

    # 将前端传回的字符串坐标数据进行转换
    def str_to_data(self,position):
        x0, y0, width, height = position.split(',')
        # position为[x0, y0, width, height]形式的字符串，因此需对x0与height做处理
        x0 = x0[1:]
        height=height[:-1]
        self.pos = (float(x0), float(y0), float(width) + float(x0), float(height) + float(y0))

    # 设置位置
    def set_position(self, position):
        # 字符串坐标数据转换
        self.str_to_data(position)
        # 新起始点坐标，左下角
        new_pos_start = (self.pos[0], self.pos[1])
        # 右上角坐标
        new_pos_end = (self.pos[2], self.pos[3])
        # 转换为像素坐标
        new_pos_start_pixels = tuple(self.fig.transFigure.transform((self.pos[0], self.pos[1])))
        new_pos_end_pixels = tuple(self.fig.transFigure.transform((self.pos[2], self.pos[3])))

        if self.fix_ax != None:
            # 转换为数据坐标
            new_pos_start = self.fix_ax.transData.inverted().transform(new_pos_start_pixels)
            new_pos_end = self.fix_ax.transData.inverted().transform(new_pos_end_pixels)
            
        # 以左下角为基点更新数据
        self.update_position_loc_left_bottom((new_pos_start[0], new_pos_start[1]),
                                                    new_pos_end[0] - new_pos_start[0], new_pos_end[1] - new_pos_start[1])
        self._update()

    def get_units(self):
        return

    def set_units(self, units):
        return

    def delete_self(self):
        self.action_delete()

class CDRectangle(CDrawGraphics):
    def __init__(self, fig, graphics, side_points, angle_points, graphics_type):
        super().__init__(fig, graphics, side_points, angle_points, graphics_type)

    def on_pick(self):
        if not mw_get_cfig().edit_mode:
            return
        
        if not self.picked:
            mw_clear_status()
            self.pick_self()
            cfig = mw_get_cfig(self.fig)
            if "Rectangle" in cfig.prop_objs and cfig.prop_objs["Rectangle"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Rectangle")
            else:
                # 处理没有坐标轴的情况
                if len(self.fig.axes) > 0:
                    cax = mw_get_cax(self.fig.gca())
                else:
                    cax = None
                props = get_property(cfig, cax, self, "Rectangle")
                self.fig.canvas.send_event("property_init", props=props, current_prop="Rectangle", font_list = get_font_lst())

    def context_menu(self):
        """右键菜单"""
        menu_list = []

        # 删除
        menu_list.append({"value": "rectangle_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "rectangle_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "rectangle_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 面颜色
        # 接收当前面颜色作为默认值
        # facecolor = self.get_facecolor()
        # menu_list.append({"value": "facecolor", "label": "面颜色", "children": [], "default_value": facecolor})

        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "linewidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "linestyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "Rectangle"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    def set_prop(self,name,value):
        """接受前端返回数据，并进行相应操作"""
        name = name.lower()
        
        if name == "rectangle_delete":
            self.action_delete()
        elif name == "rectangle_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "rectangle_fix_cancel":
            self.action_fix_cancel()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
        if name in ["color", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="Rectangle", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())
                    
        return None

    def get_colorandstyle_props(self):
        prop_names = ["Color", "FaceColor", "FaceAlpha", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

    def set_color(self, color):
        """设置rectangle边颜色"""
        if self.linestyle in self.dict_style['无']:
            color = mcolors.to_rgba(color, 0.0)
        self.graphics.update(dict(edgecolor=color))
        self.canvas.draw_idle() 

    def get_color(self):
        return color_to_hex(self.graphics.get_edgecolor())

    def set_facecolor(self,color):
        """设置rectangle面颜色"""
        self.facecolor = mcolors.to_rgba(color, self.facealpha)
        self.graphics.update(dict(facecolor=self.facecolor))
        self.canvas.draw_idle() 
    
    def get_facecolor(self):
        """返回rectangle面颜色"""
        return color_to_hex(self.graphics.get_facecolor())
    
    def set_linestyle(self, linestyle):
        invalid = True
        for key, value in self.dict_style.items():
            if linestyle in value:
                invalid = False
                break
        if invalid:
            return
        
        self.graphics.set_linestyle(linestyle)

        self.graphics.set_linestyle(linestyle)
        self.linestyle = linestyle
        self.canvas.draw_idle()
    
    def get_all_props(self):
        prop_name = {"ColorAndStyle":["Color", "FaceColor", "FaceAlpha", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name

        return props

class CDEllipse(CDrawGraphics):
    def __init__(self, fig, graphics, side_points, angle_points, graphics_type):
        super().__init__(fig, graphics, side_points, angle_points, graphics_type)

    def on_pick(self):
        if not mw_get_cfig().edit_mode:
            return
        
        if not self.picked:
            mw_clear_status()
            self.pick_self()
            cfig = mw_get_cfig(self.fig)
            if "Ellipse" in cfig.prop_objs and cfig.prop_objs["Ellipse"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Ellipse")
            else:
                # 处理没有坐标轴的情况        
                if len(self.fig.axes) > 0:
                    cax = mw_get_cax(self.fig.gca())
                else:
                    cax = None

                props = get_property(cfig, cax, self, "Ellipse")
                self.fig.canvas.send_event("property_init", props=props, current_prop="Ellipse", font_list = get_font_lst())

    def context_menu(self):
        menu_list = []

        # 删除
        menu_list.append({"value": "ellipse_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        menu_list.append({"value": "ellipse_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        menu_list.append({"value": "ellipse_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_edgecolor()
        menu_list.append({"value": "color", "label": "颜色", "children": [], "default_value": color})

        # 面颜色
        # 接收当前面颜色作为默认值 暂不实现  用set_color()实现
        # menu_list.append({"value": "FaceColor", "label": "面颜色", "children": [], "default_value": color})


        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "LineWidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "LineStyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextBox"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    def set_prop(self,name,value):
        """接受前端返回数据，并进行相应操作"""
        name = name.lower()
        
        if name == "ellipse_delete":
            # 删除
            self.action_delete()
        elif name == "ellipse_fix_to_axes":
           # 固定到坐标区
            self.action_fix_to_axes()
        elif name == "ellipse_fix_cancel":
            # 取消固定
            self.action_fix_cancel()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["color", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="Ellipse", child_key = "ColorAndStyle", value = self.get_colorandstyle_props())
                    
        return None

    def get_all_props(self):
        prop_name = {"ColorAndStyle":["Color", "FaceColor", "FaceAlpha", "LineStyle", "LineWidth"],
                     "Position":["Position"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name

        return props

    def get_colorandstyle_props(self):
        prop_names = ["Color", "FaceColor", "FaceAlpha", "LineStyle", "LineWidth"]

        props_colorandstyle = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_colorandstyle[name] = eval(fun)
        return props_colorandstyle

    def set_color(self, color):
        """设置ellipse边颜色"""
        if self.linestyle in self.dict_style['无']:
            color = mcolors.to_rgba(color, 0.0)
        self.graphics.update(dict(edgecolor=color))
        self.canvas.draw_idle() 

    def get_color(self):
        return color_to_hex(self.graphics.get_edgecolor())

    def set_facecolor(self,color):
        """设置ellipse面颜色"""
        self.facecolor = mcolors.to_rgba(color, self.facealpha)
        self.graphics.update(dict(facecolor=self.facecolor))
        self.canvas.draw_idle() 
    
    def get_facecolor(self):
        """返回ellipse面颜色"""
        return color_to_hex(self.graphics.get_facecolor())
    
    def set_linestyle(self, linestyle):
        invalid = True
        for key, value in self.dict_style.items():
            if linestyle in value:
                invalid = False
                break
        if invalid:
            return
        
        self.graphics.set_linestyle(linestyle)

        self.graphics.set_linestyle(linestyle)
        self.linestyle = linestyle
        self.canvas.draw_idle()
        
class CDTextBox(CDrawGraphics):
    def __init__(self, fig, graphics, side_points, angle_points, graphics_type):
        super().__init__(fig, graphics, side_points, angle_points, graphics_type)

    def on_pick(self):
        if not mw_get_cfig().edit_mode:
            return
        
        if not self.picked:
            mw_clear_status()
            self.pick_self()
            cfig = mw_get_cfig(self.fig)
            if "TextBox" in cfig.prop_objs and cfig.prop_objs["TextBox"] == self:
                self.fig.canvas.send_event("property_change", current_prop="TextBox")
            else:
                # 处理没有坐标轴的情况
                if len(self.fig.axes) > 0:
                    cax = mw_get_cax(self.fig.gca())
                else:
                    cax = None

                props = get_property(cfig, cax, self, "TextBox")
                self.fig.canvas.send_event("property_init", props=props, current_prop="TextBox", font_list = get_font_lst())

    # 文本
    def get_text_props(self):
        prop_names = ["String","Color"]

        props_text = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_text[name] = eval(fun)
        return props_text

    def get_color(self):
        return color_to_hex(mcolors.to_rgb(self.text.get_color()))

    def set_color(self, color):
        self.text.set_color((color))
        self.canvas.draw_idle()

    def get_text_edit(self):
        return self.text.get_text()

    def set_text_edit(self,string):
        self.text.set_text(string)
        self.box_adaptive()
        self.canvas.draw_idle()

    def get_string(self):
        return self.text.get_text()

    def set_string(self,string):
        self.text.set_text(string)
        self.box_adaptive()
        self.canvas.draw_idle()

    # 字体
    def get_fontsize(self):
        return self.text.get_fontsize()

    def set_fontsize(self, fontsize):
        fontdict={'size': fontsize}
        self.text.update(fontdict)
        if self.fit_box_to_text:
            self.box_adaptive()
        self.canvas.draw_idle()

    def get_fontangle(self):
        if self.text.get_fontstyle() == 'normal':
            return False
        else:
            return True 

    def set_fontangle(self, fontangle):
        if fontangle == 'True':
            fontangle = 'italic'
            fontdict={'style': fontangle}
            self.text.update(fontdict)
            self.canvas.draw_idle()
        else:
            fontangle = 'normal'
            fontdict={'style': fontangle}
            self.text.update(fontdict)
            self.canvas.draw_idle()

    def get_fontname(self):
        return self.text.get_fontname()

    def set_fontname(self, fontname):
        fontname = get_real_name(fontname)
        fontdict={'family': fontname}
        self.text.update(fontdict)
        self.canvas.draw_idle()

    def get_fontweight(self):
        if self.text.get_fontweight() == 'normal':
            return False
        else:
            return True 

    def set_fontweight(self, fontweight):
        if fontweight == 'True':
            fontweight = 'bold'
            fontdict={'weight': fontweight}
            self.text.update(fontdict)
            self.canvas.draw_idle()
        else:
            fontweight = 'normal'
            fontdict={'weight': fontweight}
            self.text.update(fontdict)
            self.canvas.draw_idle()

    # 文本框
    def get_textbox_props(self):
        prop_names = ["FitBoxToText","EdgeColor", "BackgroundColor", "LineStyle", "LineWidth", "FaceAlpha", "Margin"]

        props_textbox = {}
        for name in prop_names:
            fun = f"self.get_{name.lower()}()"
            props_textbox[name] = eval(fun)
        return props_textbox

    def get_fitboxtotext(self):
        return self.fit_box_to_text

    def set_fitboxtotext(self, fitboxtotext):
            # fitboxtotext == 'True'是属性面板修改 fitboxtotext == ''是右键修改
            if (fitboxtotext == 'True') or (fitboxtotext == ''):
                self.fit_box_to_text = True
                self.box_adaptive()
                self._update()
            else:
                self.fit_box_to_text = False
            

    def get_edgecolor(self):
        return color_to_hex(self.edgecolor)

    def set_edgecolor(self, color):
        if self.linestyle in self.dict_style['无']:
            color = mcolors.to_rgba(color, 0.0)
        self.graphics.update(dict(edgecolor=color))
        self.edgecolor = color
        self.box_adaptive()
        self.canvas.draw_idle()

    def get_backgroundcolor(self):
        return color_to_hex(self.facecolor)

    def set_backgroundcolor(self, color):
        self.graphics.update(dict(facecolor=color))
        self.facecolor = color
        self.box_adaptive()
        self.canvas.draw_idle()

    def get_linestyle(self):
        return self.linestyle

    def set_linestyle(self, linestyle):
        invalid = True
        for key, value in self.dict_style.items():
            if linestyle in value:
                invalid = False
                break
        if invalid:
            return
        
        self.graphics.set_linestyle(linestyle)

        self.graphics.set_linestyle(linestyle)
        self.linestyle = linestyle
        self.canvas.draw_idle()

    def get_linewidth(self):
        return self.graphics.get_linewidth()

    def set_linewidth(self, linewidth):
        try:
            linewidth=float(linewidth)
        except Exception as e:
            return

        if linewidth <= 0:
            return

        self.graphics.set_linewidth(linewidth)
        self.box_adaptive()
        self.canvas.draw_idle()

    def get_margin(self):
        return self.margin

    def set_margin(self, margin):
        try:
            margin=float(margin)
        except Exception as e:
            return

        self.margin = margin
        self.calculate_text_position()
        self.box_adaptive()
        self._update()

    # 位置
    def get_horizontalalignment(self):
        return self.h_alignment

    def set_horizontalalignment(self, alignment):
        if alignment not in ['left', 'center', 'right']:
            return

        self.h_alignment = alignment
        self.text.set_horizontalalignment(alignment)
        self.calculate_text_position()

        if self.fit_box_to_text == "on":
            self.action_box_adaptive()
        self.canvas.draw_idle()

    def get_verticalalignment(self):
        return self.v_alignment

    def set_verticalalignment(self, alignment):
        if alignment not in ['baseline', 'bottom', 'top', 'cap', 'middle']:
            return

        self.v_alignment = alignment
        if alignment == 'baseline' or alignment == 'bottom':
            text_va = 'bottom'
        elif alignment == 'top' or alignment == 'cap':
            text_va = 'top'
        else:
            text_va = 'center'

        self.text.set_verticalalignment(text_va)
        self.calculate_text_position()

        if self.fit_box_to_text == "on":
            self.action_box_adaptive()
        self.canvas.draw_idle()

    # 右键菜单
    def context_menu(self):
        menu_list = []

        # 删除
        menu_list.append({"value": "text_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 固定到坐标区
        # menu_list.append({"value": "text_fix_to_axes", "label": "固定到坐标区", "children": [], "default_value": ""})

        # 取消固定
        # menu_list.append({"value": "text_fix_cancel", "label": "取消固定", "children": [], "default_value": ""})
        
        # 编辑文本
        # 接收当前文本作为默认值
        text = self.get_text_edit()
        menu_list.append({"value": "text_edit", "label": "编辑文本", "children": [], "default_value": text})
        
        
        # 使框适合文本大小
        menu_list.append({"value": "FitBoxToText", "label": "使框适合文本大小", "children": [], "default_value": ""})
        
        
        # 颜色
        # 接收当前颜色作为默认值
        # color = self.get_color()
        # menu_list.append({"value": "Color", "label": "颜色", "children": [], "default_value": color})

        # 背景颜色
        # 接收当前背景颜色作为默认值
        # backgroundcolor = self.get_backgroundcolor()
        # menu_list.append({"value": "BackgroundColor", "label": "背景颜色", "children": [], "default_value": backgroundcolor})

        # 边颜色
        # 接收当前边颜色作为默认值
        # edgecolor = self.get_edgecolor()
        # menu_list.append({"value": "EdgeColor", "label": "边颜色", "children": [], "default_value": edgecolor})

        # 字体
        # 字体包括以下内容，fontname、fontsize、fontangle、fontweight
        # font_family = []
        # 字体名称
        # fontname = self.get_fontname()
        # font_family.append(fontname)
        # 字体大小
        # fontsize = self.get_fontsize()
        # font_family.append(fontsize)
        # 字体角度
        # fontangle = self.get_fontangle()
        # font_family.append(fontangle)
        # 字体粗细
        # fontweight = self.get_fontweight()
        # font_family.append(fontweight)
        # menu_list.append({"value": "text_font", "label": "字体", "children": [], "default_value": font_family})

        # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        # 作为默认值
        lineswidth = self.get_linewidth()
        # 建立对应关系
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "LineWidth", "label": "线宽", "children": lst_linewidth_dict, "default_value": lineswidth})

        # 线型
        lst_lineprop_label = ['实线','虚线','点线','点划线','无']
        lst_lineprop_value = ['-', '--', ':', '-.', 'None']
        lst_lineprop_dict = []
        # 作为默认值
        lineprop = self.get_linestyle()
        # 建立对应关系
        for i in range(0, len(lst_lineprop_value)):
            lineprop_dict = {"label": lst_lineprop_label[i], "value": lst_lineprop_value[i]}
            lst_lineprop_dict.append(lineprop_dict)
        menu_list.append({"value": "LineStyle", "label": "线型", "children": lst_lineprop_dict, "default_value": lineprop})

        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "TextBox"})
        
        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    # 接受前端返回数据，并进行相应操作
    def set_prop(self,name,value):
        # name = name.lower()
        name = name.lower()
        
        if name == "text_delete":
            self.action_delete()
        elif name == "text_fix_to_axes":
            self.action_fix_to_axes()
        elif name == "text_fix_cancel":
            self.action_fix_cancel()
        else:
            try:
                fun = f"self.set_{name}('{value}')"
                eval(fun)
            except:
                return None
            
        if name in ["fitboxtotext", "linewidth", "linestyle"]:
            self.fig.canvas.send_event("property_update", key="TextBox", child_key = "TextBox", value = self.get_textbox_props())
        elif name in ["text_edit"]:
            self.fig.canvas.send_event("property_update", key="TextBox", child_key = "Text", value = self.get_text_props())

        return None
    
    def get_all_props(self):
        prop_name = {"Text":["String", "Color"],
                     "Fonts":["FontName", "FontAngle", "FontSize", "FontWeight"],
                     "TextBox":["FitBoxToText","EdgeColor", "BackgroundColor", "LineStyle", "LineWidth", "FaceAlpha", "Margin"],
                     "Position":["Position","HorizontalAlignment", "VerticalAlignment"]}

        props = {}
        for key,value in prop_name.items():
            props_name = {}
            for prop_value in value:
                prop_value_lower = prop_value.lower()
                fun = f"self.get_{prop_value_lower}()"
                props_name[prop_value] = eval(fun)
            props[key] = props_name

        return props

# #修改文本对话框
# class DlgEditGraphicsText(DlgEditText):
#     '''字体设置对话框'''
#     def __init__(self, dtext, text, parent=None):
#         self.dtext = dtext
#         self.text = text
#         super().__init__(text.get_text(), parent=parent)

#     def update_text(self):
#         text = self.textEdit.toPlainText()
#         self.text.set_text(text)
#         self.dtext.calculate_text_position()
#         self.dtext._update()

# #字体属性对话框
# class DlgTitlebaseFont(DlgFont):
#     def __init__(self, dline, text, parent=None):
#         self.dline=dline
#         super().__init__(text, parent=parent)

#     def init_font_panel(self, text, font_tuple):
#         self.font_layout = DlgTitlebaseFontPanel(self.dline, text, font_tuple)

# class DlgTitlebaseFontPanel(DlgFontPanel):
#     def __init__(self, dline, text, font):
#         self.text = text
#         super().__init__(text, font)

#     def update_font(self):
#         font = self.get_font()
#         style = 'italic' if font[2] else 'normal'
#         weight = 'bold' if font[3] else 'normal'
#         fontdict={'family':font[0],'size': font[1], 'weight' : weight, 'style' : style}

#         self.text.update(fontdict)
#         self.text.figure.canvas.draw()

# 创建线
def mw_annotation_line(line_type, pos_x, pos_y, fig = None, **kwargs):
    text = kwargs.pop('string', '')
    color = kwargs.pop('linecolor', 'black')
    linestyle = kwargs.pop('linestyle','-')
    linewidth = kwargs.pop('linewidth','1.0')
    fontsize = kwargs.pop('fontsize', '10.0')
    fontweight = kwargs.pop('fontweight','normal')
    fontangle = kwargs.pop('fontangle','normal')
    pos_start = (pos_x[0],pos_y[0])
    pos_end = (pos_x[1],pos_y[1])


    dict_type_style = {'line' : '-',
                'arrow' : '->',
                'doublearrow' : '<->',
                'textarrow' : '->'}
    style = dict_type_style[line_type]

    if fig == None:
        fig = plt.gcf()

    line = Annotation('',
        xy=pos_start, xycoords='figure pixels',
        xytext=pos_end, textcoords='figure pixels',
        arrowprops=dict(arrowstyle=style,
                        connectionstyle="arc3"),
        # bbox=dict(fc="none", ec="none"),
        annotation_clip=False,
        **kwargs)
    line.set_animated(True)
    line.set_in_layout(False)
    fig.add_artist(line)
    start_point = Line2D([pos_start[0]], [pos_start[1]], marker = 's', clip_on = False, linestyle = 'none',
        markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
    end_point = Line2D([pos_end[0]], [pos_end[1]], marker = 's', clip_on = False, linestyle = 'none',
        markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')

    start_point.set_animated(True)
    end_point.set_animated(True)
    start_point.set_transform(fig.transFigure)
    end_point.set_transform(fig.transFigure)
    fig.add_artist(start_point)
    fig.add_artist(end_point)

    # 由于原线难以选中，故绘制一条隐藏的辅助线帮助选中
    auxiliary_line = Line2D([pos_start[0],pos_start[1]], [pos_end[0],pos_end[1]],
        clip_on = False, linestyle = '-',linewidth=10)
    auxiliary_line.set_transform(fig.get_transform())
    auxiliary_line.set_animated(True)
    auxiliary_line.set_in_layout(False)
    auxiliary_line.set_visible(False)
    fig.add_artist(auxiliary_line)


    if line_type == 'line':
        dline = CDLine(fig, line, start_point,
            end_point, auxiliary_line, line_type)
    elif line_type == 'arrow':
        dline = CDArrow(fig, line, start_point,
            end_point, auxiliary_line, line_type)
    elif line_type == 'textarrow':
        dline = CDTextArrow(fig, line, start_point,
            end_point, auxiliary_line, line_type)
        dline.text.set_text(text)
        dline.set_fontsize(fontsize) 
        dline.set_fontweight(fontweight)
        dline.set_fontangle(fontangle)
    elif line_type == 'doublearrow':
        dline = CDDoubleArrow(fig, line, start_point,
            end_point, auxiliary_line, line_type)
    dline.set_color(color)    
    dline.set_linestyle(linestyle)  
    dline.set_linewidth(linewidth) 
    
    # dline = CDrawLine(fig, line, start_point,
    #     end_point, auxiliary_line, line_type)
    dline.connect()
    mw_get_cfig().draw_lines.append(dline)

    # if line_type == 'textarrow':
    dline.dis_pick_self()

    return dline

# 创建文本框
def mw_annotation_shape(shape_type, dim, fig = None, **kwargs):
    text_source = kwargs.pop('string', '')

    if not isinstance(text_source, str):
        text_source = np.asarray(text_source).tolist()
    text = ''
    # 处理字符串
    if isinstance(text_source, list):
        lst_text = text_source
        if isinstance(lst_text[0], list):
            lst_text = lst_text[0]

        for i in range(0, len(lst_text)):
            text = text + lst_text[i]
            if i != len(lst_text) - 1:
                text = text + '\n'
    else:
        text = text_source

    FitBoxToText = kwargs.pop('fitboxtotext', '')
    pos_x, pos_y, width, height = dim

    if fig == None:
        fig = plt.gcf()

    side_pos = []
    side_pos.append((pos_x, pos_y + height/2))
    side_pos.append((pos_x + width/2, pos_y + height))
    side_pos.append((pos_x + width, pos_y + height/2))
    side_pos.append((pos_x + width/2, pos_y))

    angle_pos = []
    angle_pos.append((pos_x, pos_y))
    angle_pos.append((pos_x, pos_y + height))
    angle_pos.append((pos_x + width, pos_y + height))
    angle_pos.append((pos_x + width, pos_y))

    side_points = []
    angle_points = []
    for i in range (0, 4):
        side_point = Line2D([side_pos[i][0]], [side_pos[i][1]], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
        side_point.set_animated(True)
        side_point.set_transform(fig.transFigure)
        # side_point.set_data([side_pos[i][0]], [side_pos[i][1]])
        fig.add_artist(side_point)
        side_points.append(side_point)

        angle_point = Line2D([angle_pos[i][0]], [angle_pos[i][1]], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#c0e7ff')
        angle_point.set_animated(True)
        angle_point.set_transform(fig.transFigure)
        # side_point.set_data([angle_pos[i][0]], [angle_pos[i][1]])
        fig.add_artist(angle_point)
        angle_points.append(angle_point)

    edgecolor = kwargs.pop('edgecolor', '')
    if edgecolor == '':
        edgecolor = 'black'
    facecolor = kwargs.pop('facecolor', '')
    if facecolor == '':
        facecolor = 'none'
    facealpha = kwargs.pop('facealpha', '')
    if facealpha == '':
        facealpha = 1
    fill=kwargs.pop('fill','True')
    lw=kwargs.pop('linewidth','1')
    ls=kwargs.pop('linestyle','-')
    try:
        facealpha=float(facealpha)
        if facealpha >= 0 and facealpha <= 1:
            if facecolor != 'none':
                facecolor = mcolors.to_rgba(facecolor, facealpha)
    except Exception as e:
        pass

    ha = kwargs.pop('ha', '')
    if ha == '':
        ha = kwargs.pop('horizontalalignment', '')
        if ha == '':
            ha = 'left'

    va = kwargs.pop('va', '')
    if va == '':
        va = kwargs.pop('verticalalignment', '')
        if va == '':
            va = 'top'

    if shape_type == 'ellipse':
        shape = Ellipse((pos_x, pos_y), width, height,
                        edgecolor = edgecolor,
                        facecolor = facecolor,
                        fill=fill,
                        lw=lw,
                        ls=ls,
                        **kwargs)
    else:
        shape = Rectangle((pos_x, pos_y), width, height,
                        edgecolor = edgecolor,
                        facecolor = facecolor,
                        fill=fill,
                        lw=lw,
                        ls=ls,
                        **kwargs)

    shape.set_transform(fig.get_transform())
    shape.set_animated(True)
    shape.set_in_layout(False)
    fig.add_artist(shape)

    if shape_type == 'rectangle':
        dshape = CDRectangle(fig, shape, side_points, angle_points, shape_type)
    elif shape_type == 'textbox':
        dshape = CDTextBox(fig, shape, side_points, angle_points, shape_type)
        dshape.text.set_text(text)
        dshape.h_alignment = ha
        dshape.v_alignment = va
        dshape.update_graphics_position()
        if ha not in ['left', 'center', 'right']:
            ha = 'left'
        dshape.text.set_horizontalalignment(ha)

        if va not in ['baseline', 'bottom', 'top', 'cap', 'middle']:
            text_va = 'top'
        else:
            if va == 'baseline' or va == 'bottom':
                text_va = 'bottom'
            elif va == 'top' or va == 'cap':
                text_va = 'top'
            else:
                text_va = 'center'
        dshape.text.set_verticalalignment(text_va)

        dshape.calculate_text_position()
        if FitBoxToText == "on":
            dshape.action_box_adaptive()
    elif shape_type == 'ellipse':
        dshape = CDEllipse(fig, shape, side_points, angle_points, shape_type)

    dshape.connect()
    mw_get_cfig().lst_draw_graphics.append(dshape)
    dshape.facealpha = facealpha
    dshape.facecolor = facecolor
    dshape.edgecolor = edgecolor
    dshape.dis_pick_self()

    return dshape
