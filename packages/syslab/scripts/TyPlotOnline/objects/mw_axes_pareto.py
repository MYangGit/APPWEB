"""
名称：axes
功能：此文件用于初始化坐标轴
实现：实现坐标轴的事件、槽函数、右键菜单等
接口：坐标轴类
依赖：
"""

from matplotlib.legend import _get_legend_handles

from TyPlotOnline.objects.mw_axes import CAxes
from TyPlotOnline.objects.mw_figure import *


class CAxesPareto(CAxes):
    """
    实现坐标轴的一些槽函数、右键菜单等

    Attributes
    -------------------
        ax : 主坐标轴
        ax2 : 次坐标轴
    """
    def __init__(self, ax, ax2):
        super().__init__(ax)

        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(which = 'both', direction='in', top = True, right = False, left = True, bottom = False)

        self.ax2 = ax2
        self.init_ax2(ax2)

    def init_ax2(self,ax2):
        ax2.format_coord = lambda x, y: ""

        ax2.spines['top'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.tick_params(which = 'both', direction='in', top = False, right = True, left = False, bottom = True)
        ax2.minorticks_on()
        line_width = self.ax.spines['right'].get_linewidth()
        ax2.tick_params(which = 'minor', length = line_width/2 - 0.4)

        ax2.tick_params(which = 'major',
            grid_color = '#000000ff', grid_alpha = 0.15, grid_linestyle = '-')
        ax2.tick_params(which = 'minor',
            grid_color = '#000000ff', grid_alpha = 0.25, grid_linestyle = ':')

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
        return self.ax.legend(handles, labels, loc = loc, **kwargs)