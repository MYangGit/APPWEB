"""
名称：axes
功能：此文件用于初始化坐标轴
实现：实现坐标轴的事件、槽函数、右键菜单等
接口：坐标轴类
依赖：
"""
from TyPlotOnline.objects.mw_axes import CAxes
from TyPlotOnline.objects.mw_figure import *
from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.objects.mw_text import CYlabel

from matplotlib.legend import _get_legend_handles
import matplotlib.pyplot as plt
circlecolors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

class CAxesYyaxis(CAxes):
    """
    双轴坐标轴主轴

    Attributes
    -------------------
        ax : 主轴
        ax2 : 副轴
    """
    def __init__(self, ax, ax2):
        super().__init__(ax)
        self._init_yyaxis(ax2)

    def _init_yyaxis(self,ax2):
        self.init_ax()
        self.is_current = False
        self.init_colororder()
        self.cur_ax = None
        self.ax2 = ax2
        self.init_ax2(ax2)

    def before_export(self):
        super().before_export()
        self.cax2.before_export()

    def after_export(self):
        super().after_export()
        self.cax2.after_export()

    def after_import(self):
        super().after_import()
        self.cax2.after_import()
    
    def init_colororder(self):
        linestyle_data = ['-','--',':','-.','-','-','-']
        marker_data = ['None','None','None','None','o','^','*']

        cifg = mw_get_cfig(self.fig)
        if self.colororder is not None:
            self.axis_color = self.colororder[0]
        # self.ax.set_prop_cycle(color = self.colororder)
        else:
            next_color = self.ax._get_lines.get_next_color()
            colors_orders = circlecolors if cifg.colororder is None else cifg.colororder
            next_color_name = color_to_qcolor(next_color).name()
            colors_orders_first_name = color_to_qcolor(colors_orders[0]).name()
            circlecolors_first_name = color_to_qcolor(circlecolors[0]).name()

            if next_color_name == colors_orders_first_name or next_color_name == circlecolors_first_name:
                self.axis_color = colors_orders[0]
                self.colororder = [self.axis_color]

                if len(colors_orders) > 1:
                    self.next_color = colors_orders[1]
                else:
                    self.next_color = colors_orders[0]
            else:
                self.next_color = next_color
                self.axis_color = (0,0,0)
                self.colororder = [self.axis_color]

        self.lst_linestyle.clear()
        self.lst_marker.clear()
        lst_color = []
        for i in range(0, len(linestyle_data)):
            linsetyle = linestyle_data[i]
            marker = marker_data[i]
            for color in self.colororder:
                self.lst_linestyle.append(linsetyle)
                self.lst_marker.append(marker)
                lst_color.append(color)
        self.ax.set_prop_cycle(color = lst_color, linestyle = self.lst_linestyle, marker = self.lst_marker)
        # self.ax.set_prop_cycle(color = self.colororder)

    def init_minor_ticks(self):
        super().init_minor_ticks()
        self.ax.spines["left"].set_color(self.axis_color)
        self.ax.spines["right"].set_color(self.axis_color)
        # ax.spines['bottom'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.tick_params(which = 'both', axis = 'y', direction='in', top = True, right = False, left = True, bottom = True, colors = self.axis_color)

    def init_ax2(self,ax2):
        self.cax2 = CAxesYyaxis2(ax2, self.next_color)

        #self.cax2.on_press_self = self.on_press_self_replace

    def _get_legend_handles_labels(self):
        handles = []
        labels = []

        for handle in _get_legend_handles([self.ax, self.ax2]):
            label = handle.get_label()
            if not label.startswith('_'):
                handles.append(handle)
                labels.append(label)

        return handles, labels

    def create_legend(self, *args, loc, **kwargs):
        handles, labels = self._get_legend_handles_labels()
        return self.ax2.legend(handles, labels, loc = loc, **kwargs)

    def on_press_self(self, event):
        if (event.inaxes != self.ax and event.inaxes != self.ax2):
            return

        cur_ax = self.fig.gca()
        if cur_ax != self.ax and cur_ax != self.ax2:
            self.fig.sca(self.ax)

        self.update_action_state()

    def on_press(self):
        cur_ax = self.fig.gca()
        if cur_ax != self.ax and cur_ax != self.ax2:
            self.fig.sca(self.ax)

        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

    def pick_self(self, pick_only = False):
        self.cax2.pick_self(True)
        self.pick = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        self.cax2.dis_pick_self()
        self.fig.canvas.draw_idle()
        self.pick = False

class CAxesYyaxis2(CAxes):
    """
    双轴坐标轴副轴

    Attributes
    -------------------
        ax : 目标坐标轴
        fig : 坐标轴所属图窗
    """
    def __init__(self, ax, next_color):
        self.lst_linestyle = []
        self.lst_marker = []
        self.next_color = next_color

        super().__init__(ax)
        self.is_current = False

    def init_minor_ticks(self):
        super().init_minor_ticks()
        self.ax.spines["left"].set_color(self.axis_color)
        self.ax.spines["right"].set_color(self.axis_color)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)

        self.ax.tick_params(which = 'both', axis = 'y', direction='in', top = False, right = True, left = False, bottom = False, colors = self.axis_color)

    def init_texts(self):
        ylabel = CYlabel(self.ax, self.ax.yaxis.get_label())
        self.ylabels.clear()
        self.ylabels.append(ylabel)

    def on_press_self(self, event):
        pass

    def on_press(self):
        pass

    def init_colororder(self):
        cifg = mw_get_cfig(self.fig)
        if self.colororder is not None:
            self.axis_color = self.colororder[0]
            # self.ax.set_prop_cycle(color = self.colororder)
        else:
            self.axis_color = self.next_color
            self.colororder = [self.axis_color]
            # if cifg.colororder is None:
            #     self.axis_color = circlecolors[1]
            # elif len(cifg.colororder) > 1:
            #     self.axis_color = cifg.colororder[1]
            # else:
            #     self.axis_color = cifg.colororder[0]

            # self.ax.set_prop_cycle(color = [self.axis_color])

        linestyle_data = ['-','--',':','-.','-','-','-']
        marker_data = ['None','None','None','None','o','^','*']

        self.lst_linestyle.clear()
        self.lst_marker.clear()
        lst_color = []
        for i in range(0, len(linestyle_data)):
            linsetyle = linestyle_data[i]
            marker = marker_data[i]
            for color in self.colororder:
                self.lst_linestyle.append(linsetyle)
                self.lst_marker.append(marker)
                lst_color.append(color)
        self.ax.set_prop_cycle(color = lst_color, linestyle = self.lst_linestyle, marker = self.lst_marker)
