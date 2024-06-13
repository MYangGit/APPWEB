"""
名称：mw_interface
功能：提供修改界面属性的接口
接口：各种接口
依赖：
"""

# from PyQt5 import QtCore, QtGui,QtWidgets
# from PyQt5.QtGui import QColor
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QFileDialog
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.uic import loadUi
# from matplotlib.backends.backend_qt5 import SubplotToolQt

from tkinter.messagebox import NO
from typing import Tuple
import matplotlib
# from .import mw_annotation
from matplotlib.text	import Annotation, Text
from matplotlib.contour import QuadContourSet
from matplotlib.collections import LineCollection, PolyCollection, PathCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.projections.polar import PolarAxes
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.container import BarContainer, ErrorbarContainer, StemContainer
import matplotlib.legend as mlegend
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
from matplotlib import (cbook, colors)
from TyPlotOnline.objects.mw_interface import *
from matplotlib.patches import Patch, Rectangle, Wedge
from matplotlib.contour import ContourSet
from matplotlib.image import AxesImage
from matplotlib.collections import Collection
import matplotlib.cm as cm
# from data import get_parula, get_lines, get_prism, get_flag
import matplotlib.ticker as mticker
from matplotlib.projections.polar import _is_full_circle_deg
import matplotlib.markers as mmarkers
import matplotlib.transforms as mtransforms
import matplotlib.axis as maxis
import matplotlib.colors as mcolors
from matplotlib.colorbar import Colorbar
from matplotlib.axes._subplots import SubplotBase

def mw_grid(ax, value = None, which = "major", isonline = False, **kwargs):
    """
    网格线显示隐藏
    显示（或隐藏）坐标轴网格线，可选择主网格、次网格线

    Args:
        ax:     Axes，坐标轴对象
        mode:   string, 网格线显示模式，defult：'major'
            major： 显示/隐藏主网格线
            minor： 显示/隐藏次网格线
            on：    显示主网格线
            off：   隐藏所有网格线

    Returns:
    Raises:
    """

    # 画网格线
    if isinstance(ax, Axes3D):
        if value == None:
            visible = (ax.xaxis.gridlines.get_visible()
                        and ax.yaxis.gridlines.get_visible()
                        and ax.zaxis.gridlines.get_visible())
            if visible and ax._draw_grid:
                #ax.grid(b = False)
                ax.xaxis.gridlines.set_visible(False)
                ax.yaxis.gridlines.set_visible(False)
                ax.zaxis.gridlines.set_visible(False)
            else:
                #ax.grid(b = True)
                ax.xaxis.gridlines.set_visible(True)
                ax.yaxis.gridlines.set_visible(True)
                ax.zaxis.gridlines.set_visible(True)
        elif value == 'off':
            #ax.grid(b = False)
            ax.xaxis.gridlines.set_visible(False)
            ax.yaxis.gridlines.set_visible(False)
            ax.zaxis.gridlines.set_visible(False)
            mw_get_cax().grid = False
        elif value == 'on':
            #ax.grid(b = True)
            ax.xaxis.gridlines.set_visible(True)
            ax.yaxis.gridlines.set_visible(True)
            ax.zaxis.gridlines.set_visible(True)
            mw_get_cax().grid = True
    else:
        ax = mw_get_cax(ax).ax
        if value == None:
            ax.grid(which = which, **kwargs)
            mw_get_cax(ax).grid = not mw_get_cax().grid
        elif value == 'off':
            ax.grid(b = False, which = which, **kwargs)
            mw_get_cax(ax).grid = False
        elif value == 'on':
            ax.grid(b = True, which = which, **kwargs)
            mw_get_cax(ax).grid = True
        # elif value == "minor":
        #     ax.minorticks_on()
        #     ax.grid(which = 'minor', **kwargs)

    if not isonline:
        mw_get_cax().update_action_state()
    ax.figure.canvas.draw_idle()

def mw_home(fig):
    """
    将坐标轴内曲线缩放至最佳

    Args:
        fig: 图窗对象

    Returns:
    Raises:
    """

    home_button = fig.canvas.manager.toolmanager.get_tool('home')
    home_button.trigger(fig, None)

def mw_legend(ax, display = 'on', *args, loc = None, isonline = False, **kwargs):
    """
    创建图例

    参数
    --------
    ax : Axes
        matplotlib 坐标轴对象
    display : str, default : 'on'
        控制图例显示
    args ：
        位置参数
    loc : str, default : None
        图例位置
    isonline : bool, defult : False
        是否为online环境
    kwargs : 
        关键字参数

    返回值
    --------
    legend : CLegend
        图例对象
    """
    from TyPlotOnline.objects.mw_legend import CLegend
    
    clegend = None

    plt.gcf().sca(ax)
    if display == 'off':
        if mw_get_cax_yyaxis(ax) is not None:
            legend = mw_get_cax_yyaxis(ax).ax2.get_legend()
        else:
            legend = ax.get_legend()
        if legend != None:
            if mw_get_clegend(legend) in mw_get_cfig().current_objs:
                mw_clear_status()
                if mw_get_cfig().edit_mode:
                    mw_get_cfig().pick_self()
            clegend = CLegend(legend)
            mw_get_clegend(legend).box.remove()
            legend.remove()
            mw_get_cax(ax).legend = False
            mw_get_cax(legend.axes).legends.clear()
    else:
        lst_ax = []
        cax = mw_get_cax(ax)
        from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
        if isinstance(cax, CAxesPareto):
            lst_ax.append(cax.ax)
            lst_ax.append(cax.ax2)
            handles, labels, extra_args, kwargs = mlegend._parse_legend_args(lst_ax,*args,**kwargs)
            mw_set_legend_names(lst_ax, handles, labels)
            legend = cax.create_legend(*args,loc = loc,**kwargs)
        elif mw_get_cax_yyaxis(ax) is not None:
            lst_ax.append(cax.ax)
            lst_ax.append(cax.ax2)
            handles, labels, extra_args, kwargs = mlegend._parse_legend_args(lst_ax,*args,**kwargs)
            mw_set_legend_names(lst_ax, handles, labels)
            legend = cax.create_legend(*args,loc = loc,**kwargs)
        else:
            lst_ax.append(ax)

            handles, labels, extra_args, kwargs = mlegend._parse_legend_args(lst_ax,*args,**kwargs)
            handles1, labels1, extra_args1, kwargs1 = mlegend._parse_legend_args(lst_ax,**kwargs)

            mw_set_legend_name(ax, handles1, ['']*len(handles1))
            mw_set_legend_name(ax, handles, labels)
            
            # 根据曲线的 zorder 属性对曲线图例进行排序
            if handles:
                sorted_legend_items = sorted(zip(handles, labels), key=lambda item: (item[0].zorder if hasattr(item[0], 'zorder') else item[0][0].zorder))
                # 解压排序后的曲线和标签
                handles, labels = zip(*sorted_legend_items)
            # 更新图例
            font_family = None
            if 'fontfamily' in kwargs:
                font_family = kwargs['fontfamily']
                kwargs.pop('fontfamily', None)
            legend = ax.legend(*args,handles=handles, labels=labels,loc = loc,**kwargs)
            if font_family:
                for label in legend.get_texts():
                        label.set_family(font_family)
        # legend.set_draggable(state=True)
        legend.set_in_layout(False)
        mw_get_cax(ax).legend = True

        # handles,labels=ax.get_legend_handles_labels()
        clegend = CLegend(legend)

        # 更新选中状态
        if mw_get_cfig().edit_mode:
            b = False
            for l in mw_get_cax(legend.axes).legends:
                if l.picked:
                    l.dis_pick_self()
                    b = True
            if b:
                clegend.pick_self()

        mw_get_cax(legend.axes).legends.clear()
        mw_get_cax(legend.axes).legends.append(clegend)

    #设置命令行时工具栏选中状态
    if not isonline:
        mw_get_cax(ax).update_action_state()

    return clegend


def mw_setting_dialog():
    """
    打开属性对话框

    Args:

    Returns:
    Raises:
    """

def mw_help(fig):
    """
    打开帮助

    Args:

    Returns:
    Raises:
    """

    help_class = fig.canvas.manager.toolmanager.get_tool('help')
    html = help_class._get_help_html()
    QtWidgets.QMessageBox.information(None, "Help", html)

def mw_data_tips(fig, target, **kwargs):
    """
    数据提示功能

    Args:
        ax: 坐标轴对象
        current_cursor：当前的管理数据提示的对象

    Returns:
        cursor：新的管理数据提示的对象
    Raises:

    """
    data_tips_button = mw_get_toolbutton(fig, 'data_tips')
    state = data_tips_button.isChecked()
    if target == "on":
        data_tips_button.setChecked(True)
    elif target == "off":
        data_tips_button.setChecked(False)
    elif target == None:
        if state:
            data_tips_button.setChecked(False)
        else:
            data_tips_button.setChecked(True)




def mw_export_csv(ax):
    """
    导出csv

    Args:
        ax: 坐标轴对象

    Returns:
    Raises:

    """

    name, type = QFileDialog.getSaveFileName(None, '导出曲线数据', './', "csv (*.csv)")
    if name:

        lines = ax.get_lines()
        lst = []

        for line in lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()

            lst.append(x_data)
            lst.append(y_data)

        new_lst = list(map(list,zip(*lst)))
        np.savetxt(name,new_lst,delimiter=',')

def mw_get_cfig(fig = None):
    """
    获取当前cfigure对象

    Returns: cfigure
    Raises:

    """
    if fig:
        current_fig = fig
    else:
        current_fig = plt.gcf()

    for c_fig in CGlobalSetting.c_fig_lst:
        if current_fig == c_fig.fig:
            return c_fig

def mw_get_cax(ax = None, yyaxis_ax2 = False):
    """
    获取当前caxes对象

    Returns: caxes
    Raises:

    """
    from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    figure = None
    if ax:
        current_ax = ax
        figure = ax.figure
    else:
        current_ax = plt.gca()
    
    for c_ax in mw_get_cfig(figure).axs:
        if current_ax == c_ax.ax:
            return c_ax
        elif c_ax.__class__.__name__ == "CAxesPareto" and c_ax.ax2 == current_ax:
            return c_ax
        elif c_ax.__class__.__name__ == "CAxesYyaxis" and c_ax.ax2 == current_ax:
            if yyaxis_ax2:
                return c_ax.cax2
            else:
                return c_ax

    return None

def mw_get_cax_yyaxis(ax = None):
    """
    获取当前caxesyyaxis对象

    Returns: caxes
    Raises:

    """
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    if ax:
        current_ax = ax
    else:
        current_ax = plt.gca()

    for c_ax in mw_get_cfig().axs:
        if isinstance(c_ax, CAxesYyaxis) and (c_ax.ax2 == current_ax or c_ax.ax == current_ax):
            return c_ax

    return None

def mw_get_cline(line):
    for cax in mw_get_cfig().get_all_caxes():
        for cline in cax.lines:
            if cline.line == line:
                return cline

    return None

def mw_get_cbar3(bar):
    for cax in mw_get_cfig().get_all_caxes():
        for cbar3 in cax.bar3_containers:
            if cbar3.poly3Dcollection == bar:
                return cbar3

    return None

def mw_get_cbar(bar):
    for cax in mw_get_cfig().get_all_caxes():
        for cbar in cax.bar_containers:
            if cbar.bar_container == bar:
                return cbar
            if isinstance(bar[0], Tuple) and bar[1][0] == cbar.bars[0]:
                return cbar
            if isinstance(bar, Tuple) and bar[0] == cbar.bars[0]:
                return cbar

    return None

def mw_get_chistogram(hist):
    for cax in mw_get_cfig().get_all_caxes():
        for chist in cax.histograms:
            if type(chist.bar_container) == type(hist) and chist.bar_container == hist:
                return chist
            if len(hist) >= 3 and type(chist.bar_container) == type(hist[2]) and chist.bar_container == hist[2]:
                return chist
            if len(hist) >= 3 and isinstance(hist[2], Tuple) and hist[2][0] == chist.bars[0]:
                return chist
            if isinstance(hist, Tuple) and hist[0] == chist.bars[0]:
                return chist

    return None

def mw_get_chistogram2(bar):
    for cax in mw_get_cfig().get_all_caxes():
        for chistogram2s in cax.histogram2s:
            if chistogram2s.poly3Dcollection == bar:
                return chistogram2s

    return None

def mw_get_chist(hist):
    for cax in mw_get_cfig().get_all_caxes():
        for chist in cax.hists:
            if ((type(chist.hist) == type(hist[2]) and chist.hist == hist[2]) or
                (type(chist.hist) == type(hist) and chist.hist == hist)):
                return chist
            if len(hist) >= 3 and isinstance(hist[2], Tuple) and hist[2][0] == chist.bars[0]:
                return chist
            if isinstance(hist, Tuple) and hist[0] == chist.bars[0]:
                return chist

    return None

def mw_get_cpie(pie):
    for cax in mw_get_cfig().get_all_caxes():
        for cpie in cax.pies:
            if cpie.pie == pie:
                return cpie

    return None

def mw_get_cerrorbar(errorbar):
    for cax in mw_get_cfig().get_all_caxes():
        for cerrorbar in cax.errorbars:
            if cerrorbar.errorbar_container == errorbar:
                return cerrorbar

    return None

def mw_get_cstem(stem):
    for cax in mw_get_cfig().get_all_caxes():
        for cstem in cax.stems:
            if cstem.stem_container == stem:
                return cstem
            elif isinstance(stem, Tuple) and stem[0] == cstem.markerline:
                return cstem

    return None

def mw_get_cscatter(scatter):
    for cax in mw_get_cfig().get_all_caxes():
        for cscatter in cax.scatters:
            if cscatter.path_collection == scatter:
                return cscatter

    return None

def mw_get_cstreamline(streamline):
    for cax in mw_get_cfig().get_all_caxes():
        for cstreamline in cax.streamlines:
            if cstreamline.streamline == streamline:
                return cstreamline

    return None

def mw_get_carea(scatter):
    for cax in mw_get_cfig().get_all_caxes():
        for carea in cax.areas:
            if carea.poly_collection == scatter:
                return carea

    return None

def mw_get_csurf(surf):
    for cax in mw_get_cfig().get_all_caxes():
        for csurf in cax.surfs:
            if csurf.poly_collection == surf:
                return csurf

    return None

def mw_get_cpcolor(pcolor):
    for cax in mw_get_cfig().get_all_caxes():
        for cpcolor in cax.pcolors:
            if cpcolor.poly_collection == pcolor:
                return cpcolor

    return None  

def mw_get_ccontour(contour):
    for cax in mw_get_cfig().get_all_caxes():
        for ccontour in cax.contours:
            if ccontour.contour == contour:
                return ccontour

    return None

def mw_get_cfimplicitline(fimplicitline):
    for cax in mw_get_cfig().get_all_caxes():
        for cfimplicitline in cax.fimplicitlines:
            if cfimplicitline.contour == fimplicitline:
                return cfimplicitline

    return None

def mw_get_ctext(text):
    texts=[]
    for cax in mw_get_cfig().get_all_caxes():
        texts += cax.titles + cax.ylabels + cax.xlabels + cax.zlabels + cax.texts
    for colorbar in mw_get_cfig().colorbars:
        texts += colorbar.xlabels + colorbar.ylabels
    for ctext in texts:
        if ctext.text == text:
            return ctext
    return None

def mw_get_clegend(legend):
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    all_axes = []
    for cax in mw_get_cfig().get_all_caxes():
        all_axes.append(cax)
        if isinstance(cax, CAxesYyaxis):
            all_axes.append(cax.cax2)

    for cax in all_axes:
        for clegend in cax.legends:
            if clegend.legend == legend:
                return clegend

    return None

def mw_get_clegend_by_title(text):
    legends=[]
    for ax in mw_get_cfig().get_all_caxes():
        if ax.ax.get_legend() is not None:
            legends.append(ax.ax.get_legend())
    for clegend in legends:
        if clegend.get_title() == text:
            return clegend
    return None

def mw_get_cheatmap(axes_image):
    for cax in mw_get_cfig().get_all_caxes():
        for cheatmap in cax.heatmaps:
            if cheatmap.axes_image == axes_image:
                return cheatmap

    return None

def mw_get_cimage(axes_image):
    for cax in mw_get_cfig().get_all_caxes():
        for cimage in cax.cimages:
            if cimage.axes_image == axes_image:
                return cimage

    return None

def mw_get_ccolorbar(colorbar):
    for c_colorbar in mw_get_cfig().colorbars:
        if c_colorbar.colorbar == colorbar:
            return c_colorbar

    return None

def mw_get_cgeomap(geomap):
    for cax in mw_get_cfig().axs:
        if cax.cgeomap.geomap == geomap:
            return cax.cgeomap

    return None

def mw_get_cgeodensity(geodensity):
    for cax in mw_get_cfig().axs:
        if cax.cgeomap.cdensity_plot == geodensity:
            return cax.cgeomap.cdensity_plot

    return None

def mw_get_dline(line):
    for dline in mw_get_cfig().draw_lines:
        if dline.line == line:
            return dline

    return None

def mw_get_dgraphaics(graphics):
    for dgraphics in mw_get_cfig().lst_draw_graphics:
        if dgraphics.graphics == graphics:
            return dgraphics

    return None

def mw_get_crectangle(rectangle):
    for cax in mw_get_cfig().get_all_caxes():
        for crectangle in cax.rectangles:
            if crectangle.collection == rectangle or crectangle.rect == rectangle:
                return crectangle

    return None

def mw_get_cpatch(patch):
    for cax in mw_get_cfig().get_all_caxes():
        for cpatch in cax.patchs:
            if cpatch.collection == patch:
                return cpatch

    return None

def mw_get_cquiver(quiver):
    for cax in mw_get_cfig().get_all_caxes():
        for cquiver in cax.quivers:
            if cquiver.quiver == quiver:
                return cquiver
    return None

def mw_get_cquiver3(quiver3):
    for cax in mw_get_cfig().get_all_caxes():
        for cquiver3 in cax.quiver3s:
            if cquiver3.quiver3 == quiver3:
                return cquiver3
    return None

def mw_get_cfeather(feather):
    for cax in mw_get_cfig().get_all_caxes():
        for cfeather in cax.feathers:
            if cfeather.feather == feather:
                return cfeather
    return None

def mw_get_ccompass(compass):
    for cax in mw_get_cfig().get_all_caxes():
        for ccompass in cax.compasss:
            if ccompass.compass == compass:
                return ccompass
    return None

def mw_get_cobj(obj):
    from TyPlotOnline.objects.mw_image import CImage
    from TyPlotOnline.objects.mw_stem3 import StemContainer3
    from TyPlotOnline.objects.mw_quiver import MWQuiver
    from TyPlotOnline.objects.mw_compass import MWCompass
    from TyPlotOnline.objects.mw_feather import MWFeather

    if isinstance(obj, Figure):
        return mw_get_cfig()
    elif isinstance(obj, Axes):
        return mw_get_cax(obj)
    elif isinstance(obj, Line2D):
        if mw_get_cstreamline(obj) != None:
            return mw_get_cstreamline(obj)
        else:
            return mw_get_cline(obj)
    elif isinstance(obj, Line3DCollection):
        return mw_get_cquiver3(obj)
    elif isinstance(obj, ErrorbarContainer):
        return mw_get_cerrorbar(obj)
    elif isinstance(obj, BarContainer):
        if mw_get_cbar(obj) != None:
            return mw_get_cbar(obj)
        else:
            return mw_get_chist(obj)
    elif isinstance(obj, StemContainer) or isinstance(obj, StemContainer3):
        return mw_get_cstem(obj)
    elif isinstance(obj, Tuple):
        if mw_get_chistogram(obj) != None:
            return mw_get_chistogram(obj)
        elif mw_get_cbar(obj) != None:
            return mw_get_cbar(obj)
        elif mw_get_chist(obj) != None:
            return mw_get_chist(obj)
        elif mw_get_cstem(obj) != None:
            return mw_get_cstem(obj)
    elif isinstance(obj, Wedge):
        return mw_get_cpie(obj)
    elif isinstance(obj, PathCollection):
        return mw_get_cscatter(obj)
    elif isinstance(obj, Poly3DCollection):
        return mw_get_csurf(obj) or mw_get_cbar3(obj) or mw_get_chistogram2(obj)
    elif isinstance(obj, MWCompass):
        return mw_get_ccompass(obj)
    elif isinstance(obj, MWFeather):
        return mw_get_cfeather(obj)
    elif isinstance(obj, MWQuiver):
        return mw_get_cquiver(obj)
    elif isinstance(obj, PolyCollection):
        if mw_get_carea(obj) != None:
            return mw_get_carea(obj)
        else:
            return mw_get_cpcolor(obj)
    elif isinstance(obj, ContourSet):
        return mw_get_ccontour(obj)
    elif isinstance(obj, AxesImage):
        if mw_get_cheatmap(obj) != None:
            return mw_get_cheatmap(obj)
        else:
            return mw_get_cimage(obj)
    elif isinstance(obj, CImage):
        return obj
    elif isinstance(obj, Annotation):
        return mw_get_dline(obj)
    elif isinstance(obj, Text):
        if mw_get_ctext(obj):
            return mw_get_ctext(obj)
    elif isinstance(obj, Patch):
        return mw_get_dgraphaics(obj)
    elif isinstance(obj, mlegend.Legend):
        if mw_get_clegend(obj):
            return mw_get_clegend(obj)
    elif isinstance(obj, Colorbar):
        return mw_get_ccolorbar(obj)
    elif obj.__class__.__name__ == "CGeoBubble":
        return obj
    elif obj.__class__.__name__ == "CGeoDensity":
        return obj
    elif obj.__class__.__name__ == "CBoxChart":
        return obj
    elif obj.__class__.__name__ == "CWordCloud":
        return obj
    elif obj.__class__.__name__ == "PatchCollection":
        if mw_get_crectangle(obj) != None:
            return mw_get_crectangle(obj)
        else:
            return mw_get_cpatch(obj)

    return None

def mw_get_toolbutton(fig, name):
    # if not CGlobalSetting.isOnline:
    #     toolbar = fig.canvas.manager.toolbar
    #     for button, handler in toolbar._toolitems[name]:
    #         return button

    return None

def mw_remove_tool(toolmanager, name):
    if name == 'grid':
        tool = toolmanager.get_tool(name)
        tool.destroy()

        if getattr(tool, 'toggled', False):
            toolmanager.trigger_tool(tool, 'toolmanager')

        toolmanager._remove_keys(name)

        del toolmanager._tools[name]

    else:
        tool = toolmanager.get_tool(name)
        if tool:
            toolmanager.remove_tool(name)

def mw_remove_toolitem(toolmanager, toolbar, name):
    tool = toolmanager.get_tool(name)
    if tool:
        toolbar.remove_toolitem(name)

def set_toolbutton_enabled(fig, buttonname, enabled):
    # return
    fig.canvas.send_event("toolbar_update", action=buttonname, disabled=not enabled)
    # return
    # button = mw_get_toolbutton(fig, buttonname)
    # if button != None:
    #    button.setEnabled(enabled) 

def set_toolbutton_checked(fig, buttonname, checked):
    # return
    fig.canvas.send_event("toolbar_update", action=buttonname, active=checked)
    # return
    # button = mw_get_toolbutton(fig, buttonname)
    # if button != None:
    #    button.setChecked(checked) 

# 清空选中状态
def mw_clear_status(clear_objs = True):
    """
    初始化属性面板

    Parameters
    ----------
    clear_objs : 是否清除当前选中的对象列表
    """
    cfig = mw_get_cfig()

    cfig.dis_pick_self()
    all_axes = []
    # from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    for cax in cfig.axs:
        all_axes.append(cax)
        # if isinstance(cax, CAxesYyaxis):
        #     all_axes.append(cax.cax2)

    for cax in all_axes:
        cax.dis_pick_self()
        for cline in cax.lines:
            cline.dis_pick_self()
        for c_bar_container in cax.bar_containers:
            c_bar_container.dis_pick_self()
        for c_bar3_container in cax.bar3_containers:
            c_bar3_container.dis_pick_self()
        for c_pie in cax.pies:
            c_pie.dis_pick_self()
        for c_errorbar in cax.errorbars:
            c_errorbar.dis_pick_self()
        for c_stem in cax.stems:
            c_stem.dis_pick_self()
        for c_scatter in cax.scatters:
            c_scatter.dis_pick_self()
        for c_area in cax.areas:
            c_area.dis_pick_self()
        for c_surf in cax.surfs:
            c_surf.dis_pick_self()
        for c_hist in cax.histograms:
            c_hist.dis_pick_self()
        for c_histogram2 in cax.histogram2s:
            c_histogram2.dis_pick_self()
        for c_hist in cax.hists:
            c_hist.dis_pick_self()
        for c_title in cax.titles:
            c_title.dis_pick_self()
        for c_xlabel in cax.xlabels:
            c_xlabel.dis_pick_self()
        for c_ylabel in cax.ylabels:
            c_ylabel.dis_pick_self()
        for c_zlabel in cax.zlabels:
            c_zlabel.dis_pick_self()
        for c_legend in cax.legends:
            c_legend.dis_pick_self()
        for c_text in cax.texts:
            c_text.dis_pick_self()
        for c_image  in cax.cimages:
            c_image.dis_pick_self()
        for c_boxchart in cax.cboxcharts:
            c_boxchart.dis_pick_self()
        for c_wordcloud in cax.cwordclouds:
            c_wordcloud.dis_pick_self()
        for c_contour in cax.contours:
            c_contour.dis_pick_self()
        for c_fimplicitline in cax.fimplicitlines:
            c_fimplicitline.dis_pick_self()
        if cax.cgeomap is not None and cax.cgeomap.cdensity_plot is not None:
            cax.cgeomap.cdensity_plot.dis_pick_self()
        if cax.cgeomap is not None and cax.cgeomap.cbubble_plot is not None:
            cax.cgeomap.cbubble_plot.dis_pick_self()
        for c_rect in cax.rectangles:
            c_rect.dis_pick_self()
        for c_patch in cax.patchs:
            c_patch.dis_pick_self()
        for c_quiver in cax.quivers:
            c_quiver.dis_pick_self()
        for c_quiver3 in cax.quiver3s:
            c_quiver3.dis_pick_self()
        for c_compass in cax.compasss:
            c_compass.dis_pick_self()
        for c_feather in cax.feathers:
            c_feather.dis_pick_self()
        for c_streamline in cax.streamlines:
            c_streamline.dis_pick_self()
        for c_feather_baseline in cax.feather_baselines:
            c_feather_baseline.dis_pick_self()
        for c_pcolor in cax.pcolors:
            c_pcolor.dis_pick_self()
        # 将生成标线置空，从而当点击绘制图形等按钮时，之前点击右键菜单生成标线将不生效
        if cax.dline is not None:
            cax.dline = None

    for c_colorbar in cfig.colorbars:
        c_colorbar.dis_pick_self()
        for c_xlabel in c_colorbar.xlabels:
            c_xlabel.dis_pick_self()
        for c_ylabel in c_colorbar.ylabels:
            c_ylabel.dis_pick_self()

    for d_line in cfig.draw_lines:
        d_line.dis_pick_self()

    for d_graphics in cfig.lst_draw_graphics:
        d_graphics.dis_pick_self()

    if clear_objs:
        mw_get_cfig().current_objs.clear()

def mw_change_obj_color(color, obj):
    if isinstance(obj, Figure):
        obj.set_facecolor(color)
    elif isinstance(obj, Axes):
        obj.set_facecolor(color)

def mw_get_grid_status(ax):
    major_xticks = ax.xaxis.majorTicks
    major_yticks = ax.yaxis.majorTicks
    minor_xticks = ax.xaxis.minorTicks
    minor_yticks = ax.yaxis.minorTicks

    bx_major = False
    by_major = False
    bx_minor = False
    by_minor = False

    # 获取x轴主网格线的状态
    if len(major_xticks) == 0:
        bx_major = False
    else:
        if all(tick.gridline.get_visible() for tick in major_xticks):
            bx_major = True
        elif not any(tick.gridline.get_visible() for tick in major_xticks):
            bx_major = False
        else:
            bx_major = None

    # 获取y轴主网格线的状态
    if len(major_yticks) == 0:
        by_major = False
    else:
        if all(tick.gridline.get_visible() for tick in major_yticks):
            by_major  = True
        elif not any(tick.gridline.get_visible() for tick in major_yticks):
            by_major  = False
        else:
            by_major  = None

    # 获取x轴次网格线的状态
    if len(minor_xticks) == 0:
        bx_minor = False
    else:
        if all(tick.gridline.get_visible() for tick in minor_xticks):
            bx_minor = True
        elif not any(tick.gridline.get_visible() for tick in minor_xticks):
            bx_minor = False
        else:
            bx_minor = None

    # 获取y轴次网格线的状态
    if len(minor_yticks) == 0:
        minor_yticks = False
    else:
        if all(tick.gridline.get_visible() for tick in minor_yticks):
            by_minor = True
        elif not any(tick.gridline.get_visible() for tick in minor_yticks):
            by_minor = False
        else:
            by_minor = None

    return bx_major, by_major, bx_minor, by_minor

def mw_get_legend_status(fig):
    button = mw_get_toolbutton(fig, 'legend')
    if button.isChecked():
        return True
    else:
        return False

def tuple_to_fontdict(tuple):
    style = 'italic' if tuple[2] else 'normal'
    weight = 'bold' if tuple[3] else 'normal'
    fontdict={'family':tuple[0],'size': tuple[1], 'weight' : weight, 'style' : style}
    return fontdict

def float_tuple_to_color(tuple):
    if isinstance(tuple, Tuple):
        return QColor.fromRgbF(tuple[0], tuple[1], tuple[2], 1)
    else:
        color = mcolors.to_rgba(tuple)
        return QColor.fromRgbF(color[0], color[1], color[2], 1)

def udpate_action_state(state):
    button = mw_get_toolbutton(plt.gcf(), 'home')
    button.setEnabled(state)

    button = mw_get_toolbutton(plt.gcf(), 'pan')
    button.setEnabled(state)

    button = mw_get_toolbutton(plt.gcf(), 'zoom')
    button.setEnabled(state)

# 切换选中的对象
def update_select_obj(objs):
    """
    操作的对象发生变化，需要切换当前选中对象


    Parameters
    ----------
    bojs : 当前操作的对象lst
    """
    mw_clear_status()
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    for obj in objs:
        if isinstance(obj, CAxesYyaxis):
            obj.pick_self()
        elif mw_get_cobj(obj) is not None:
            mw_get_cobj(obj).pick_self()

# 设置hold_value
def mw_hold(ax, value):
    c_ax = mw_get_cax(ax)
    if len(c_ax.heatmaps) > 0:
        return "heatmap"
    if len(c_ax.cwordclouds) > 0:
        return "wordcloud"

    if value == None:
        if c_ax.hold_value == 'on':
            value = 'off'
        else:
            value = 'on'
    c_ax.hold_value = value
    return ""

# 获取hold_value
def mw_ishold(ax):
    c_ax = mw_get_cax(ax)
    return c_ax.hold_value

# 清空当前坐标轴
def mw_cla(ax = None, reset = None):
    current_ax = plt.gca() if ax == None else ax

    # 将选中状态切换至figure
    if not CGlobalSetting.isOnline:
        button = mw_get_toolbutton(current_ax.figure, 'edit_mode')
        if button.isChecked():
            c_fig = mw_get_cfig(current_ax.figure)
            if len(c_fig.current_objs) > 0:
                t = c_fig.current_objs[0]

                from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
                from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis2
                from TyPlotOnline.objects.mw_axes import CAxes
                from TyPlotOnline.objects.mw_axes_3d import CAxes3D
                from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
                from TyPlotOnline.mw_draw_graphics import CDrawLine,CDrawGraphics
                if (isinstance(t, CAxes) or isinstance(t, CAxes3D) or isinstance(t, CAxesYyaxis)
                    or isinstance(t, CAxesYyaxis2) or isinstance(t, CAxesPareto)
                    or isinstance(t, CDrawLine) or isinstance(t, CDrawGraphics)):
                    pass
                else:
                    mw_clear_status()
                    c_fig.current_objs.clear()
                    c_fig.pick_self()

    if reset == None or mw_get_cax(current_ax).is_geomap:
        c_ax = mw_get_cax(current_ax, True)

        # 清空地理图中的密度图对象
        if c_ax.is_geomap and c_ax.cgeomap.cdensity_plot != None:
            c_ax.cgeomap.cdensity_plot.density_im.remove()
            c_ax.cgeomap.cdensity_plot = None

        # 清空地理图中的气泡图对象
        if c_ax.is_geomap and c_ax.cgeomap.cbubble_plot != None:
            for i in c_ax.cgeomap.cbubble_plot.scatters:
                i.remove()
            c_ax.cgeomap.cbubble_plot.scatters.clear()
            c_ax.cgeomap.cbubble_plot = None

        # heatmap 不支持 cla()
        if len(c_ax.heatmaps) > 0:
            return

        # 删除colorbar
        # set_toolbutton_checked(current_ax.figure, 'colorbar', False)
        if CGlobalSetting.isOnline == True:
            mw_remove_colorbar(current_ax.figure, current_ax)
        else:
            set_toolbutton_checked(current_ax.figure, 'Colorbar', False)

        c_ax.colorbar_on = False

        # 清空曲线
        for c_line in c_ax.lines:
            c_line.line.remove()
        c_ax.lines.clear()

        # 清空条形图
        for c_bar_container in c_ax.bar_containers:
            c_bar_container.bar_container.remove()
        c_ax.bar_containers.clear()

        # 清空条形图
        for c_bar3_container in c_ax.get_all_bar3s():
            c_bar3_container.remove()
        c_ax.bar3_containers.clear()

        # 清空饼图
        for c_pie in c_ax.pies:
            c_pie.pie.remove()
            c_pie.text.remove()
        c_ax.pie_collection = None
        c_ax.pies.clear()

        # 清空误差图
        for c_errorbar in c_ax.errorbars:
            c_errorbar.errorbar_container.remove()
            # lines = c_errorbar.errorbar_container.lines
            # print(c_errorbar.errorbar_container)
            # data_line = lines[0]
            # data_line.remove()
            # caplines = list(lines[1])
            # for capline in caplines:
            #     capline.remove()
            # barcols = list(lines[2])
            # for barcol in barcols:
            #     barcol.remove()
        c_ax.errorbars.clear()

        # 清空针状图
        for c_stem in c_ax.stems:
            c_stem.stem_container.remove()
        c_ax.stems.clear()

        # 清空散点图
        for c_scatter in c_ax.scatters:
            c_scatter.path_collection.remove()
        c_ax.scatters.clear()

        # 清空区域图
        for c_area in c_ax.areas:
            c_area.poly_collection.remove()
        c_ax.areas.clear()

        # 清空曲面
        for c_surf in c_ax.surfs:
            c_surf.poly_collection.remove()
        c_ax.surfs.clear()

        # 清空曲面
        for c_pcolor in c_ax.pcolors:
            c_pcolor.poly_collection.remove()
        c_ax.pcolors.clear()

        #清空箱线图
        for c_boxchart in c_ax.cboxcharts:
            for item in c_boxchart.artists:
                item.remove()
        c_ax.cboxcharts.clear()

        for c_hist in c_ax.histograms:
            c_hist.bar_container.remove()
        c_ax.histograms.clear()

        #清空二元等高图
        for c_histogram2 in c_ax.histogram2s:
            c_histogram2.poly3Dcollection.remove()
            # c_histogram2.emptyPoly3Dcollection.remove()
        c_ax.histogram2s.clear()

        for c_hist in c_ax.hists:
            c_hist.hist.remove()
        c_ax.histograms.clear()

        for c_contours in c_ax.contours:
            for collection in c_contours.collections:
                collection.remove()
        c_ax.contours.clear()

        #清空箭头图
        for c_quivers in c_ax.quivers:
            c_quivers.quiver.remove()
        c_ax.quivers.clear()

        #清空三维箭头图
        for c_quiver3s in c_ax.quiver3s:
            c_quiver3s.quiver3.remove()
        c_ax.quiver3s.clear()

        #清空流线图
        for c_streamlines in c_ax.streamlines:
            c_streamlines.streamline.remove()
        c_ax.streamlines.clear()

        #清空罗盘图
        for c_compass in c_ax.compasss:
            c_compass.compass.remove()
        c_ax.compasss.clear()

        #清空羽状图
        for c_feather in c_ax.feathers:
            c_feather.feather.remove()
        c_ax.feathers.clear()

        # heatmap 不支持 cla()
        # for c_heatmaps in c_ax.heatmaps:
        #     c_heatmaps.axes_image.remove()
        # c_ax.heatmaps.clear()

        for c_images in c_ax.cimages:
            c_images.axes_image.remove()
        c_ax.cimages.clear()

        # 刷新图例
        # update_legend(current_ax)

        set_toolbutton_enabled(current_ax.figure, 'Cursor', False)
        legend = current_ax.get_legend()
        if legend:
            mw_legend(ax, display = 'off')

        c_ax.update_action_state()

        # 清空数据提示标签
        if c_ax.current_mplcursor != None:
            for sel in c_ax.current_mplcursor.selections:
                c_ax.current_mplcursor.remove_selection(sel)

        if mw_get_cfig(c_ax.fig).current_mplcursor != None:
            mw_get_cfig(c_ax.fig).current_mplcursor.delete_all()

        c_ax.legend_order.clear()

        # 清除基线、选中状态
        for line in current_ax.get_lines():
            line.remove()

        if c_ax.is_geomap:
            return
        # 坐标轴范围更新
        from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
        from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
        if not isinstance(mw_get_cax_yyaxis(current_ax), CAxesYyaxis) \
                and not isinstance(current_ax, PolarAxes) \
                and not isinstance(mw_get_cax(current_ax),CAxesPareto):
            current_ax.set_xlim(xmin = 0, xmax = 1, auto = True)

        if not isinstance(current_ax, PolarAxes) \
                and not isinstance(mw_get_cax(current_ax),CAxesPareto):
            current_ax.set_ylim(ymin = 0, ymax = 1, auto = True)

        if isinstance(mw_get_cax(current_ax), CAxesYyaxis):
            c_ax.init_minor_ticks()
            c_ax.init_grid_style()
            c_ax.init_colororder()

        for c_text in c_ax.texts:
            current_ax.figure.canvas.mpl_disconnect(c_text.draw_id)
            c_text.text.remove()
        c_ax.texts.clear()

    elif reset == 'reset':
        c_ax = mw_get_cax(current_ax)
        current_ax = c_ax.ax
        # current_ax = c_ax.ax
        # heatmap 不支持 cla()
        # if len(c_ax.heatmaps) > 0:
        #     return

        c_ax.colororder = None

        from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
        from TyPlotOnline.objects.mw_figure import mw_update_caxe
        if isinstance(c_ax,CAxesPareto):
            c_ax.ax.cla()
            c_ax.ax2.cla()
        else:
            current_ax.cla()
        if len(c_ax.cwordclouds) > 0:
            current_ax.figure.tight_layout(rect = (0.13,0.11,0.905,0.925))
            current_ax.figure.tight_layout(rect = (0.13,0.11,0.905,0.925))

        c_ax.lines.clear()
        c_ax.bar_containers.clear()
        c_ax.bar3_containers.clear()
        c_ax.pies.clear()
        c_ax.pie_collection = None
        c_ax.errorbars.clear()
        c_ax.stems.clear()
        c_ax.scatters.clear()
        c_ax.areas.clear()
        c_ax.surfs.clear()
        c_ax.pcolors.clear()
        c_ax.histograms.clear()
        c_ax.histogram2s.clear()
        c_ax.hists.clear()
        c_ax.contours.clear()
        c_ax.heatmaps.clear()
        c_ax.cimages.clear()
        c_ax.cwordclouds.clear()
        for c_boxchart in c_ax.cboxcharts:
            for item in c_boxchart.artists:
                item.remove()
        c_ax.cboxcharts.clear()
        c_ax.quivers.clear()
        c_ax.quiver3s.clear()
        c_ax.compasss.clear()
        c_ax.feathers.clear()
        c_ax.streamlines.clear()
        # 清空数据提示标签
        if c_ax.current_mplcursor != None:
            c_ax.current_mplcursor.delete_all()

        if mw_get_cfig(c_ax.fig).current_mplcursor != None:
            mw_get_cfig(c_ax.fig).current_mplcursor.delete_all()

        c_ax.legend_order.clear()
        if not CGlobalSetting.isOnline:
            c_ax.add_pick_state_box()
        c_ax.init_ax()

        mw_legend(current_ax,display='off')
        current_ax.figure.canvas.draw()

        set_toolbutton_enabled(current_ax.figure, 'Cursor', False)

        mw_grid(current_ax,value="off")

        if mw_get_cfig(current_ax.figure).data_tips:
            mw_get_cfig(current_ax.figure).data_tips = False
            set_toolbutton_checked(current_ax.figure, 'DataTips', False)
            # button = mw_get_toolbutton(current_ax.figure, 'data_tips').setChecked(False)

        c_ax.legend = False
        c_ax.grid = False
        c_ax.cursor = False
        c_ax.colorbar_on = False

        c_ax.update_action_state()
        # print(dir(current_ax.figure.canvas.manager.toolmanager))

        from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
        if isinstance(c_ax, CAxesYyaxis):
            ax = c_ax.ax
            for c_ax in mw_get_cfig().axs:
                if c_ax.ax == current_ax or c_ax.ax2 == current_ax:
                    c_ax.ax.cla()
                    c_ax.ax2.cla()
                    c_ax.ax2.remove()
                    mw_get_cfig().axs.remove(c_ax)
                    del c_ax
                    break
            mw_update_caxe(ax.figure, ax)
            c_ax = mw_get_cax(ax)
        elif isinstance(current_ax, PolarAxes):
            c_ax.init_polaraxes()
            c_ax.init_texts()
        else:
            if not isinstance(current_ax, Axes3D):
                c_ax.init_minor_ticks()
                c_ax.init_grid_style()
            if isinstance(mw_get_cax(c_ax.ax), CAxesYyaxis):
                c_ax.init_colororder()
            c_ax.init_texts()

        for c_text in c_ax.texts:
            current_ax.figure.canvas.mpl_disconnect(c_text.draw_id)
            c_text.text.remove()
        c_ax.texts.clear()

        c_ax.connect()
    
# 清空图窗
def mw_clf(fig = None, reset = None):
    current_fig = plt.gcf() if fig == None else fig
    c_fig = mw_get_cfig(current_fig)
    if reset == None:
        c_fig.axs.clear()
        current_fig.clf()
    elif reset == 'reset':
        c_fig.axs.clear()
        current_fig.clf()
    c_fig.current_mplcursor = None
    c_fig.fig.add_artist(c_fig.pick_state)

# 清空双y轴
def mw_clear_yyaxis(ax = None):
    """
    删除清空原CAxesYyAxis对象，构建CAxes对象
    """
    from TyPlotOnline.objects.mw_figure import mw_update_caxe
    ax = plt.gca() if ax == None else ax
    # mw_cla(current_ax)
    cax = mw_get_cax_yyaxis(ax)
    if cax != None:
        ax = cax.ax
        ax2 = cax.ax2
        # mw_get_cfig().axs.remove(cax)
        # ax2.remove()
        # mw_update_caxe(ax.figure, ax)
        mw_cla(ax, 'reset')
        return ax
    else:
        mw_cla(ax, 'reset')
        return ax

# 清空帕累托图
def mw_clear_pareto(ax = None):
    """
    删除清空原CAxesPareto对象，构建CAxes对象
    """
    from TyPlotOnline.objects.mw_figure import mw_update_caxe
    current_ax = plt.gca() if ax == None else ax
    mw_cla(current_ax)
    cax = mw_get_cax(ax)
    if cax != None:
        ax = cax.ax
        ax2 = cax.ax2
        mw_get_cfig().axs.remove(cax)
        ax2.remove()
        mw_update_caxe(ax.figure, ax)
        mw_cla(ax, 'reset')
        return ax
    else:
        mw_cla(ax, 'reset')
        return ax

# 删除原坐标轴，绘制一个新的直角坐标轴
def mw_update_to_ax(ax = None):
    """
    删除原坐标轴，绘制一个新坐标轴
    """
    from TyPlotOnline.objects.mw_figure import mw_update_caxe
    from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis

    current_ax = plt.gca() if ax == None else ax
    cax = mw_get_cax(current_ax)
    if not isinstance(cax, CAxesYyaxis) and cax.hold_value == 'off':
        mw_cla(current_ax, 'reset')
        if isinstance(cax, CAxesPareto):
            current_ax = mw_clear_pareto(current_ax)
    if isinstance(current_ax, PolarAxes) or isinstance(current_ax, Axes3D):
        if cax.hold_value == 'on' and isinstance(current_ax, PolarAxes):
            return '不支持将笛卡尔绘图添加到 polaraxes。'
        current_ax.remove()
        if cax in mw_get_cfig().axs:
            mw_get_cfig().axs.remove(cax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2])
        else:
            ax_new = plt.axes()

        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new
    if current_ax in mw_get_cfig().big_axes.keys() and cax.hold_value == 'off':
        mw_clear_matrix(current_ax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2])
        else:
            ax_new = plt.axes()
        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new

    return None

# 删除原坐标轴，绘制一个新的极坐标轴
def mw_update_to_polarax(ax = None):
    """
    删除原坐标轴，绘制一个新坐标轴
    """
    from TyPlotOnline.objects.mw_figure import mw_update_caxe

    current_ax = plt.gca() if ax == None else ax
    cax = mw_get_cax(current_ax)
    if cax.hold_value == 'off':
        mw_cla(current_ax, 'reset')
    if current_ax in mw_get_cfig().big_axes.keys() and cax.hold_value == 'off':
        mw_clear_matrix(current_ax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2])
        else:
            ax_new = plt.axes()
        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new
    if isinstance(current_ax, Axes) and not isinstance(current_ax, PolarAxes):
        if cax.hold_value == 'on':
            return '不支持将极坐标图添加到 axes。'
        current_ax = cax.ax
        current_ax.remove()
        if cax in mw_get_cfig().axs:
            mw_get_cfig().axs.remove(cax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2], projection="polar")
        else:
            ax_new = plt.axes(projection="polar")
        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new

    return None

# 删除原坐标轴，绘制一个新的三维坐标轴
def mw_update_to_ax3d(ax = None):
    """
    删除原坐标轴，绘制一个新坐标轴
    """
    from TyPlotOnline.objects.mw_figure import mw_update_caxe
    current_ax = plt.gca() if ax == None else ax
    cax = mw_get_cax(current_ax)
    if cax.hold_value == 'off':
        mw_cla(current_ax, 'reset')
    if current_ax in mw_get_cfig().big_axes.keys() and cax.hold_value == 'off':
        mw_clear_matrix(current_ax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2])
        else:
            ax_new = plt.axes()
        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new
    if isinstance(current_ax, Axes) and not isinstance(current_ax, Axes3D):
        if cax.hold_value == 'on' and isinstance(current_ax, PolarAxes):
            return '不支持将笛卡尔绘图添加到 polaraxes。'
        current_ax = cax.ax
        current_ax.remove()
        if cax in mw_get_cfig().axs:
            mw_get_cfig().axs.remove(cax)
        if isinstance(current_ax, SubplotBase):
            pos = current_ax.get_geometry()
            ax_new = plt.subplot(pos[0], pos[1], pos[2], projection = "3d")
        else:
            ax_new = plt.axes(projection="3d")

        mw_update_caxe(ax_new.figure, ax_new)
        return ax_new

    return None

def update_view(fig = None):
    if fig == None:
        fig = plt.gcf()

    fig.canvas.draw_idle()

# 刷新图例
def update_legend(ax):
    legend = None
    c_ax=mw_get_cax(ax)
    if len(c_ax.legends)!=0:
        legend = c_ax.legends[0]
    if not legend:
        ax.figure.canvas.draw_idle()
        return
    else:
        # from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
        # if isinstance(c_ax, CAxesPareto):
        #     legend.draw(ax.figure._cachedRenderer)
        # else:
        legend.set_ncol()

    ax.figure.canvas.draw_idle()

# 命令kwargs缩写处理
def mw_normalize_kwargs(type, **kwargs):
    if type == "line":
        kwargs = cbook.normalize_kwargs(kwargs, Line2D)
    elif type == "bar":
        kwargs = cbook.normalize_kwargs(kwargs, Patch)
    elif type in ['surf', 'area', 'bar3','quiver','quiver3','streamline','compass','feather']:
        kwargs = cbook.normalize_kwargs(kwargs, Collection)

    return kwargs

# 对kwargs的特殊值进行处理
def pop_special_kwargs(lst_key, **kwargs):
    """
    处理facecolor、edgecolor、facealpha、edgealpha、linestyle等
    ----------------------------------
    lst_key: 需要处理的key值
    """
    special_kwargs = dict()
    if 'facecolor' in kwargs:
        special_kwargs['facecolor'] = kwargs['facecolor']
    elif 'facecolors' in kwargs and 'facecolors' in lst_key:
        special_kwargs['facecolors'] = kwargs['facecolors']
    elif 'markerfacecolor' in kwargs and 'markerfacecolor' in lst_key:
        special_kwargs['markerfacecolor'] = kwargs['markerfacecolor']

    if 'edgecolor' in kwargs:
        special_kwargs['edgecolor'] = kwargs['edgecolor']
    elif 'edgecolors' in kwargs and 'edgecolors' in lst_key:
        special_kwargs['edgecolors'] = kwargs['edgecolors']
    elif 'markeredgecolor' in kwargs and 'markeredgecolor' in lst_key:
        special_kwargs['markeredgecolor'] = kwargs['markeredgecolor']

    alpha = kwargs.pop('alpha', '')
    facealpha = kwargs.pop('facealpha', '')
    if facealpha == '':
        if alpha != '':
            special_kwargs['facealpha'] = alpha
        else:
            special_kwargs['facealpha'] = 1
    else:
        special_kwargs['facealpha'] = facealpha
    edgealpha = kwargs.pop('edgealpha', '')
    if edgealpha == '':
        if alpha != '':
            special_kwargs['edgealpha'] = alpha
        else:
            special_kwargs['edgealpha'] = 1
    else:
        special_kwargs['edgealpha'] = edgealpha
    linestyle = kwargs.pop('linestyle', 'a')
    if linestyle == 'a':
        special_kwargs['linestyle'] = '-'
    else:
        special_kwargs['linestyle'] = linestyle
    # if linestyle not in ['', 'none']:
    #     kwargs['linestyle'] = linestyle

    return special_kwargs, kwargs

# 获取不重复的图例名
def mw_get_unique_legend_name(ax, obj):
    c_ax = mw_get_cax(ax)

    for num in range(1,1000):
        s = "data" + str(num)
        if s not in c_ax.legend_order.values():
            c_ax.legend_order[obj] = s
            return s

# 设置图例名
def mw_set_legend_name(ax, handles = [], labels = []):
    c_ax = mw_get_cax(ax)

    if handles:
        for (h, label) in zip(handles, labels):
            for key in c_ax.legend_order.keys():
                if h == key:
                    key.set_label(label)
                    c_ax.legend_order[key] = label
                elif type(key) == BarContainer:
                    children = key.get_children()
                    if handles == children:
                        key.set_label(label)
                        c_ax.legend_order[key] = label
    else:
        for (label, key) in zip(labels, c_ax.legend_order.keys()):
            key.set_label(label)
            c_ax.legend_order[key] = label

def mw_set_legend_names(lst_ax, handles = [], labels = []):
    index = 0
    if handles:
        length = len(handles)
        for i in range(index, length):
            h = handles[i]
            label = labels[i]
            for ax in lst_ax:
                c_ax = mw_get_cax(ax, True)
                for key in c_ax.legend_order.keys():
                    if h == key:
                        key.set_label(label)
                        c_ax.legend_order[key] = label
                    elif type(key) == BarContainer:
                        children = key.get_children()
                        if handles == children:
                            key.set_label(label)
                            c_ax.legend_order[key] = label
    else:
        length = len(labels)
        for i in range(index, length):
            label = labels[i]
            for ax in lst_ax:
                c_ax = mw_get_cax(ax, True)
                for key in c_ax.legend_order.keys():
                    key.set_label(label)
                    c_ax.legend_order[key] = label


def get_label_list(kwargs):
    for k, v in kwargs.items():
        if k == 'label':
            return v
    return None

def mw_set_plot_path(path):
    CGlobalSetting.cGlobalPlotPath = path + "python"
    CGlobalSetting.icon_path = CGlobalSetting.cGlobalPlotPath + "/resources/icon/"

def mw_set_current_geo_path(path):
    CGlobalSetting.current_geo_path = path + "python"

def mw_dudate_bar_width(bars, old_width, new_width, category = 'v'):
    change = new_width / old_width

    if category == 'v':
        for _bar in bars:
            x = _bar.get_x()
            current_width = _bar.get_width()
            new_width = current_width * change
            change_width = new_width - current_width
            new_x = x - change_width / 2

            _bar.set_x(new_x)
            _bar.set_width(new_width)
    else:
        for _bar in bars:
            y = _bar.get_y()
            current_height = _bar.get_height()
            new_height = current_height * change
            change_width = new_height - current_height
            new_y = y - change_width / 2

            _bar.set_y(new_y)
            _bar.set_height(new_height)

def ticks_auto(ax, axis):
    formatter = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    #formatter = matplotlib.ticker.StrMethodFormatter('{x}')
    if axis in ['x', 'both']:
        ax.xaxis.set_major_formatter(formatter)
    if axis in ['y', 'both']:
        ax.yaxis.set_major_formatter(formatter)
    if axis in ['z', 'both']:
        ax.zaxis.set_major_formatter(formatter)

def show_label(ax, axis):
    if axis in ['X','Both']:
        ax.get_xaxis().get_label().set_visible(True)
    if axis in ['Y','Both']:
        ax.get_yaxis().get_label().set_visible(True)
    if axis in ['Z','Both'] and isinstance(ax, Axes3D):
        ax.get_zaxis().get_label().set_visible(True)

def hide_label(ax, axis):
    if axis == 'X':
        ax.get_xaxis().get_label().set_visible(False)
    elif axis == 'Y':
        ax.get_yaxis().get_label().set_visible(False)
    elif axis == 'Z' and isinstance(ax, Axes3D):
        ax.get_zaxis().get_label().set_visible(False)

# 处理无限参数的函数，将参数转化为x,y,fmt三者的list集合
def _process_args(ax, *args):
    res = []

    if len(args) == 1:
        lst = []
        y = args[0]
        lst.append(y)
        res.append(lst)
    elif len(args) == 2:
        lst = []
        if isinstance(args[0], (list, np.ndarray,range)) and isinstance(args[1], (list, np.ndarray)):
            x = args[0]
            y = args[1]
            fmt = ""
            lst.append(x)
            lst.append(y)
            lst.append(fmt)
            res.append(lst)
        elif isinstance(args[0], (list, np.ndarray,range)) and isinstance(args[1], str):
            y = args[0]
            fmt = args[1]
            lst.append(y)
            lst.append(fmt)
            res.append(lst)
    else:
        while args and not isinstance(args[0], str):
            lst = []
            x, y, *args = args
            fmt = ""
            if args and isinstance(args[0], str):
                fmt, *args = args
            lst.append(x)
            lst.append(y)
            lst.append(fmt)
            res.append(lst)

    return res

# 提取参数中的linewidth
def mw_get_linewidth(**kwargs):
    normalize_kwargs = mw_normalize_kwargs('surf', **kwargs)
    linewidth = normalize_kwargs.pop('linewidth','')
    return linewidth

def mw_colorbar(ax, obj, **kwargs):
    if obj.colorbar != None:
        c_ax = mw_get_cax(ax)
        c_ax.colorbar = obj.colorbar
        c_ax.colorbar_on = True
        return

    if isinstance(obj,QuadContourSet):
        return
    fig = ax.figure
    c_ax = mw_get_cax(ax)
    original_pos = ax.get_position(original = True)
    c_ax.original_pos = original_pos
    # obj._is_filled = False
    # obj._is_stroked = False

    pos = ax.get_position()
    length_1 = pos.x1 - pos.x0
    length_2 = 0.043

    fraction = (0.9 - length_1 + length_2)/2
    cb = fig.colorbar(obj, ax = ax, fraction = fraction, **kwargs)

    current_pos = ax.get_position()
    c_ax.current_pos = current_pos
    c_ax.colorbar = cb

    c_ax.colorbar_on = True

    set_toolbutton_checked(ax.figure, 'Colorbar', True)

    return cb

def mw_remove_colorbar(current_fig, current_ax):
    fig = plt.gcf() if current_fig is None else current_fig
    ax = fig.gca() if current_ax is None else current_ax

    c_ax = mw_get_cax(ax)

    if c_ax.colorbar != None:
        ax.set_position(c_ax.original_pos)
        c_ax.original_pos = None
        c_ax.current_pos = None
        #在选中状态下关闭colorbar时,更新current_objs
        c_colorbar = mw_get_ccolorbar(c_ax.colorbar )
        if c_colorbar in mw_get_cfig().current_objs:
            mw_get_cfig().current_objs.remove(c_colorbar)

        c_ax.colorbar.remove()
        c_ax.colorbar = None

        ax.set_anchor('C')
        if not CGlobalSetting.isOnline:
            subplots = SubplotToolQt(fig, fig.canvas.parent())
            subplots._reset()
            del subplots

    c_ax.colorbar_on = False

    set_toolbutton_checked(ax.figure, 'Colorbar', False)

# 获取图例名（内部函数）
def _get_legend_name(height, labels):
    # 设置默认图例名
    dim = np.shape(height)
    count = 0
    if len(dim) == 1:
        count = 1
    else:
        count = dim[1]

    for i in range(0,count):
        _get_unique_name(labels)

    return labels

# 获取唯一标识名（内部函数）
def _get_unique_name(lst_num):
    for num in range(1,101):
        s = "data" + str(num)
        if s not in lst_num:
            lst_num.append(s)
            return s
    return None

# 调整界面位置
def adjust_views(figure = None, adjust = False):
    """
    在界面进行如下操作后，调整坐标轴的位置，保证对象都处于界面之内
    1.修改坐标轴的字体大小
    2.调整界面大小
    """
    fig = plt.gcf() if figure is None else figure
    if fig.get_axes() == []:
        return
    if mw_get_cfig(fig).auto_adjust_view or adjust:
        fig.tight_layout(rect = (0.13,0.11,0.905,0.925))

    fig.canvas.draw_idle()

# 获取cmap颜色序列
def get_cmap_colors(cmap, N = 256):
    """
    根据cmap名称或者cmap对象获取长度为N的颜色序列
    """
    if isinstance(cmap, colors.ListedColormap):
        cmap = cmap.name

    if isinstance(cmap,str):
        if cmap == 'parula':
            cmap = get_parula(N)
            return np.asarray(cmap.colors)
        elif cmap == 'flag':
            cmap = get_flag(N)
            return np.asarray(cmap.colors)
        elif cmap == 'lines':
            cmap = get_lines(N)
            return np.asarray(cmap.colors)
        elif cmap == 'prism':
            cmap = get_prism(N)
            return np.asarray(cmap.colors)

    cmap = cm.get_cmap(cmap, N)
    array = np.array(range(0,N))

    rgba = cmap(array)
    rgb = rgba[:,range(0,3)]
    return np.asarray(rgb)

# 坐标转换相关函数
def mw_display_to_figure(figure, pos):
    return tuple(figure.transFigure.inverted().transform(pos))

def mw_figure_to_display(figure, pos):
    return tuple(figure.transFigure.transform(pos))

def mw_display_to_axes(axes, pos):
    return tuple(axes.transAxes.inverted().transform(pos))

def mw_axes_to_display(axes, pos):
    return tuple(axes.transAxes.transform(pos))

def mw_display_to_data(axes, pos):
    return tuple(axes.transData.inverted().transform(pos))

def mw_data_to_display(axes, pos):
    return tuple(axes.transData.transform(pos))

def mw_display_to_inches(figure, pos):
    return tuple(figure.dpi_scale_trans.inverted().transform(pos))

def mw_inches_to_display(figure, pos):
    return tuple(figure.dpi_scale_trans.transform(pos))

#笛卡尔坐标转球坐标
def cart2sph(x, y, z):
   theta = np.arctan2(y, x)
   phi = np.arctan2 (z, np.sqrt (x * x + y * y))
   r = np.sqrt(x * x + y * y + z * z)

   return  theta, phi, r

#球坐标转笛卡尔坐标
def sph2cart(theta, phi, r):
    x = r * np.cos (phi) * np.cos (theta)
    y = r * np.cos (phi) * np.sin (theta)
    z = r * np.sin (phi)

    return x, y, z

def IsAxes3d(ax):
    if isinstance(ax, Axes3D):
        return True

    return False


def IsAxes(ax):
    if isinstance(ax, Axes):
        return True

    return False

def IsPolarAxes(ax):
    if isinstance(ax, PolarAxes):
        return True

    return False

def DelAxes(cax):
    fig = plt.gcf()
    cfig = mw_get_cfig(fig)
    if cax in cfig.axs:
        cfig.axs.remove(cax)

def change_autoscalex(ax, auto = True, not_change_lst = []):
    lst_ax = [ax]
    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    cax = mw_get_cax()
    if isinstance(cax, CAxesYyaxis):
        lst_ax.clear()
        lst_ax.append(cax.ax)
        lst_ax.append(cax.ax2)

    auto_false_lst = []
    for i in range(0, len(lst_ax)):
        _ax = lst_ax[i]
        _auto_false_lst = []
        if len(not_change_lst) == 0 or 'X' not in not_change_lst[i]:
            if _ax.get_autoscalex_on() != auto:
                _ax.set_autoscalex_on(auto)
            else:
                _auto_false_lst.append('X')

        if len(not_change_lst) == 0 or 'Y' not in not_change_lst[i]:
            if _ax.get_autoscaley_on() != auto:
                _ax.set_autoscaley_on(auto)
            else:
                _auto_false_lst.append('Y')

        if isinstance(_ax, Axes3D):
            if len(not_change_lst) == 0 or 'Z' not in not_change_lst[i]:
                if _ax.get_autoscalez_on() != auto:
                    _ax.set_autoscalez_on(auto)
                    _auto_false_lst.append('Z')
        auto_false_lst.append(_auto_false_lst)

    return auto_false_lst

dict_font_windows = {
    '仿宋' : 'FangSong',
    '华文中宋' : 'STZhongsong',
    '华文仿宋' : 'STFangsong',
    '华文宋体' : 'STSong',
    '华文彩云' : 'STCaiyun',
    '华文新魏' : 'STXinwei',
    '华文楷体' : 'STKaiti',
    '华文琥珀' : 'STHupo',
    '华文细黑' : 'STXihei',
    '华文行楷' : 'STXingkai',
    '华文隶书' : 'STLiti',
    '宋体' : 'SimSun',
    '幼圆' : 'YouYuan',
    '微软雅黑' : 'Microsoft YaHei',
    '方正舒体' : 'FZShuTi',
    '方正姚体' : 'FZYaoTi',
    '楷体' : 'KaiTi',
    '等线' : 'DengXian',
    '隶书' : 'LiSu',
    '黑体' : 'SimHei',
}

dict_font_windows_reverse = {
    'FangSong' : '仿宋',
    'STZhongsong' : '华文中宋',
    'STFangsong' : '华文仿宋',
    'STSong' : '华文宋体',
    'STCaiyun' : '华文彩云',
    'STXinwei' : '华文新魏',
    'STKaiti' : '华文楷体',
    'STHupo' : '华文琥珀',
    'STXihei' : '华文细黑',
    'STXingkai' : '华文行楷',
    'STLiti' : '华文隶书',
    'SimSun' : '宋体',
    'YouYuan' : '幼圆',
    'Microsoft YaHei' : '微软雅黑',
    'FZShuTi' : '方正舒体',
    'FZYaoTi' : '方正姚体',
    'KaiTi' : '楷体',
    'DengXian' : '等线',
    'LiSu' : '隶书',
    'SimHei' : '黑体',
}

dict_font_linux  = {
    '等线' : 'X-xiheiti_Noncommercial',
    '方正宋体' : 'FZSongS-Extended',
    '微软雅黑' : 'Microsoft YaHei',
    '方正仿宋' : 'FZFangSong-Z02',
    '方正黑体' : 'FZHei-B01',
}

dict_font_linux_reverse  = {
    'X-xiheiti_Noncommercial' : '等线',
    'FZSongS-Extended' : '方正宋体',
    'Microsoft YaHei' : '微软雅黑',
    'FZFangSong-Z02' : '方正仿宋',
    'FZHei-B01' : '方正黑体',
}

def get_font_lst():
    if CGlobalSetting.CGlobalPlatformVersion == "Windows":
        chiese_font_dict = dict_font_windows
    else:
        chiese_font_dict = dict_font_linux
    lst_family = list(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))
    lst_family_chiese = list(chiese_font_dict.keys())
    lst_family = lst_family + lst_family_chiese

    lst_family_delete = ['jdiconfontD', 'jdiconfontC', 'jdiconfontB', 'jdiconfontA',
        'jdIcoMoonFree', 'jdIcoFont', 'jdFontCustom', 'jdFontAwesome', 'cmtt10',
        'cmsy10', 'cmss10', 'cmr10', 'cmmi10', 'cmex10', 'cmb10', 'ZWAdobeF',
        'Bookshelf Symbol 7', 'Wingdings 3', 'Wingdings 2', 'Wingdings', 
        # 'FangSong','STZhongsong', 'STFangsong', 'STSong', 'STCaiyun', 'STXinwei', 'STKaiti',
        # 'STHupo', 'STXihei', 'STXingkai', 'STLiti', 'SimSun', 'YouYuan', 'Microsoft YaHei',
        # 'FZShuTi', 'FZYaoTi', 'KaiTi', 'DengXian', 'LiSu', 'SimHei',
        'DejaVu Sans Display', 'DejaVu Serif Display', 'Euclid Extra', 'Euclid Math One',
        'Euclid Math Two', 'Euclid Symbol', 'HoloLens MDL2 Assets', 'JdIonicons',
        'MS Outlook', 'MS Reference Specialty', 'MT Extra', 'MT Extra Tiger', 'Marlett',
        'Origin', 'STIXNonUnicode', 'STIXSizeFiveSym', 'STIXSizeFourSym', 'STIXSizeOneSym',
        'STIXSizeThreeSym', 'STIXSizeTwoSym', 'Segoe MDL2 Assets', 'Symbol', 'Symbol Tiger',
        'Symbol Tiger Expert', 'Webdings', 'Lohit Assamese', 'Lohit Bengali', 'Lohit Devanagari',
        'Lohit Gujarati', 'Lohit Kannada', 'Lohit Nalayalam', 'Lohit Marathi', 'Lohit Napali',
        'Lohit Oriya', 'Lohit Punjabi', 'Lohit Tamil', 'Lohit Telugu', 'Madan2', 'Noto Emoji']

    for delete_family in lst_family_delete:
        if delete_family in lst_family:
            lst_family.remove(delete_family)

    lst_family.sort()
    return lst_family

def get_chinese_name(real_name):
    if real_name in dict_font_linux_reverse:
        return dict_font_linux_reverse[real_name]

    return real_name


def get_real_name(chinese_name):
    if chinese_name in dict_font_linux:
        return dict_font_linux[chinese_name]
    return chinese_name

def set_ax_colororder(ax, newcolors):
    #ax.set_prop_cycle(color = newcolors)
    cax = mw_get_cax(ax, True)
    cax.colororder = newcolors
    cax.init_colororder()
    len_color = len(newcolors)

    lines = cax.get_all_lines()
    for i in range(0, len(lines)):
        index = i % len_color
        lines[i].set_color(newcolors[index])

    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    if isinstance(mw_get_cax(ax), CAxesYyaxis):
        for i in range(0, len(lines)):
            lines[i].set_linestyle(cax.lst_linestyle[i])
            lines[i].set_marker(cax.lst_marker[i])

    for i in range(0, len(cax.bar_containers)):
        index = i % len_color
        for bar in cax.bar_containers[i].bars:
            bar.set_facecolor(newcolors[index])
        cax.bar_containers[i].facecolor = newcolors[index]

    for i in range(0, len(cax.errorbars)):
        index = i % len_color
        cax.errorbars[i].data_line.set_color(newcolors[index])
        for capline in cax.errorbars[i].caplines:
            capline.set_color(newcolors[index])
        for barcol in cax.errorbars[i].barcols:
            barcol.set_color(newcolors[index])

    stems = cax.get_all_stems()
    for i in range(0, len(cax.stems)):
        index = i % len_color
        cax.stems[i].markerline.set_color(newcolors[index])
        cax.stems[i].stemlines.set_color(newcolors[index])

    for i in range(0, len(cax.scatters)):
        index = i % len_color
        if cax.scatters[i].facecolor is not None:
            cax.scatters[i].path_collection.set_facecolor(newcolors[index])
            cax.scatters[i].facecolor = newcolors[index]
        if cax.scatters[i].edgecolor is not None:
            cax.scatters[i].path_collection.set_edgecolor(newcolors[index])
            cax.scatters[i].edgecolor = newcolors[index]
        cax.scatters[i].facecolor = newcolors[index]

    for i in range(0, len(cax.histograms)):
        index = i % len_color
        for bar in cax.histograms.bars[i]:
            bar.set_facecolor(newcolors[index])
        cax.histograms[i].facecolor = newcolors[index]

def set_colororder(obj, newcolors):
    if newcolors == "default":
        newcolors = [(0.00,0.45,0.74),(0.85,0.33,0.10),(0.93,0.69,0.13),
            (0.49,0.18,0.56),(0.47,0.67,0.19),(0.30,0.75,0.93),(0.64,0.08,0.18)]
    else:
        newcolors = np.asarray(newcolors)

    from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
    if isinstance(obj, Figure):
        mw_get_cfig(obj).colororder = newcolors
        for cax in mw_get_cfig(obj).axs:
            if isinstance(cax, CAxesYyaxis):
                ax = cax.cur_ax
            else:
                ax = cax.ax
            set_ax_colororder(ax, newcolors)
    elif isinstance(obj, Axes):
        mw_get_cax(obj).colororder = newcolors
        set_ax_colororder(obj, newcolors)

def get_ax_colororder(ax):
    return ax._get_lines.prop_cycler_data.by_key()['color']

def get_colororder(obj):
    if isinstance(obj, Figure):
        return mw_get_cfig(obj).colororder
    elif isinstance(obj, Axes):
        return mw_get_cax(obj, True).colororder

def str_remove_zeros(str):
    if '.' in str and 'e' not in str:
        result_str = str.rstrip('0').rstrip('.')
        return result_str
    else:
        return str

def mw_get_keyvalue(key1, key2, **kwargs):
    flag1 = False
    flag2 = False
    res = None

    for k, v in kwargs.items():
        if k == key1:
            flag1 = True
            res = v
        if k == key2:
            flag2 = True
            res = v

    if flag1 and flag2:
        flag = False
    else:
        flag = True
    return flag, res

def mw_get_value(key, **kwargs):
    res = None

    for k, v in kwargs.items():
        if k == key:
            res = v

    return res

# 设置对象的cmap,同时处理_original_edgecolor
def mw_set_obj_cmap(obj, cmap):
    c_obj = mw_get_cobj(obj)
    if c_obj == None:
        return

    obj.set_cmap(cmap)
    if isinstance(obj, PolyCollection):
        pass
    else:
        if hasattr(c_obj,"facecolor") and c_obj.facecolor == 'flat':
            obj._facecolor3d = obj.to_rgba(obj._A, c_obj.facealpha)
            obj._original_facecolor = obj._facecolor3d

        if hasattr(c_obj,"edgecolor") and c_obj.edgecolor == 'flat':
            obj._edgecolor3d = obj.to_rgba(obj._A, c_obj.edgealpha)
            obj._original_edgecolor = obj._edgecolor3d

    update_legend(obj.axes)

# 刷新绘图工具栏状态
def update_draw_button_status(figure, current_btn):
    # draw_btns = ['draw_line', 'draw_arrow', 'draw_double_arrow', 'draw_text_arrow',
    #             'draw_text', 'draw_rect', 'draw_ellipse']
    draw_btns = ['DrawLine', 'DrawArrow', 'DrawDoubleArrow', 'DrawTextArrow',
                'DrawText', 'DrawRect', 'DrawEllipse']
    for draw_btn in draw_btns:
        if current_btn == draw_btn:
            continue
        
        set_toolbutton_checked(figure, draw_btn, False)
        cfig = mw_get_cfig(figure)
        cfig.drawing = False
        cfig.draw_graphics = None
        figure.canvas.send_event("cursor", cursor = "default")
        # button = mw_get_toolbutton(figure, draw_btn)
        # if button.isChecked():
        #     button.setChecked(False)

# 刷新函数，用于动画效果的对象统一刷新
def update_all(fig):
    data_tips = mw_get_cfig().current_mplcursor
    if data_tips.background is not None:
        data_tips.canvas.restore_region(data_tips.background)
    if data_tips.hover_point != None:
        data_tips.ax.draw_artist(data_tips.hover_point)
    if data_tips.hover_annotate != None:
        data_tips.ax.draw_artist(data_tips.hover_annotate)

    data_tips.draw_self()

    for i in range(0, mw_get_cfig().cursor_lines.__len__())[::-1]:
        cursor_line = mw_get_cfig().cursor_lines[i]
        cursor_line.draw_self()

    for cax in mw_get_cfig().get_all_caxes():
        # for title in cax.titles:
        #     title.draw_self()
        # for xlabel in cax.xlabels:
        #     xlabel.draw_self()
        # for ylabel in cax.ylabels:
        #     ylabel.draw_self()
        # for zlabel in cax.zlabels:
        #     zlabel.draw_self()
        # for legend in cax.legends:
        #     legend.draw_self()
        for text in cax.texts:
            text.draw_self()


    for drect in mw_get_cfig().lst_draw_graphics:
        drect.draw_self()

    for dline in mw_get_cfig().draw_lines:
        dline.draw_self()

    fig.canvas.blit(fig.bbox)
    fig.canvas.manager.refresh_all()

# 禁用工具栏快捷键
def disable_keymap():
    plt.rcParams["keymap.save"] = ''

# 启用工具栏快捷键
def enable_keymap():
    plt.rcParams["keymap.save"] = ['s','ctrl+s']


# 获取figure默认ax的position
def mw_get_default_ax_pos():
    return CGlobalSetting.c_ax_pos_lst

# 获取默认的精度
def mw_get_default_precision():
    return CGlobalSetting.precision

# 禁用或开启工具栏所有功能
def mw_enable_toolbar(fig, enable = True):
    fig.canvas.manager.toolbar.setEnabled(enable)

# 将散点图矩阵的大坐标轴存入figure
def mw_set_big_ax(bigax, matrix_axes):
    cfig = mw_get_cfig(bigax.figure)
    if cfig != None:
        cfig.big_axes[bigax] = matrix_axes

# 清空散点图矩阵
def mw_clear_matrix(bigax):
    cfig = mw_get_cfig(bigax.figure)
    if cfig == None:
        return

    if bigax in cfig.big_axes.keys():
        matrix_axes = cfig.big_axes.pop(bigax)
        for ax in matrix_axes:
            cax = mw_get_cax(ax)
            mw_cla(ax, "reset")
            ax.remove()
            if cax in mw_get_cfig().axs:
                mw_get_cfig().axs.remove(cax)
    cbigax = mw_get_cax(bigax)
    mw_cla(bigax, "reset")
    bigax.remove()
    if cax in mw_get_cfig().axs:
        mw_get_cfig().axs.remove(cbigax)


def mw_get_platform():
    return CGlobalSetting.CGlobalPlatformVersion


def mw_print(file_name, printer_name = None):
    if CGlobalSetting.CGlobalPlatformVersion != "Windows":
        raise Exception('该功能只支持Windows操作系统，其余操作系统的支持正在开发中...')

    import win32print
    import win32ui
    from PIL import Image, ImageWin

    #
    # Constants for GetDeviceCaps
    #
    #
    # HORZRES / VERTRES = printable area
    #
    HORZRES = 8
    VERTRES = 10
    #
    # LOGPIXELS = dots per inch
    #
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    #
    # PHYSICALWIDTH/HEIGHT = total area
    #
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    #
    # PHYSICALOFFSETX/Y = left / top margin
    #
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113

    if printer_name == None:
        printer_name = win32print.GetDefaultPrinter ()

    #
    # You can only write a Device-independent bitmap
    # directly to a Windows device context; therefore
    # we need (for ease) to use the Python Imaging
    # Library to manipulate the image.
    #
    # Create a device context from a named printer
    # and assess the printable size of the paper.
    #
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    #
    # Open the image, rotate it if it's wider than
    # it is high, and work out how much to multiply
    # each pixel by to get it as big as possible on
    # the page without distorting.
    #
    bmp = Image.open (file_name)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min (ratios)

    #
    # Start the print job, and draw the bitmap to
    # the printer device at the scaled size.
    #
    hDC.StartDoc (file_name)
    hDC.StartPage ()

    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()

def mw_im(filename):
    import matplotlib.image as im
    # 打开图片
    # file_name = r"E:\Projects\MwSyslab\branches\Library\TyPlot/Figure_1.png"
    arr = im.imread(filename)
    return arr


def mw_findobj(obj, type = None, string = None):
    c_obj = mw_get_cobj(obj)
    if c_obj == None:
        return []

    from TyPlotOnline.objects.mw_figure import CFigure
    from TyPlotOnline.objects.mw_axes import CAxes
    from TyPlotOnline.objects.mw_axes_3d import CAxes3D

    if type == None:
        if string == None:
            if isinstance(c_obj, CFigure):
                lst_cax = c_obj.get_all_caxes()
                res = []
                for cax in lst_cax:
                    res.extend(cax.get_all_objs())
                return res
            elif isinstance(c_obj, (CAxes, CAxes3D)):
                res = c_obj.get_all_objs()
                return res
            else:
                return []
        else:
            if isinstance(c_obj, CFigure):
                lst_cax = c_obj.get_all_caxes()
                res = []
                for cax in lst_cax:
                    lst1 = get_obj(obj, type="text")
                    res.extend(lst1)
                    lst2 = get_obj(obj, type="label")
                    res.extend(lst2)
                return res
            elif isinstance(c_obj, (CAxes, CAxes3D)):
                res = []
                lst1 = get_obj(c_obj, type="text")
                lst2 = get_obj(c_obj, type="label")

                for l in lst1:
                    if string in l.get_text():
                        res.append(l)

                for l in lst2:
                    if string in l.get_text():
                        res.append(l)
                return res
            else:
                return []
    else:
        if isinstance(c_obj, CFigure):
            lst_cax = c_obj.get_all_caxes()
            res = []
            for cax in lst_cax:
                res.extend(get_obj(cax, type=type))
            return res
        elif isinstance(c_obj, (CAxes, CAxes3D)):
            return get_obj(c_obj, type=type)
        else:
            return []

def get_obj(obj, type="line"):
    if type == "line":
        return obj.get_all_lines()
    elif type == "area":
        return obj.get_all_areas()
    elif type == "boxchart":
        return obj.get_all_cboxcharts()
    elif type == "contour":
        return obj.get_all_contours()
    elif type == "feather":
        return obj.get_all_feathers()
    elif type == "histogram":
        return obj.get_all_histograms()
    elif type == "patch":
        return obj.get_all_patchs()
    elif type == "quiver":
        return obj.get_all_quivers()
    elif type == "stem":
        return obj.get_all_stems()
    elif type == "bar3":
        return obj.get_all_bar3s()
    elif type == "image":
        return obj.get_all_cimages()
    elif type == "wordcloud":
        return obj.get_all_cwordclouds()
    elif type == "fimplicitline":
        return obj.get_all_fimplicitlines()
    elif type == "hist":
        return obj.get_all_hists()
    elif type == "pie":
        return obj.get_all_pies()
    elif type == "rectangle":
        return obj.get_all_rectangles()
    elif type == "streamline":
        return obj.get_all_streamlines()
    elif type == "bar":
        return obj.get_all_bars()
    elif type == "compass":
        return obj.get_all_compasss()
    elif type == "errorbar":
        return obj.get_all_errorbar()
    elif type == "heatmap":
        return obj.get_all_heatmaps()
    elif type == "quiver3":
        return obj.get_all_quiver3s()
    elif type == "scatter":
        return obj.get_all_scatters()
    elif type == "surf":
        return obj.get_all_surfs()
    elif type == "text":
        return obj.get_all_texts()
    elif type == "label":
        return obj.get_all_labels()



def mw_set_alpha(obj, value, **kwargs):
    from TyPlotOnline.objects.mw_stem3 import StemContainer3
    from TyPlotOnline.objects.mw_quiver import MWQuiver
    from TyPlotOnline.objects.mw_compass import MWCompass
    from TyPlotOnline.objects.mw_feather import MWFeather

    if isinstance(obj, Axes):
        # 处理坐标轴内对象
        c_ax = mw_get_cax(obj)
        if c_ax.bar_containers != None:
            for bar in c_ax.bar_containers:
                # c_bar = mw_get_cbar(bar)
                bar.set_facealpha(value)

        if c_ax.bar3_containers != None:
            for bar in c_ax.bar3_containers:
                # c_bar = mw_get_cbar3(bar)
                bar.set_facealpha(value)

        if c_ax.pies != None:
            for pie in c_ax.pies:
                # c_pie = mw_get_cpie(pie)
                pie.set_facealpha(value)

        if c_ax.scatters != None:
            for scatter in c_ax.scatters:
                # c_scatter = mw_get_cbar(scatter)
                scatter.set_facealpha(value)

        if c_ax.areas != None:
            for area in c_ax.areas:
                # c_area = mw_get_carea(area)
                area.set_facealpha(value)

        if c_ax.surfs != None:
            for surf in c_ax.surfs:
                # c_surf = mw_get_csurf(surf)
                surf.set_facealpha(value)

        if c_ax.cimages != None:
            for image in c_ax.cimages:
                # c_image = mw_get_carea(image)
                image.set_facealpha(value)

        if c_ax.patchs != None:
            for patch in c_ax.patchs:
                # c_patch = mw_get_cpatch(patch)
                patch.set_facealpha(value)

    elif isinstance(obj, Line2D):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, Line3DCollection):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, ErrorbarContainer):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, StemContainer) or isinstance(obj, StemContainer3):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, Tuple):
        if isinstance(obj[0], Rectangle):
            c_bar = mw_get_cbar(obj)
            c_bar.set_facealpha(value)
        elif isinstance(obj[0][0], Wedge):
            for p in obj[0]:
                c_pie = mw_get_cpie(p)
                c_pie.set_facealpha(value)
        elif isinstance(obj[2][0], Rectangle):
            c_histogram = mw_get_chistogram(obj[2])
            c_histogram.set_facealpha(value)

    elif isinstance(obj, PathCollection):
        c_scatter = mw_get_cscatter(obj)
        c_scatter.set_facealpha(value)
        update_legend(obj.axes)
    elif isinstance(obj, Poly3DCollection):
        c_surf = mw_get_csurf(obj)
        c_surf.set_facealpha(value)
        update_legend(obj.axes)
    elif isinstance(obj, MWCompass):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, MWFeather):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, MWQuiver):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, PolyCollection):
        c_area = mw_get_carea(obj)
        c_area.set_facealpha(value)
        update_legend(obj.axes)
    elif isinstance(obj, ContourSet):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, AxesImage):
        obj.set_alpha(value)
    elif isinstance(obj, Annotation):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, Text):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, Patch):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, mlegend.Legend):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif isinstance(obj, Colorbar):
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif obj.__class__.__name__ == "CGeoBubble":
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif obj.__class__.__name__ == "CGeoDensity":
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif obj.__class__.__name__ == "CBoxChart":
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif obj.__class__.__name__ == "CWordCloud":
        raise Exception('alpha 命令与指定的对象不兼容。')
    elif obj.__class__.__name__ == "PatchCollection":
        if mw_get_crectangle(obj) != None:
            raise Exception('alpha 命令与指定的对象不兼容。')
        else:
            cpatch = mw_get_cpatch(obj)
            cpatch.set_facealpha(value)
            update_legend(obj.axes)

def arrayvalue_to_ndarray(arr):
    if arr.__class__.__name__ in ("VectorValue", "ArrayValue"):
        return np.asarray(arr)
    else:
        return arr

def color_to_hex(color):
    if color == 'none' or color == 'None':
        return 'none'
    elif color == 'auto' or color == 'flat':
        return color
    elif isinstance(color, str):
        return mcolors.to_hex(mcolors.to_rgba(color))
    elif isinstance(color, tuple):
        return mcolors.to_hex(mcolors.to_rgba(color))
    elif len(color) == 1 and len(color[0]) > 1:
        return mcolors.to_hex(color[0])
    elif len(color) == 0 :
        return "none"    
    else:
        return mcolors.to_hex(color)

def get_property(cfig, cax = None, cobj = None, obj_name = None):
    props = {}
    prop_objs = {}

    fig_prop = cfig.get_all_props()
    props["Figure"] = fig_prop
    prop_objs["Figure"] = cfig
    
    if cax == None:
        if len(cfig.axs) > 0:
            cax = mw_get_cax(cfig.fig.gca())
        else:
            cfig.prop_objs = prop_objs
            return props
   
    ax_prop = cax.get_all_props()
    props["Axes"] = ax_prop
    prop_objs["Axes"] = mw_get_cax()

    if cobj != None and obj_name != None:
        obj_prop = cobj.get_all_props()
        props[obj_name] = obj_prop
        prop_objs[obj_name] = cobj
    else:
        if len(cax.lines) > 0:
            cobj = cax.lines[0]
            props["Line"] = cobj.get_all_props()
            prop_objs["Line"] = cobj
        elif len(cax.scatters) > 0:
            cobj = cax.scatters[0]
            props["Scatter"] = cobj.get_all_props()
            prop_objs["Scatter"] = cobj

    cfig.prop_objs = prop_objs
    return props

def get_default_colors_hex():
    color_list = [
        (0, 114, 189), (217, 83, 25), (237, 177, 32),
        (126, 47, 142), (119, 172, 48), (77, 190, 238), (162, 20, 47),
        (255, 255, 17), (19, 159, 255), (255, 105, 41),
        (100, 212, 19), (183, 70, 255), (15, 255, 255), (255, 19, 166),
        (255, 255, 255), (240, 240, 240), (230, 230, 230),
        (204, 204, 204), (166, 166, 166), (128, 128, 128), (38, 38, 38),
        (255, 0, 0), (255, 0, 255), (255, 255, 0),
        (0, 255, 0), (0, 255, 255), (0, 0, 255), (0, 0, 0)
    ]

    hex_colors = [mcolors.to_hex(np.array(c) / 255.) for c in color_list]

    return hex_colors

import pandas as pd
def sample_index(xdata, ydata, scale_factor, aspect_ratio = None):
    sampled_data = []
    if (len(xdata) != len(ydata) or len(xdata) < 2):
        return sampled_data

    # 根据 height 与 width 的比例和 cfig.sampling_num 计算 x_bit、y_bit
    # 采样数量默认为 cfig.sampling_num = 30000
    if aspect_ratio == None:
        aspect_ratio = 0.75

    cfig = mw_get_cfig()
    if cfig.x_bit and cfig.y_bit:
        x_bit = cfig.x_bit
        y_bit = cfig.y_bit
    else:
        sampling_num = cfig.min_sampling_num
        # sampling_num = 480000
        x_bit = int(np.sqrt(sampling_num/aspect_ratio))
        y_bit = int(0.75 * np.sqrt(sampling_num/aspect_ratio))

    x_bit = int(x_bit * np.sqrt(scale_factor))
    y_bit = int(y_bit * np.sqrt(scale_factor))

    # idx_from = min(len(xdata) - 1, idx_from)
    # idx_from = max(idx_from, 0)
    # idx_to = min(len(xdata) - 1, idx_to)
    # idx_to = max(idx_to, 0)

    x_min = np.min(xdata)
    x_max = np.max(xdata)
    y_min = np.min(ydata)
    y_max = np.max(ydata)

    x_interval = x_max - x_min
    y_interval = y_max - y_min

    bit_map = np.zeros((x_bit + 1, y_bit + 1), dtype=bool).ravel()
    if len(bit_map) >= len(xdata):
        return range(0, len(xdata))

    x_positions = x_bit * ((xdata - x_min) / x_interval).ravel()  # 计算所有数据点在x轴上的位置
    y_positions = y_bit * ((ydata - y_min) / y_interval).ravel()  # 计算所有数据点在y轴上的位置

    bit_num = x_bit * y_positions.astype(int) + x_positions.astype(int)
    valid_indices = np.where(bit_num < bit_map.size)[0]

    # _, return_index = np.unique(bit_num[valid_indices], return_index=True)
    # return_index.sort()
    series = pd.Series(bit_num[valid_indices])
    return_index = series.drop_duplicates(keep='first').index.to_numpy()

    return return_index


def get_resample_data(xdata, 
    ydata, 
    scale_factor, 
    aspect_ratio = None,
    figure = None, 
    ax = None
    ):
    

    cfig = mw_get_cfig()

    # 以下3种情况不采样
    # 1.要采样的数量大于当前图形数据量：cfig.sampling_num * scale_factor > len(xdata)
    # 2.当前图形数据量小于用户设置的最小采样数阈值：len(xdata) <= cfig.min_sampling_num)
    # 3.x轴或y轴为log形式
    # 如果用户自定义了x_bit,y_bit也采样，可忽略1,2
    if (cfig.sampling_num * scale_factor > len(xdata)
        or len(xdata) <= cfig.min_sampling_num)\
        and (cfig.x_bit == None and cfig.y_bit == None):
        return xdata, ydata

    if ax == None:
        ax = plt.gca()
    if ax.get_xscale() == "log" or ax.get_yscale() == "log":
        return xdata, ydata
    
    series = pd.Series(xdata)
    if not series.is_monotonic and not series.is_monotonic_decreasing:
        # print("xdata 非单调，当前算法无法采样。")
        return xdata, ydata 

    if scale_factor < 1:
        # return None
        scale_factor = 1

    index = sample_index(xdata, ydata, scale_factor, aspect_ratio = aspect_ratio)
    # index = np.round(np.linspace(0, len(x) - 1, current_num)).astype(int)

    xdata = xdata[index]
    ydata = ydata[index]

    return xdata, ydata

class CNotFound():
    """
    用于figure导入时替代找不到的类
    """
    def __init__(self) -> None:
        pass
    
    # 当stem3等online暂不支持的绘图类型,
    # 使用图例相关功能时，调用此函数，保证不报错
    def get_label(self):
        return ""