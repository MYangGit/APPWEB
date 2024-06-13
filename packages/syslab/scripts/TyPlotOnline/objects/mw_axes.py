"""
名称：axes
功能：此文件用于初始化坐标轴
实现：实现坐标轴的事件、槽函数、右键菜单等
接口：坐标轴类
依赖：
"""
# from PyQt5.QtWidgets import QMenu
# from PyQt5.QtGui import QCursor, QColor
from mpl_toolkits.mplot3d.axes3d import Axes3D
from TyPlotOnline.objects.mw_axes_3d import CAxes3D
from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.objects.mw_axes_3d import CAxes3D
from mpl_toolkits.axes_grid.anchored_artists import AnchoredAuxTransformBox
import matplotlib.transforms as mtransforms
from TyPlotOnline.data_tips.data_tips import Cursor
from TyPlotOnline.objects.mw_text import CTitle, CXlabel, CYlabel,CZlabel
import matplotlib.text as mtext
from matplotlib.streamplot import Grid, StreamMask, DomainMap, _get_integrator, _gen_starting_points, interpgrid
from TyPlotOnline.objects.mw_datum_line import CDrawDatumLine

from TyPlotOnline.common.mw_inner_function import mw_process_unit_info
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
from TyPlotOnline.objects.mw_line import CLine
import copy

import functools
import numpy as np
import matplotlib.collections as mcoll
from matplotlib import _api
import matplotlib.lines as mlines
import math
import matplotlib.colors as mcolors

import TyPlotOnline.settings.mw_setting_axes as ax_setting

class CAxes(object):
    """
    实现坐标轴的一些槽函数、右键菜单等

    Attributes
    -------------------
        ax : 目标坐标轴
        fig : 坐标轴所属图窗
        lines : 坐标轴内初始化后的曲线对象
        bar_containers : 坐标轴内初始化后的BarContainer对象
        pies : 坐标轴内初始化后的pie对象
        legend : 图例是否显示
        grid : 网格是否显示
        cursor : 游标是否开启
        data_tips : 数据提示是否开启
        hold_value : 绘图是否保持原图形
        lst_num : 存放bar的图形名
        pick : 选中状态
        tick_auto : 刻度是否自动
        cursor_line : 游标线
        current_mplcursor : 数据提示数据
    """
    def __init__(self, ax, position=[1,1,1]):
        self.init_attrs(ax, position=position)
        self.init_customize()

    def init_attrs(self, ax, position=[1,1,1]):
        self.ax = ax
        self.position = position
        self.fig = self.ax.figure if hasattr(self.ax, "figure") else None
        self.lines = []
        self.bar_containers = []
        self.bar3_containers = []
        self.pies = []
        self.pie_collection = None
        self.errorbars = []
        self.stems = []
        self.scatters = []
        self.areas = []
        self.surfs = []
        self.pcolors = []
        self.histograms = []
        self.histogram2s = []
        self.hists = []
        self.contours = []
        self.heatmaps = []
        self.fimplicitlines = []
        self.colorbar = None
        self.original_pos = None
        self.current_pos = None
        self.titles = []
        self.xlabels = []
        self.ylabels = []
        self.zlabels = []
        self.legends = []
        self.cimages = []
        self.legend = False
        self.grid = False
        self.cursor = False
        self.colorbar_on = False
        self.hold_value = 'off'
        self.pick = False
        self.tick_auto = {'X' : True, 'Y' : True, 'Z' : True}
        self.minor_tick = {'X' : False, 'Y' : False, 'Z' : False}
        self.cursor_line = []
        self.current_mplcursor = None
        self.legend_order = {}
        self.is_3d = False
        self.daspect = [1, 1, 0.75]
        self.is_geomap = False
        self.geomap = None
        self.cgeomap = None
        self.colororder = None
        self.cwordclouds = []
        self.cboxcharts = []
        self.texts = []
        self.rectangles = []
        self.patchs = []
        self.quivers = []
        self.quiver3s = []
        self.compasss = []
        self.streamlines=[]
        self.feathers = []
        self.feather_baselines = []
        self.font = CGlobalSetting.cGlobalFont

        # 标线，临时接收标线绘制对象
        self.dline = None
        # 标线集合,存储当前所有标线
        self.lst_datum_lines = []

        # yyaxis参数
        self.lst_linestyle = []
        self.lst_marker = []

        # 调整曲线层级置顶、置底时的微小增量
        self.LEVEL_OFFSET = 0.0000001

    def init_customize(self):
        self.current_lim = self.ax.dataLim.width
        self.init_font()

        if mw_get_cfig(self.fig).current_mplcursor == None:
            mw_get_cfig(self.fig).current_mplcursor = Cursor(self.fig, self.ax)
        else:
            mw_get_cfig(self.fig).current_mplcursor.ax = self.ax

        # if not CGlobalSetting.isOnline:
        #     # self.ax.get_legend=self.get_legend_to_replace
        #     self.ax._set_view_from_bbox = self._set_view_from_bbox
        #     self.ax.drag_pan = self.drag_pan
        self.create_pick_state()

        if not isinstance(self.ax, Axes3D):
            self.ax.quiver = self._quiver
        self.ax.streamplot=self._streamline
        self.ax.feather = self._feather
        self.ax.compass = self._compass

        self.init_ax()

        if isinstance(self.ax, Axes3D):
            self.init_axes3d()
        elif isinstance(self.ax, PolarAxes):
            self.init_polaraxes()
        else:
            self.init_minor_ticks()
            self.init_grid_style()
            # self.init_lines()
            # self.init_bar_containers()
        
        # if not CGlobalSetting.isOnline:
        self.connect()
        # self.ax.text = self.text
        self.init_texts()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["titles"]
        del state["xlabels"]
        del state["ylabels"]
        del state["zlabels"]
        return state

    def __setstate__(self, state):
        # 删除属性中无法初始化的对象，CNotFound
        for i in list(state.keys()):
            if (isinstance(state[i], CNotFound) 
                or (isinstance(state[i], list) 
                    and any(isinstance(item, CNotFound) for item in state[i]))):
                del state[i]

        self.init_attrs(None)
        # 旧属性导入，且兼容新实现
        common_keys = self.__dict__.keys() & state.keys()
        for i in common_keys:
            type_old = type(state[i])
            type_new = self.__dict__[i]
            if type_new != type_old and self.__dict__[i] != None:
                try:
                    state[i] = type_new(state[i])
                except:
                    pass
        self.__dict__.update(state)
        
    def before_export(self):
        """
        在导出前需要处理一些属性，使坐标轴可以正常序列化
        """
        # 处理标签
        for ctitle in self.titles:
            ctitle.before_export()
        for cxlabel in self.xlabels:
            cxlabel.before_export()
        for cylabel in self.ylabels:
            cylabel.before_export()
        for czlabel in self.zlabels:
            czlabel.before_export()
        for ctext in self.texts:
            ctext.before_export()
        for csurf in self.surfs:
            csurf.before_export()

    def after_export(self):
        """
        在导出完毕需要将导出前的操作影响去除
        """
        for ctitle in self.titles:
            ctitle.after_export()
        for cxlabel in self.xlabels:
            cxlabel.after_export()
        for cylabel in self.ylabels:
            cylabel.after_export()
        for czlabel in self.zlabels:
            czlabel.after_export()
        for ctext in self.texts:
            ctext.after_export()
        for csurf in self.surfs:
            csurf.after_export()
            
    def after_import(self):
        """
        在导入后需要重新初始化部分属性，使坐标轴的功能完备
        """
        # print(self.__dict__)
        # print(mw_get_cfig(self.fig))
        # print(CGlobalSetting.c_fig_lst)
        if not hasattr(self,"current_lim"):
            self.current_lim = self.ax.dataLim.width
        if mw_get_cfig(self.fig).current_mplcursor == None:
            mw_get_cfig(self.fig).current_mplcursor = Cursor(self.fig, self.ax)
        else:
            mw_get_cfig(self.fig).current_mplcursor.ax = self.ax

        for cl in self.lines:
            cl.after_import()
            # 不存在或者存在且为空的时候，需要处理
            if not hasattr(cl,"originDataX"):
                cl.originDataX = None
                cl.originDataY = None
                cl.sampled = False
                cl.init_origin_data()
            elif hasattr(cl,"originDataX") and cl.originDataX is None:
                cl.init_origin_data()
        for c_scatter in self.scatters:
            # 不存在或者存在且为空的时候，需要处理
            if not hasattr(c_scatter,"originDataX"):
                c_scatter.originDataX = None
                c_scatter.originDataY = None
                c_scatter.sampled = False
                c_scatter.init_origin_data()
            elif hasattr(c_scatter,"originDataX") and c_scatter.originDataX is None:
                c_scatter.init_origin_data()

        # if not CGlobalSetting.isOnline:
            # self.ax.get_legend=self.get_legend_to_replace
            # self.ax._set_view_from_bbox = self._set_view_from_bbox
            # self.ax.drag_pan = self.drag_pan
        self.create_pick_state()

        if not isinstance(self.ax, Axes3D):
            self.ax.quiver = self._quiver
        self.ax.streamplot=self._streamline
        self.ax.feather = self._feather
        self.ax.compass = self._compass

        self.connect()
        self.init_texts()
        for csurf in self.surfs:
            csurf.after_import()

        self.update_action_state()
        self.resample()

    def init_ax(self):
        self.ax.format_coord = lambda x, y: ""
        self.init_colororder()
        # self.ax._autotitlepos = False
        # self.ax.xaxis.set_zorder(3)
        # self.ax.yaxis.set_zorder(3)

    def init_colororder(self):
        cifg = mw_get_cfig(self.fig)
        if cifg.colororder is not None:
            self.ax.set_prop_cycle(color = cifg.colororder)
            self.colororder = cifg.colororder

    def init_texts(self):
        title = CTitle(self.ax, self.ax.title)
        title.dis_pick_self()
        self.titles.clear()
        self.titles.append(title)
        xlabel = CXlabel(self.ax, self.ax.xaxis.get_label())
        xlabel.dis_pick_self()
        self.xlabels.clear()
        self.xlabels.append(xlabel)
        ylabel = CYlabel(self.ax, self.ax.yaxis.get_label())
        ylabel.dis_pick_self()
        self.ylabels.clear()
        self.ylabels.append(ylabel)
        if isinstance(self.ax, Axes3D):
            zlabel = CZlabel(self.ax, self.ax.zaxis.get_label())
            zlabel.dis_pick_self()
            self.zlabels.clear()
            self.zlabels.append(zlabel)

    def init_minor_ticks(self):
        self.ax.set_aspect('auto')
        self.ax.set(frame_on=True)
        self.ax.tick_params(which = 'both', direction='in', top = True, right = True, colors = 'k')
        self.ax.minorticks_on()
        line_width = self.ax.spines['left'].get_linewidth()
        self.ax.tick_params(which = 'minor', length = line_width/2 - 0.4)
        self.ax.spines["left"].set_color('k')
        self.ax.spines["right"].set_color('k')
        self.ax.spines['left'].set_visible(True)
        self.ax.spines['right'].set_visible(True)
        self.ax.spines['top'].set_visible(True)
        self.ax.spines['bottom'].set_visible(True)

    def init_grid_style(self):
        #将主、次网格线默认颜色设为黑色
        self.ax.tick_params(which = 'major',
            grid_color = '#000000ff', grid_alpha = 0.15, grid_linestyle = '-')
        # self.ax.get_xaxis().set_tick_params(which = 'major',
        #     grid_color = '#000000ff', grid_alpha = 0.15, grid_linestyle = '-')
        # self.ax.get_yaxis().set_tick_params(which = 'major',
        #     grid_color = '#000000ff', grid_alpha = 0.15, grid_linestyle = '-')

        self.ax.tick_params(which = 'minor',
            grid_color = '#000000ff', grid_alpha = 0.25, grid_linestyle = ':')
        # self.ax.get_xaxis().set_tick_params(which = 'minor',
        #     grid_color = '#000000ff', grid_alpha = 0.25, grid_linestyle = ':')
        # self.ax.get_yaxis().set_tick_params(which = 'minor',
        #     grid_color = '#000000ff', grid_alpha = 0.25, grid_linestyle = ':')
    
    def init_toolbar_status(self):
        if ax_setting.get_xmajorgrid_status(self.ax) and ax_setting.get_ymajorgrid_status(self.ax):
            self.grid = True
            set_toolbutton_checked(self.fig, 'Grid', True)

        # 获取Axes当前是否存在legend以及所有的legend
        c_legend = ax_setting.get_legend_status(self.ax)
        if c_legend:
            self.legend = True
            self.legends.clear()
            self.legends.append(c_legend)
            set_toolbutton_checked(self.fig, 'Legend', True)

    def init_polaraxes(self):
        self.location_auto = True
        self.lim_auto = {'R' : True, 'Theta' : True}
        self.ax.set_xticks(np.deg2rad(np.arange(0.0, 360.0, 30.0)))
        self.ax.minorticks_on()
        self.init_grid_style()
        self.ax.set_rlabel_position(80)
        _min, _max = self.ax.get_xlim()
        min = np.rad2deg(_min)
        max = np.rad2deg(_max)
        self.theta_lim = (min,max)

        set_toolbutton_enabled(self.fig, 'Cursor', False)
        set_toolbutton_enabled(self.fig, 'Zoom', False)
        set_toolbutton_enabled(self.fig, 'Pan', False)
        set_toolbutton_enabled(self.fig, 'Grid', False)

        mw_get_cfig(self.fig).auto_adjust_view = False

        set_toolbutton_enabled(self.fig, 'AdjustMargin', True)

        self.ax.grid(b = True, which = "major")
        set_toolbutton_checked(self.fig, 'Grid', True)

        self.grid=True

    def init_axes3d(self):
        self.is_3d = True
        self.ax3d = CAxes3D(self.ax)
        self.ax.xaxis.gridlines.set_visible(False)
        self.ax.yaxis.gridlines.set_visible(False)
        self.ax.zaxis.gridlines.set_visible(False)
        self.grid = False
    def get_self_ax(self):
        return self.ax

    def init_font(self):
        t = self.ax.xaxis.get_label()
        fontname = t.get_fontname()
        fontsize = str(t.get_fontsize())
        fontstyle = True if t.get_fontstyle() == "italic" else False
        fontweight = True if t.get_fontweight() == "bold" else False

        self.font = (fontname, fontsize, fontstyle, fontweight)

    def connect(self):
        self.cid_key_press = self.ax.figure.canvas.mpl_connect(
             'key_press_event', self.on_key_press)

        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press_self)
        
        self.ax.callbacks.connect('xlim_changed', self.xlim_changed)

    def enable_paste(self):
        # 是否有待粘贴的曲线属性
        if len(CGlobalSetting.line_copy_prop) <=0:
            return False

        from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
        # 检查是否有不符合粘贴条件的图形：compass、帕累托图、热图、饼图、箱线图
        if isinstance(mw_get_cax(self.ax), CAxesPareto) or isinstance(self.ax, Axes3D) or isinstance(self.ax,PolarAxes):
            return False

        for prop_copy in CGlobalSetting.line_copy_prop:
            # 检查坐标轴类型是否一致、是否在当前坐标轴复制和粘贴
            if prop_copy['_axes'] == self.ax:
                return False
        return True

    def on_key_press(self, event):
        # 在当前axes内使用快捷键进行粘贴
        if self != mw_get_cax():
            return
        paste_able = self.enable_paste()
        # 当前处于编辑模式、当前坐标轴被选中且坐标轴经过上述判断符合可粘贴要求时，才可以粘贴曲线
        if event.key == "ctrl+v" and mw_get_cfig().edit_mode and self.pick and paste_able:
            self.line_paste_before()

    def on_press_self(self, event):
        if (event.inaxes != self.ax):
            return

        self.fig.sca(self.ax)
        self.update_action_state()

    def on_press(self):
        self.fig.sca(self.ax)
        self.update_action_state()

        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

            cfig = mw_get_cfig()
            if "Axes" in cfig.prop_objs and cfig.prop_objs["Axes"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Axes")
            else:
                props = get_property(cfig, cax = self)
                from TyPlotOnline.mw_prop import mw_property_init
                # mw_property_init(None)
                self.fig.canvas.send_event("property_init", props=props, current_prop="Axes", font_list = get_font_lst())

    def context_menu(self):
        """初始化右键菜单"""
        # 标线在非编辑模式下进行 游标优先级高于标线
        # 暂不支持标线功能
        # if not mw_get_cfig().edit_mode and not mw_get_cax().cursor:
        #     menu_list = []
        #     # 点击生成x轴标线右键菜单
        #     menu_list.append({"value": "x_datum_line", "label": "点击生成x轴标线", "children": [], "default_value":""})
            
        #     # 点击生成y轴标线右键菜单
        #     menu_list.append({"value": "y_datum_line", "label": "点击生成y轴标线", "children": [], "default_value":""})

        #     self.fig.canvas.send_event("contextmenu", menu_list=menu_list)
        #     self.fig.canvas.send_event("contextmenu", menu_list=menu_list)
        if mw_get_cfig().edit_mode:
            menu_list = []
            
            paste_able = self.enable_paste()
            menu_list.append({"value": "paste", "label": "粘贴", "children": [], "default_value":"","disabled":not paste_able})

            self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    def line_paste(self):
        if len(CGlobalSetting.line_copy_prop) == 0:
            return
        # 获取粘贴前的xlim与ylim
        x_limit,y_limit = self.ax.get_xlim(),self.ax.get_ylim()
        # 标志当前为xlim设置、ylim没设置时的情况或者ylim设置、xlim没设置的情况
        is_xlim,is_ylim = False,False

        if not self.ax._autoscaleXon and self.ax._autoscaleYon:
            # xlim 设置，ylim 未设置时的情况
            is_xlim = True
        elif self.ax._autoscaleXon and not self.ax._autoscaleYon:
            # ylim 设置，xlim 未设置时的情况
            is_ylim = True

        ymin, ymax = y_limit
        xmin, xmax = x_limit
        if len(self.ax._children) == 1:
            prop_copy = CGlobalSetting.line_copy_prop[0]
            xdata = prop_copy['_xorig']
            ydata = prop_copy['_yorig']
            if is_xlim:
                i = np.where((xdata > xmin) & (xdata < xmax))[0]
                if len(i) > 0:
                    ymin = ydata[i].min()
                    ymax = ydata[i].max()
            if is_ylim:
                i = np.where((ydata > ymin) & (ydata < ymax))[0]
                if len(i) > 0:
                    xmin = xdata[i].min()
                    xmax = xdata[i].max()
        
        for prop_copy in CGlobalSetting.line_copy_prop:
            # 因为需要删除_axes属性，因此复制曲线属性，不然无法实现曲线一次复制多次粘贴
            props = copy.copy(prop_copy)
            # 在同一axes内不进行复制粘贴操作
            if props['_axes'] != self.ax:
                # 先根据待绘制曲线的x y坐标绘制曲线 显式指定颜色，以避免打破默认颜色规律
                line_copy, = self.ax.plot(props['_xorig'],props['_yorig'],color=props['_color'])
                del props['_axes']
                line_copy.__dict__.update(props)
                c_line = CLine(line_copy)
                mw_get_cax().lines.append(c_line)
                c_line.set_zorder(mw_get_cax().get_max_level().get_zorder()+mw_get_cax().LEVEL_OFFSET)
                update_legend(self.ax)

                xdata = props['_xorig']
                ydata = props['_yorig']
                if is_xlim:
                    i = np.where((xdata > xmin) & (xdata < xmax))[0]
                    if len(i) > 0:
                        ymin = min(ydata[i].min(), ymin)
                        ymax = max(ydata[i].max(), ymax)
                elif is_ylim:
                    i = np.where((ydata > ymin) & (ydata < ymax))[0]
                    if len(i) > 0:
                        xmin = min(xdata[i].min(),xmin)
                        xmax = max(xdata[i].max(),xmax)

        if is_xlim:
            self.ax.set_ylim(ymin,ymax)
            self.ax._autoscaleYon = True
        elif is_ylim:
            self.ax.set_xlim(xmin,xmax)
            self.ax._autoscaleXon = True

        self.fig.canvas.draw_idle()

    def line_paste_before(self):
        data_num = 0
        # 需要在复制粘贴之前判断一下数据量，如果数据量较大，提醒用户
        if CGlobalSetting.line_copy_prop != None:
            # 遍历每一条待复制曲线属性
            for prop_copy in CGlobalSetting.line_copy_prop:
                # 在同一axes内不进行复制粘贴操作
                if prop_copy['_axes'] != self.ax:
                    data_num = data_num + len(prop_copy['_xorig'])
        # 百万数量级以上需要提醒
        if data_num >= pow(10,6):
            # 前端进行提醒
            self.fig.canvas.send_event("paste_reminder")
            # self.line_paste()
        else:
            self.line_paste()

    def action_grid(self):
        mw_grid(self.ax, 'on' if not self.grid else 'off')

    def action_legend(self):
        mw_legend(self.ax, 'on' if not self.legend else 'off')

    def action_color(self):
        face_color = self.ax.get_facecolor()
        if self.is_3d:
            face_color = self.ax.w_xaxis.pane.get_facecolor()

        current_color = QColor.fromRgbF(face_color[0], face_color[1], face_color[2], face_color[3])

        dlg_color = DlgColor(current_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color()
            if self.is_3d:
                self.ax.w_xaxis.set_pane_color(select_color.getRgbF())
                self.ax.w_yaxis.set_pane_color(select_color.getRgbF())
                self.ax.w_zaxis.set_pane_color(select_color.getRgbF())
            else:
                self.ax.set_facecolor(select_color.name())

    def action_reset_view(self):
        # self.ax.set_box_aspect((1,1,0.75))
        self.ax.view_init(30, -127.5)
        show_label(self.ax, 'Both')
        ticks_auto(self.ax, 'both')
        self.ax3d.update_annotation()

    def action_view_xy(self):
        # self.ax.set_box_aspect((1,1,1e-10))
        self.ax.view_init(90,-90)
        show_label(self.ax, 'Both')
        hide_label(self.ax, 'Z')
        ticks_auto(self.ax, 'both')
        self.ax.get_zaxis().set_ticklabels([])
        self.ax3d.update_annotation()

    def action_view_xz(self):
        # self.ax.set_box_aspect((1,1e-10,1))
        self.ax.view_init(0,-90)
        show_label(self.ax, 'Both')
        hide_label(self.ax, 'Y')
        ticks_auto(self.ax, 'both')
        self.ax.get_yaxis().set_ticklabels([])
        self.ax3d.update_annotation()

    def action_view_yz(self):
        # self.ax.set_box_aspect((1e-10,1,1))
        self.ax.view_init(0,0)
        show_label(self.ax, 'Both')
        hide_label(self.ax, 'X')
        ticks_auto(self.ax, 'both')
        self.ax.get_xaxis().set_ticklabels([])
        self.ax3d.update_annotation()

    def action_prop(self):
        from TyPlotOnline.settings.mw_setting_base import CPropertySetting

        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.ax], self.get_all_lines()])
        prop_dlg.set_current_index(1)
        prop_dlg.connect()
        prop_dlg.exec_()

    def update_action_state(self):
        set_toolbutton_enabled(self.fig, 'Grid', True)
        set_toolbutton_checked(self.fig, 'Grid', self.grid)

        set_toolbutton_enabled(self.fig, 'Legend', True)
        set_toolbutton_checked(self.fig, 'Legend', self.legend)

        if isinstance(self.ax, PolarAxes):
            set_toolbutton_enabled(self.fig, 'Cursor', False)
            set_toolbutton_checked(self.fig, 'Cursor', False)
            set_toolbutton_enabled(self.fig, 'Zoom', False)
            set_toolbutton_checked(self.fig, 'Zoom', False)
            set_toolbutton_enabled(self.fig, 'Pan', False)
            set_toolbutton_checked(self.fig, 'Pan', False)
            set_toolbutton_enabled(self.fig, 'Home', False)
            set_toolbutton_checked(self.fig, 'Home', False)
        elif len(self.heatmaps) > 0 or len(self.pies) > 0:
            set_toolbutton_enabled(self.fig, 'Zoom', False)
            set_toolbutton_enabled(self.fig, 'Pan', False)
            set_toolbutton_enabled(self.fig, 'Grid', False)
        else:
            set_toolbutton_enabled(self.fig, 'Zoom', True)
            set_toolbutton_enabled(self.fig, 'Pan', True)
            set_toolbutton_enabled(self.fig, 'Grid', True)

            if not self.is_3d:
                if (len(self.pies) + len(self.bar_containers) + len(self.bar3_containers) +
                    len(self.errorbars) + len(self.stems) + len(self.scatters) + len(self.areas) +
                    len(self.surfs) + len(self.histograms) + len(self.hists) + len(self.contours) +
                    len(self.heatmaps)) > 0:
                    set_toolbutton_enabled(self.fig, 'Cursor', False)
                elif len(self.lines) > 0:
                    set_toolbutton_enabled(self.fig, 'Cursor', True)
                    set_toolbutton_checked(self.fig, 'Cursor', self.cursor)
                else:
                    set_toolbutton_enabled(self.fig, 'Cursor', True)
        
        # set_toolbutton_enabled(self.fig, 'Colorbar', self.colorbar_on)

    def create_pick_state(self):
        trans = mtransforms.blended_transform_factory(self.ax.transAxes, self.ax.transAxes)
        self.box = AnchoredAuxTransformBox(trans, loc='center',frameon = False )
        self.pick_state = Line2D([0, 0, 0, 0.5, 1, 1, 1, 0.5], [1, 0.5, 0, 0, 0, 0.5, 1, 1], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785')
        self.box.drawing_area.add_artist(self.pick_state)
        self.ax.add_artist(self.box)

        self.pick_state.set_visible(False)

    def add_pick_state_box(self):
        self.ax.add_artist(self.box)

    def pick_self(self, pick_only = False):
        """曲线选中状态"""
        self.pick_state.set_visible(True)
        self.fig.canvas.draw_idle()
        self.pick = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        self.pick_state.set_visible(False)
        self.fig.canvas.draw_idle()
        self.pick = False

    def get_all_lines(self):
        lines = []
        for c_line in self.lines:
            lines.append(c_line.line)

        return lines

    def get_all_errorbar(self):
        errorbars = []
        for c_errorbar in self.errorbars:
            errorbars.append(c_errorbar.errorbar_container)

        return errorbars

    def get_all_cboxcharts(self):
        return self.cboxcharts

    def get_all_cwordclouds(self):
        return self.cwordclouds

    def get_all_bars(self):
        bar_containers = []
        for bar_container in self.bar_containers:
            bar_containers.append(bar_container.bar_container)

        return bar_containers

    def get_all_bar3s(self):
        bar3_containers = []
        for bar3_container in self.bar3_containers:
            bar3_containers.append(bar3_container.poly3Dcollection)

        return bar3_containers

    def get_all_pies(self):
        pies = []
        for c_pie in self.pies:
            pies.append(c_pie.pie)

        return pies

    def get_all_stems(self):
        stems = []
        for c_stem in self.stems:
            stems.append(c_stem.stem_container)

        return stems

    def get_all_scatters(self):
        scatters = []
        for c_scatter in self.scatters:
            scatters.append(c_scatter.path_collection)

        return scatters

    def get_all_areas(self):
        areas = []
        for c_area in self.areas:
            areas.append(c_area.poly_collection)

        return areas

    def get_all_surfs(self):
        surfs = []
        for c_surf in self.surfs:
            surfs.append(c_surf.poly_collection)

        return surfs

    def get_all_histograms(self):
        hists = []
        for c_hist in self.histograms:
            hists.append(c_hist.hist)

        return hists

    def get_all_histograms2(self):
        hists2 = []
        for c_hist2 in self.histogram2s:
            hists2.append(c_hist2.poly3Dcollection)

        return hists2

    def get_all_hists(self):
        hists = []
        for c_hist in self.hists:
            hists.append(c_hist.hist)

        return hists

    def get_all_contours(self):
        contours = []
        for c_contour in self.contours:
            contours.append(c_contour.contour)

        return contours

    def get_all_heatmaps(self):
        heatmaps = []
        for c_heatmap in self.heatmaps:
            heatmaps.append(c_heatmap.axes_image)

        return heatmaps

    def get_all_cimages(self):
        cimages = []
        for c_image in self.cimages:
            cimages.append(c_image)

        return cimages

    def get_all_fimplicitlines(self):
        fimplicitlines = []
        for c_fimplicitline in self.fimplicitlines:
            fimplicitlines.append(c_fimplicitline.contour)

        return fimplicitlines

    def get_all_rectangles(self):
        crectangles = []
        for c_rectangle in self.rectangles:
            crectangles.append(c_rectangle.collection)

        return crectangles

    def get_all_patchs(self):
        cpatchs = []
        for c_patch in self.patchs:
            cpatchs.append(c_patch.collection)

        return cpatchs

    def get_all_quivers(self):
        cquivers = []
        for c_quiver in self.quivers:
            cquivers.append(c_quiver.quiver)
        return cquivers

    def get_all_quiver3s(self):
        cquiver3s = []
        for c_quiver3 in self.quiver3s:
            cquiver3s.append(c_quiver3.quiver3)

        return cquiver3s

    def get_all_streamlines(self):
        cstreamlines = []
        for c_streamline in self.streamlines:
            cstreamlines.append(c_streamline.streamline)

        return cstreamlines

    def get_all_feathers(self):
        cfeathers = []
        for c_feather in self.feathers:
            cfeathers.append(c_feather.feather)

        return cfeathers

    def get_all_compasss(self):
        ccompasss = []
        for c_compass in self.compasss:
            ccompasss.append(c_compass.compass)

        return ccompasss

    def get_all_pcolors(self):
        pcolors = []
        for c_pcolor in self.pcolors:
            pcolors.append(c_pcolor.poly_collection)

        return pcolors

    def get_all_texts(self):
        texts = []
        for c_text in self.texts:
            texts.append(c_text.text)

        return texts

    def get_all_labels(self):
        labels = []
        for c_xlabel in self.xlabels:
            labels.append(c_xlabel.text)
        for c_ylabel in self.ylabels:
            labels.append(c_ylabel.text)
        for c_zlabel in self.zlabels:
            labels.append(c_ylabel.text)

        return labels

    def get_all_objs(self):
        res = []
        if len(self.get_all_lines()) != 0:
            res.extend(self.get_all_lines())
        if len(self.get_all_labels()) != 0:
            res.extend(self.get_all_labels())
        if len(self.get_all_texts()) != 0:
            res.extend(self.get_all_texts())
        if len(self.get_all_compasss()) != 0:
            res.extend(self.get_all_compasss())
        if len(self.get_all_feathers()) != 0:
            res.extend(self.get_all_feathers())
        if len(self.get_all_streamlines()) != 0:
            res.extend(self.get_all_streamlines())
        if len(self.get_all_quiver3s()) != 0:
            res.extend(self.get_all_quiver3s())
        if len(self.get_all_quivers()) != 0:
            res.extend(self.get_all_quivers())
        if len(self.get_all_areas()) != 0:
            res.extend(self.get_all_areas())
        if len(self.get_all_bar3s()) != 0:
            res.extend(self.get_all_bar3s())
        if len(self.get_all_bars()) != 0:
            res.extend(self.get_all_bars())
        if len(self.get_all_cboxcharts()) != 0:
            res.extend(self.get_all_cboxcharts())
        if len(self.get_all_cimages()) != 0:
            res.extend(self.get_all_cimages())
        if len(self.get_all_contours()) != 0:
            res.extend(self.get_all_contours())
        if len(self.get_all_cwordclouds()) != 0:
            res.extend(self.get_all_cwordclouds())
        if len(self.get_all_errorbar()) != 0:
            res.extend(self.get_all_errorbar())
        if len(self.get_all_fimplicitlines()) != 0:
            res.extend(self.get_all_fimplicitlines())
        if len(self.get_all_heatmaps()) != 0:
            res.extend(self.get_all_heatmaps())
        if len(self.get_all_hists()) != 0:
            res.extend(self.get_all_hists())
        if len(self.get_all_patchs()) != 0:
            res.extend(self.get_all_patchs())
        if len(self.get_all_pies()) != 0:
            res.extend(self.get_all_pies())
        if len(self.get_all_rectangles()) != 0:
            res.extend(self.get_all_rectangles())
        if len(self.get_all_stems()) != 0:
            res.extend(self.get_all_stems())
        if len(self.get_all_histograms()) != 0:
            res.extend(self.get_all_histograms())
        if len(self.get_all_histograms2()) != 0:
            res.extend(self.get_all_histograms2())
        if len(self.get_all_pcolors()) != 0:
            res.extend(self.get_all_pcolors())

        return res

    def mw_update_xticks(self):
        """
        Update ticks (position and labels) using the current data interval of
        the axes.  Return the list of ticks that will be drawn.
        """
        major_locs = self.cgeomap.get_right_locs()[1]
        self.ax.xaxis.set_major_locator(mticker.FixedLocator(major_locs))
        major_labels = self.cgeomap.get_right_loclabels("x")

        major_ticks = self.ax.xaxis.get_major_ticks(len(major_locs))
        self.ax.xaxis.major.formatter.set_locs(major_locs)
        for tick, loc, label in zip(major_ticks, major_locs, major_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        minor_locs = self.ax.xaxis.get_minorticklocs()
        minor_labels = self.ax.xaxis.minor.formatter.format_ticks(minor_locs)
        minor_ticks = self.ax.xaxis.get_minor_ticks(len(minor_locs))
        self.ax.xaxis.minor.formatter.set_locs(minor_locs)
        for tick, loc, label in zip(minor_ticks, minor_locs, minor_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        ticks = [*major_ticks, *minor_ticks]

        view_low, view_high = self.ax.xaxis.get_view_interval()
        if view_low > view_high:
            view_low, view_high = view_high, view_low

        interval_t = self.ax.get_transform().transform([view_low, view_high])

        ticks_to_draw = []
        for tick in ticks:
            try:
                loc_t = self.ax.get_transform().transform(tick.get_loc())
            except AssertionError:
                # transforms.transform doesn't allow masked values but
                # some scales might make them, so we need this try/except.
                pass
            else:
                if mtransforms._interval_contains_close(interval_t, loc_t):
                    ticks_to_draw.append(tick)

        return ticks_to_draw


    def mw_update_yticks(self):
        """
        Update ticks (position and labels) using the current data interval of
        the axes.  Return the list of ticks that will be drawn.
        """
        major_locs = self.cgeomap.get_right_locs()[0]
        self.ax.yaxis.set_major_locator(mticker.FixedLocator(major_locs))
        major_labels = self.cgeomap.get_right_loclabels("y")
        major_ticks = self.ax.yaxis.get_major_ticks(len(major_locs))
        self.ax.yaxis.major.formatter.set_locs(major_locs)
        for tick, loc, label in zip(major_ticks, major_locs, major_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        minor_locs = self.ax.yaxis.get_minorticklocs()
        minor_labels = self.ax.yaxis.minor.formatter.format_ticks(minor_locs)
        minor_ticks = self.ax.yaxis.get_minor_ticks(len(minor_locs))
        self.ax.yaxis.minor.formatter.set_locs(minor_locs)
        for tick, loc, label in zip(minor_ticks, minor_locs, minor_labels):
            tick.update_position(loc)
            tick.set_label1(label)
            tick.set_label2(label)
        ticks = [*major_ticks, *minor_ticks]

        view_low, view_high = self.ax.yaxis.get_view_interval()
        if view_low > view_high:
            view_low, view_high = view_high, view_low

        interval_t = self.ax.get_transform().transform([view_low, view_high])

        ticks_to_draw = []
        for tick in ticks:
            try:
                loc_t = self.ax.get_transform().transform(tick.get_loc())
            except AssertionError:
                # transforms.transform doesn't allow masked values but
                # some scales might make them, so we need this try/except.
                pass
            else:
                if mtransforms._interval_contains_close(interval_t, loc_t):
                    ticks_to_draw.append(tick)

        return ticks_to_draw


    def mw_set_xlim(self, left=None, right=None, emit=True, auto=False,
                 *, xmin=None, xmax=None):

        if right is None and np.iterable(left):
            left, right = left
        if xmin is not None:
            if left is not None:
                raise TypeError('Cannot pass both `xmin` and `left`')
            left = xmin
        if xmax is not None:
            if right is not None:
                raise TypeError('Cannot pass both `xmax` and `right`')
            right = xmax

        # self.ax._process_unit_info(xdata=(left, right))
        mw_process_unit_info(self.ax, xdata=(left, right))
        left = self.ax._validate_converted_limits(left, self.ax.convert_xunits)
        right = self.ax._validate_converted_limits(right, self.ax.convert_xunits)

        if left is None or right is None:
            # Axes init calls set_xlim(0, 1) before get_xlim() can be called,
            # so only grab the limits if we really need them.
            old_left, old_right = self.ax.get_xlim()
            if left is None:
                left = old_left
            if right is None:
                right = old_right

        if left < -10000 or right > 40085117:
            return self.ax.get_xlim()

        if self.ax.get_xscale() == 'log' and (left <= 0 or right <= 0):
            # Axes init calls set_xlim(0, 1) before get_xlim() can be called,
            # so only grab the limits if we really need them.
            old_left, old_right = self.ax.get_xlim()
            if left <= 0:
                cbook._warn_external(
                    'Attempted to set non-positive left xlim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.')
                left = old_left
            if right <= 0:
                cbook._warn_external(
                    'Attempted to set non-positive right xlim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.')
                right = old_right
        if left == right:
            cbook._warn_external(
                f"Attempting to set identical left == right == {left} results "
                f"in singular transformations; automatically expanding.")
        reverse = left > right
        left, right = self.ax.xaxis.get_major_locator().nonsingular(left, right)
        left, right = self.ax.xaxis.limit_range_for_scale(left, right)
        # cast to bool to avoid bad interaction between python 3.8 and np.bool_
        left, right = sorted([left, right], reverse=bool(reverse))

        self.ax._viewLim.intervalx = (left, right)
        # Mark viewlims as no longer stale without triggering an autoscale.
        for ax in self.ax._shared_axes['x'].get_siblings(self.ax):
            ax._stale_viewlims['x'] = False
        if auto is not None:
            self.ax._autoscaleXon = bool(auto)

        if emit:
            self.ax.callbacks.process('xlim_changed', self.ax)
            # Call all of the other x-axes that are shared with this one
            for other in self.ax._shared_axes['x'].get_siblings(self.ax):
                if other is not self.ax:
                    other.set_xlim(self.ax.viewLim.intervalx,
                                   emit=False, auto=auto)
                    if other.figure != self.ax.figure:
                        other.figure.canvas.draw_idle()
        self.ax.stale = True
        return left, right

    def mw_set_ylim(self, bottom=None, top=None, emit=True, auto=False,
                 *, ymin=None, ymax=None):

        if top is None and np.iterable(bottom):
            bottom, top = bottom
        if ymin is not None:
            if bottom is not None:
                raise TypeError('Cannot pass both `ymin` and `bottom`')
            bottom = ymin
        if ymax is not None:
            if top is not None:
                raise TypeError('Cannot pass both `ymax` and `top`')
            top = ymax

        # self.ax._process_unit_info(ydata=(bottom, top))
        mw_process_unit_info(self.ax, ydata=(bottom, top))
        bottom = self.ax._validate_converted_limits(bottom, self.ax.convert_yunits)
        top = self.ax._validate_converted_limits(top, self.ax.convert_yunits)

        if bottom is None or top is None:
            # Axes init calls set_ylim(0, 1) before get_ylim() can be called,
            # so only grab the limits if we really need them.
            old_bottom, old_top = self.ax.get_ylim()
            if bottom is None:
                bottom = old_bottom
            if top is None:
                top = old_top

        if bottom < 0 or top > 39943738:
            return self.ax.get_ylim()

        if self.ax.get_yscale() == 'log' and (bottom <= 0 or top <= 0):
            # Axes init calls set_xlim(0, 1) before get_xlim() can be called,
            # so only grab the limits if we really need them.
            old_bottom, old_top = self.ax.get_ylim()
            if bottom <= 0:
                cbook._warn_external(
                    'Attempted to set non-positive bottom ylim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.')
                bottom = old_bottom
            if top <= 0:
                cbook._warn_external(
                    'Attempted to set non-positive top ylim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.')
                top = old_top
        if bottom == top:
            cbook._warn_external(
                f"Attempting to set identical bottom == top == {bottom} "
                f"results in singular transformations; automatically "
                f"expanding.")
        reverse = bottom > top
        bottom, top = self.ax.yaxis.get_major_locator().nonsingular(bottom, top)
        bottom, top = self.ax.yaxis.limit_range_for_scale(bottom, top)
        # cast to bool to avoid bad interaction between python 3.8 and np.bool_
        bottom, top = sorted([bottom, top], reverse=bool(reverse))

        self.ax._viewLim.intervaly = (bottom, top)
        # Mark viewlims as no longer stale without triggering an autoscale.
        for ax in self.ax._shared_axes['y'].get_siblings(self.ax):
            ax._stale_viewlims['y'] = False
        if auto is not None:
            self.ax._autoscaleYon = bool(auto)

        if emit:
            self.ax.callbacks.process('ylim_changed', self.ax)
            # Call all of the other y-axes that are shared with this one
            for other in self.ax._shared_axes['y'].get_siblings(self.ax):
                if other is not self.ax:
                    other.set_ylim(self.ax.viewLim.intervaly,
                                   emit=False, auto=auto)
                    if other.figure != self.ax.figure:
                        other.figure.canvas.draw_idle()
        self.ax.stale = True
        return bottom, top

    def mw_set_view_from_bbox(self, bbox, direction='in',
                            mode=None, twinx=False, twiny=False):

        if len(bbox) == 3:
            Xmin, Xmax = self.ax.get_xlim()
            Ymin, Ymax = self.ax.get_ylim()

            xp, yp, scl = bbox  # Zooming code

            if scl == 0:  # Should not happen
                scl = 1.

            if scl > 1:
                direction = 'in'
            else:
                direction = 'out'
                scl = 1/scl

            # get the limits of the axes
            tranD2C = self.ax.transData.transform
            xmin, ymin = tranD2C((Xmin, Ymin))
            xmax, ymax = tranD2C((Xmax, Ymax))

            # set the range
            xwidth = xmax - xmin
            ywidth = ymax - ymin
            xcen = (xmax + xmin)*.5
            ycen = (ymax + ymin)*.5
            xzc = (xp*(scl - 1) + xcen)/scl
            yzc = (yp*(scl - 1) + ycen)/scl

            bbox = [xzc - xwidth/2./scl, yzc - ywidth/2./scl,
                    xzc + xwidth/2./scl, yzc + ywidth/2./scl]
        elif len(bbox) != 4:
            # should be len 3 or 4 but nothing else
            cbook._warn_external(
                "Warning in _set_view_from_bbox: bounding box is not a tuple "
                "of length 3 or 4. Ignoring the view change.")
            return

        # Original limits.
        xmin0, xmax0 = self.ax.get_xbound()
        ymin0, ymax0 = self.ax.get_ybound()
        # The zoom box in screen coords.
        startx, starty, stopx, stopy = bbox
        # Convert to data coords.
        (startx, starty), (stopx, stopy) = self.ax.transData.inverted().transform(
            [(startx, starty), (stopx, stopy)])
        # Clip to axes limits.
        xmin, xmax = np.clip(sorted([startx, stopx]), xmin0, xmax0)
        ymin, ymax = np.clip(sorted([starty, stopy]), ymin0, ymax0)
        # Don't double-zoom twinned axes or if zooming only the other axis.
        if twinx or mode == "y":
            xmin, xmax = xmin0, xmax0
        if twiny or mode == "x":
            ymin, ymax = ymin0, ymax0

        if direction == "in":
            new_xbound = xmin, xmax
            new_ybound = ymin, ymax

        elif direction == "out":
            x_trf = self.ax.xaxis.get_transform()
            sxmin0, sxmax0, sxmin, sxmax = x_trf.transform(
                [xmin0, xmax0, xmin, xmax])  # To screen space.
            factor = (sxmax0 - sxmin0) / (sxmax - sxmin)  # Unzoom factor.
            # Move original bounds away by
            # (factor) x (distance between unzoom box and axes bbox).
            sxmin1 = sxmin0 - factor * (sxmin - sxmin0)
            sxmax1 = sxmax0 + factor * (sxmax0 - sxmax)
            # And back to data space.
            new_xbound = x_trf.inverted().transform([sxmin1, sxmax1])

            y_trf = self.ax.yaxis.get_transform()
            symin0, symax0, symin, symax = y_trf.transform(
                [ymin0, ymax0, ymin, ymax])
            factor = (symax0 - symin0) / (symax - symin)
            symin1 = symin0 - factor * (symin - symin0)
            symax1 = symax0 + factor * (symax0 - symax)
            new_ybound = y_trf.inverted().transform([symin1, symax1])

        # if new_xbound[0] < 0 or new_xbound[1] > 40075016.68557848 \
        #     or new_ybound[0] < 0 or new_ybound[1] > 39943737.76081716:
        #     return
        # if new_xbound[0] < 0 :
        #     new_xbound[1] = new_xbound[1] - new_xbound[0]
        #     new_xbound[0] = 0
        #     if new_xbound[1] > 40075016.68557848:
        #         return

        # if new_xbound[1] > 40075016.68557848:
        #     new_xbound[0] = 40075016.68557848 - new_xbound[1] + new_xbound[0]
        #     new_xbound[1] = 40075016.68557848
        #     if new_xbound[0] < 0 :
        #         return

        if new_ybound[0] < 0 :
            new_ybound[1] = new_ybound[1] - new_ybound[0]
            new_ybound[0] = 0
            if new_ybound[1] > 39943737.76081716:
                new_ybound[1] = 39943737.76081716

        if new_ybound[1] > 39943737.76081716:
            new_ybound[0] = 39943737.76081716 - new_ybound[1] + new_ybound[0]
            new_ybound[1] = 39943737.76081716
            if new_ybound[0] < 0 :
                new_ybound[0] = 0

        height = new_ybound[1]-new_ybound[0]
        width = (40075/39944)*height
        if width < 1e-5 or height <1e-5:
            return
        mid_x = (new_xbound[1]+new_xbound[0])/2
        if (mid_x - width/2) < 0:
            new_xbound=(0.001,width)
        elif (mid_x + width/2) > 40075000:
            new_xbound=(40075000-width,40075000)
        else:
            new_xbound=(mid_x - width/2,mid_x + width/2)

        if not twinx and mode != "y":
            self.ax.set_xbound(new_xbound)
        if not twiny and mode != "x":
            self.ax.set_ybound(new_ybound)
        self.cgeomap.check_update_ims()

    def mw_set_view(self,view):
        """
        Apply a previously saved view.

        Called when restoring a view, such as with the navigation buttons.

        .. note::

            Intended to be overridden by new projection types, but if not, the
            default implementation restores the view limits. You *must*
            implement :meth:`_get_view` if you implement this method.
        """
        xmin, xmax, ymin, ymax = view
        self.ax.set_xlim((xmin, xmax))
        self.ax.set_ylim((ymin, ymax))
        self.cgeomap.check_update_ims()

    def mw_drag_pan(self, button, key, x, y):

        def format_deltas(key, dx, dy):
            if key == 'control':
                if abs(dx) > abs(dy):
                    dy = dx
                else:
                    dx = dy
            elif key == 'x':
                dy = 0
            elif key == 'y':
                dx = 0
            elif key == 'shift':
                if 2 * abs(dx) < abs(dy):
                    dx = 0
                elif 2 * abs(dy) < abs(dx):
                    dy = 0
                elif abs(dx) > abs(dy):
                    dy = dy / abs(dy) * abs(dx)
                else:
                    dx = dx / abs(dx) * abs(dy)
            return dx, dy

        p = self.ax._pan_start
        dx = x - p.x
        dy = y - p.y
        if dx == dy == 0:
            return
        if button == 1:
            dx, dy = format_deltas(key, dx, dy)
            result = p.bbox.translated(-dx, -dy).transformed(p.trans_inverse)
        elif button == 3:
            try:
                dx = -dx / self.ax.bbox.width
                dy = -dy / self.ax.bbox.height
                dx, dy = format_deltas(key, dx, dy)
                if self.ax.get_aspect() != 'auto':
                    dx = dy = 0.5 * (dx + dy)
                alpha = np.power(10.0, (dx, dy))
                start = np.array([p.x, p.y])
                oldpoints = p.lim.transformed(p.trans)
                newpoints = start + alpha * (oldpoints - start)
                result = (mtransforms.Bbox(newpoints)
                          .transformed(p.trans_inverse))
            except OverflowError:
                cbook._warn_external('Overflow while panning')
                return
        else:
            return

        valid = np.isfinite(result.transformed(p.trans))
        points = result.get_points().astype(object)
        xlim = points[:, 0]
        ylim = points[:, 1]
        # Just ignore invalid limits (typically, underflow in log-scale).
        points[~valid] = None
        if ylim[0] < 0:
            ylim[1] = ylim[1] - ylim[0]
            ylim[0] = 0
            if ylim[1] > 39943737.76081716:
                ylim[1] = 39943737.76081716

        if ylim[1] > 39943737.76081716:
            ylim[0] = 39943737.76081716 - ylim[1] + ylim[0]
            ylim[1] = 39943737.76081716
            if ylim[0] < 0:
                ylim[0] = 0

        height = ylim[1]-ylim[0]
        width = (40075/39944)*height
        if width < 1e-5 or height <1e-5:
            return
        mid_x = (xlim[1]+xlim[0])/2
        if (mid_x - width/2) < 0:
            xlim=(0.001,width)
        elif (mid_x + width/2) > 40075000:
            xlim=(40075000-width,40075000)
        else:
            xlim=(mid_x - width/2,mid_x + width/2)

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.cgeomap.check_update_ims()

    def _set_view_from_bbox(self, bbox, direction='in',
                            mode=None, twinx=False, twiny=False):
        if len(bbox) == 3:
            Xmin, Xmax = self.ax.get_xlim()
            Ymin, Ymax = self.ax.get_ylim()

            xp, yp, scl = bbox  # Zooming code

            if scl == 0:  # Should not happen
                scl = 1.

            if scl > 1:
                direction = 'in'
            else:
                direction = 'out'
                scl = 1/scl

            # get the limits of the axes
            tranD2C = self.ax.transData.transform
            xmin, ymin = tranD2C((Xmin, Ymin))
            xmax, ymax = tranD2C((Xmax, Ymax))

            # set the range
            xwidth = xmax - xmin
            ywidth = ymax - ymin
            xcen = (xmax + xmin)*.5
            ycen = (ymax + ymin)*.5
            xzc = (xp*(scl - 1) + xcen)/scl
            yzc = (yp*(scl - 1) + ycen)/scl

            bbox = [xzc - xwidth/2./scl, yzc - ywidth/2./scl,
                    xzc + xwidth/2./scl, yzc + ywidth/2./scl]
        elif len(bbox) != 4:
            # should be len 3 or 4 but nothing else
            cbook._warn_external(
                "Warning in _set_view_from_bbox: bounding box is not a tuple "
                "of length 3 or 4. Ignoring the view change.")
            return

        # Original limits.
        xmin0, xmax0 = self.ax.get_xbound()
        ymin0, ymax0 = self.ax.get_ybound()
        # The zoom box in screen coords.
        startx, starty, stopx, stopy = bbox
        # Convert to data coords.
        (startx, starty), (stopx, stopy) = self.ax.transData.inverted().transform(
            [(startx, starty), (stopx, stopy)])
        # Clip to axes limits.
        xmin, xmax = np.clip(sorted([startx, stopx]), xmin0, xmax0)
        ymin, ymax = np.clip(sorted([starty, stopy]), ymin0, ymax0)
        # Don't double-zoom twinned axes or if zooming only the other axis.
        if twinx or mode == "y":
            xmin, xmax = xmin0, xmax0
        if twiny or mode == "x":
            ymin, ymax = ymin0, ymax0

        if direction == "in":
            new_xbound = xmin, xmax
            new_ybound = ymin, ymax

        elif direction == "out":
            x_trf = self.ax.xaxis.get_transform()
            sxmin0, sxmax0, sxmin, sxmax = x_trf.transform(
                [xmin0, xmax0, xmin, xmax])  # To screen space.
            factor = (sxmax0 - sxmin0) / (sxmax - sxmin)  # Unzoom factor.
            # Move original bounds away by
            # (factor) x (distance between unzoom box and axes bbox).
            sxmin1 = sxmin0 - factor * (sxmin - sxmin0)
            sxmax1 = sxmax0 + factor * (sxmax0 - sxmax)
            # And back to data space.
            new_xbound = x_trf.inverted().transform([sxmin1, sxmax1])

            y_trf = self.ax.yaxis.get_transform()
            symin0, symax0, symin, symax = y_trf.transform(
                [ymin0, ymax0, ymin, ymax])
            factor = (symax0 - symin0) / (symax - symin)
            symin1 = symin0 - factor * (symin - symin0)
            symax1 = symax0 + factor * (symax0 - symax)
            new_ybound = y_trf.inverted().transform([symin1, symax1])

        if new_xbound[0] < -1e200 or new_xbound[1] > 1e200 or new_ybound[0] < -1e200 or new_ybound[1] > 1e200:
            return

        if not twinx and mode != "y":
            self.ax.set_xbound(new_xbound)
        if not twiny and mode != "x":
            self.ax.set_ybound(new_ybound)

    def drag_pan(self, button, key, x, y):
        if IsPolarAxes(self.ax):
            return

        def format_deltas(key, dx, dy):
            if key == 'control':
                if abs(dx) > abs(dy):
                    dy = dx
                else:
                    dx = dy
            elif key == 'x':
                dy = 0
            elif key == 'y':
                dx = 0
            elif key == 'shift':
                if 2 * abs(dx) < abs(dy):
                    dx = 0
                elif 2 * abs(dy) < abs(dx):
                    dy = 0
                elif abs(dx) > abs(dy):
                    dy = dy / abs(dy) * abs(dx)
                else:
                    dx = dx / abs(dx) * abs(dy)
            return dx, dy

        p = self.ax._pan_start
        dx = x - p.x
        dy = y - p.y
        if dx == dy == 0:
            return
        if button == 1:
            dx, dy = format_deltas(key, dx, dy)
            result = p.bbox.translated(-dx, -dy).transformed(p.trans_inverse)
        elif button == 3:
            try:
                dx = -dx / self.ax.bbox.width
                dy = -dy / self.ax.bbox.height
                dx, dy = format_deltas(key, dx, dy)
                if self.ax.get_aspect() != 'auto':
                    dx = dy = 0.5 * (dx + dy)
                alpha = np.power(10.0, (dx, dy))
                start = np.array([p.x, p.y])
                oldpoints = p.lim.transformed(p.trans)
                newpoints = start + alpha * (oldpoints - start)
                result = (mtransforms.Bbox(newpoints)
                          .transformed(p.trans_inverse))
            except OverflowError:
                cbook._warn_external('Overflow while panning')
                return
        else:
            return

        valid = np.isfinite(result.transformed(p.trans))
        points = result.get_points().astype(object)
        # Just ignore invalid limits (typically, underflow in log-scale).
        points[~valid] = None

        if (points[:, 0][0] == None or points[:, 0][1] == None
            or points[:, 1][0] == None or points[:, 1][1] == None):
            return

        if (points[:, 0][0] < -1e200 or points[:, 0][1] > 1e200
            or points[:, 1][0] < -1e200 or points[:, 1][1] > 1e200):
            return

        self.ax.set_xlim(points[:, 0])
        self.ax.set_ylim(points[:, 1])

    def _quiver(self, *args, length=0.1, pivot='tail', normalize=False, arrow_scale = 3, angle = 15, type = 'quiver', **kwargs):
        from matplotlib.axes._axes import _process_plot_format
        # point_rotate 绕 point_center 逆时针旋转
        def Nrotate(angle, point_rotate, point_center):
            rotatex, rotatey = point_rotate
            centerx, centery = point_center
            rotatex = np.array(rotatex)
            rotatey = np.array(rotatey)
            nRotatex = (rotatex-centerx)*math.cos(angle) - (rotatey-centery)*math.sin(angle) + centerx
            nRotatey = (rotatex-centerx)*math.sin(angle) + (rotatey-centery)*math.cos(angle) + centery

            return nRotatex, nRotatey

        # point_rotate 绕 point_center 逆时针旋转
        def Srotate(angle, point_rotate, point_center):
            rotatex, rotatey = point_rotate
            centerx, centery = point_center
            rotatex = np.array(rotatex)
            rotatey = np.array(rotatey)
            sRotatex = (rotatex-centerx)*math.cos(angle) + (rotatey-centery)*math.sin(angle) + centerx
            sRotatey = (rotatey-centery)*math.cos(angle) - (rotatex-centerx)*math.sin(angle) + centery

            return sRotatex,sRotatey

        def arrows(shafts):
            pos_head = []

            for pos in shafts:
                pos_start = pos[1]
                pos_end = pos[0]
                # 计算出三分之一点
                pos_31 = [(pos_start[0] +(arrow_scale-1)*pos_end[0])/arrow_scale, (pos_start[1] +(arrow_scale-1)*pos_end[1])/arrow_scale]
                # 箭头左枝起始坐标
                pos_head.append([Srotate(math.radians(angle), pos_31, pos_end),pos_end])
                # 箭头右枝起始坐标
                pos_head.append([Nrotate(math.radians(angle), pos_31, pos_end),pos_end])

            return np.array(pos_head)

        argi = 4
        if len(args) < argi:
            raise ValueError('Wrong number of arguments. Expected %d got %d' %
                                (argi, len(args)))
        input_args = args[:argi]
        fmt = args[4]
        linestyle, marker, color = _process_plot_format(fmt)

        # extract the masks, if any
        masks = [k.mask for k in input_args
                    if isinstance(k, np.ma.MaskedArray)]
        # broadcast to match the shape
        bcast = np.broadcast_arrays(*input_args, *masks)
        input_args = bcast[:argi]
        masks = bcast[argi+1:]
        if masks:
            # combine the masks into one
            mask = functools.reduce(np.logical_or, masks)
            # put mask on and compress
            input_args = [np.ma.array(k, mask=mask).compressed()
                            for k in input_args]
        else:
            input_args = [np.ravel(k) for k in input_args]

        if any(len(v) == 0 for v in input_args):
            # No quivers, so just make an empty collection and return early
            linec_shafts = mcoll.LineCollection([], *args[argi+1:], **kwargs)
            linec_heads = mcoll.LineCollection([], *args[argi+1:], **kwargs)
            self.ax.add_collection(linec_shafts)
            self.ax.add_collection(linec_heads)
            return linec_shafts, linec_heads

        shaft_dt = np.array([0., length], dtype=float)
        # arrow_dt = shaft_dt * arrow_length_ratio

        _api.check_in_list(['tail', 'middle', 'tip'], pivot=pivot)
        if pivot == 'tail':
            shaft_dt -= length
        elif pivot == 'middle':
            shaft_dt -= length / 2

        XYZ = np.column_stack(input_args[:2])
        UVW = np.column_stack(input_args[2:argi]).astype(float)

        norm = np.linalg.norm(UVW, axis=1)

        mask = norm > 0
        XYZ = XYZ[mask]
        if normalize:
            UVW = UVW[mask] / norm[mask].reshape((-1, 1))
        else:
            UVW = UVW[mask]

        # lines_shafts=None
        # lines_heads=None

        if "linewidth" not in kwargs and "linewidths" not in kwargs:
            kwargs["linewidth"] = 1

        if type == 'feather':
            if 'linestyle' not in kwargs:
                kwargs['linestyle'] = linestyle
            if 'marker' not in kwargs:
                kwargs['marker'] = marker
            if 'color' not in kwargs:
                kwargs['color'] = color
            shafts = (XYZ - np.multiply.outer(shaft_dt, UVW)).swapaxes(0, 1)
            heads = arrows(shafts)

            line_shafts = Line2D(shafts[:, :, 0].flatten(), shafts[:, :, 1].flatten(), **kwargs)
            line_heads = Line2D(heads[:, :, 0].flatten()[:-1], heads[:, :, 1].flatten()[:-1],**kwargs)
            self.ax.add_line(line_shafts)
            self.ax.add_line(line_heads)
            return line_shafts, line_heads
        else:
            if linestyle is None:
                linestyle = '-'

            if 'linestyles' not in kwargs :
                kwargs['linestyles'] = linestyle

            shafts = (XYZ - np.multiply.outer(shaft_dt, UVW)).swapaxes(0, 1)
            heads = arrows(shafts)
            lines_shafts = [*shafts]
            lines_heads = [*heads]
            linec_shafts = mcoll.LineCollection(lines_shafts,*args[argi+1:], **kwargs)
            linec_heads = mcoll.LineCollection(lines_heads, *args[argi+1:],**kwargs)
            self.ax.add_collection(linec_shafts)
            self.ax.add_collection(linec_heads)
            return linec_shafts, linec_heads

    def _streamline(self, x, y, u, v, density=1, linewidth=None, color=None,
                cmap=None, norm=None, arrowsize=1, arrowstyle='-|>',
                minlength=0.1, transform=None, zorder=None, start_points=None,
                maxlength=4.0, integration_direction='both',**kwargs):

        grid = Grid(x, y)
        mask = StreamMask(density)
        dmap = DomainMap(grid, mask)

        if zorder is None:
            zorder = mlines.Line2D.zorder

        # default to data coordinates
        if transform is None:
            transform = self.ax.transData

        if color is None:
            color = self.ax._get_lines.get_next_color()

        if linewidth is None:
            linewidth = matplotlib.rcParams['lines.linewidth']

        line_kw = kwargs
        arrow_kw = dict(arrowstyle=arrowstyle, mutation_scale=10 * arrowsize)

        _api.check_in_list(['both', 'forward', 'backward'],
                           integration_direction=integration_direction)

        if integration_direction == 'both':
            maxlength /= 2.

        use_multicolor_lines = isinstance(color, np.ndarray)
        if use_multicolor_lines:
            if color.shape != grid.shape:
                raise ValueError("If 'color' is given, it must match the shape of "
                                 "'Grid(x, y)'")
            line_colors = []
            color = np.ma.masked_invalid(color)
        else:
            line_kw['color'] = color
            arrow_kw['color'] = color

        if isinstance(linewidth, np.ndarray):
            if linewidth.shape != grid.shape:
                raise ValueError("If 'linewidth' is given, it must match the "
                                 "shape of 'Grid(x, y)'")
            line_kw['linewidth'] = []
        else:
            line_kw['linewidth'] = linewidth
            arrow_kw['linewidth'] = linewidth

        line_kw['zorder'] = zorder
        arrow_kw['zorder'] = zorder

        # Sanity checks.
        if u.shape != grid.shape or v.shape != grid.shape:
            raise ValueError(
                "'u' and 'v' must match the shape of 'Grid(x, y)'")

        u = np.ma.masked_invalid(u)
        v = np.ma.masked_invalid(v)

        integrate = _get_integrator(u, v, dmap, minlength, maxlength,
                                    integration_direction)

        trajectories = []
        if start_points is None:
            for xm, ym in _gen_starting_points(mask.shape):
                if mask[ym, xm] == 0:
                    xg, yg = dmap.mask2grid(xm, ym)
                    t = integrate(xg, yg)
                    if t is not None:
                        trajectories.append(t)
        else:
            sp2 = np.asanyarray(start_points, dtype=float).copy()

            # Check if start_points are outside the data boundaries
            for xs, ys in sp2:
                if not (grid.x_origin <= xs <= grid.x_origin + grid.width and
                        grid.y_origin <= ys <= grid.y_origin + grid.height):
                    raise ValueError("Starting point ({}, {}) outside of data "
                                     "boundaries".format(xs, ys))

            # Convert start_points from data to array coords
            # Shift the seed points from the bottom left of the data so that
            # data2grid works properly.
            sp2[:, 0] -= grid.x_origin
            sp2[:, 1] -= grid.y_origin

            for xs, ys in sp2:
                xg, yg = dmap.data2grid(xs, ys)
                t = integrate(xg, yg)
                if t is not None:
                    trajectories.append(t)

        if use_multicolor_lines:
            if norm is None:
                norm = mcolors.Normalize(color.min(), color.max())
            cmap = cm.get_cmap(cmap)

        """
        The above part is the source code.
        The following are the changes.
        """
        list_points = []
        for t in trajectories:
            tgx, tgy = t.T
            # Rescale from grid-coordinates to data-coordinates.
            tx, ty = dmap.grid2data(tgx, tgy)
            tx += grid.x_origin
            ty += grid.y_origin

            points = np.transpose([tx, ty]).reshape(-1, 1, 2)
            list_points.append(points.tolist())

        list_streamlines = []

        for i in range(0, len(list_points)):
            _t = []

            for j in range(0, len(list_points[i])):
                _t.append(list_points[i][j][0])

            _line = self.ax.plot(np.array(_t)[:, 0],np.array(_t)[:, 1], **line_kw)

            list_streamlines.append(_line)

        self.ax.autoscale_view()

        return list_streamlines

    def _feather(self,*args,**kwargs):
        linec_feather = []
        x,y,u,v,fmt=args[:5]
        x = arrayvalue_to_ndarray(x)
        y = arrayvalue_to_ndarray(y)
        u = arrayvalue_to_ndarray(u)
        v = arrayvalue_to_ndarray(v)
        for i in range(0,len(u)):
            _line = self._quiver([x[i]],[y[i]],[u[i]],[v[i]], fmt,length = 1, arrow_scale = 5, angle = 20, type = 'feather',**kwargs)
            linec_feather.append(_line)

        self.ax.autoscale_view()

        return linec_feather

    def _compass(self, *args, **kwargs):
        from matplotlib.axes._axes import _process_plot_format

        def arrows(theta, rho,  **kwargs):
            theta_arrow = []
            rho_arrow = []
            # 箭头左枝起始坐标
            theta_arrow.append(theta[1] + math.sin(math.radians(5)))
            rho_arrow.append(rho[1] * 4 / 5)
            # 端点坐标
            theta_arrow.append(theta[1])
            rho_arrow.append(rho[1])
            # 箭头右枝起始坐标
            theta_arrow.append(theta[1] - math.sin(math.radians(5)))
            rho_arrow.append(rho[1] * 4 / 5)

            line_arrow = Line2D(theta_arrow, rho_arrow, **kwargs)
            return line_arrow

        line_compass = []
        rho = []
        z, fmt = args[:2]
        linestyle, marker, color = _process_plot_format(fmt)


        if 'linewidth' not in kwargs:
            kwargs['linewidth'] = 1
        if 'linestyle' not in kwargs:
                kwargs['linestyle'] = linestyle
        if 'marker' not in kwargs:
            kwargs['marker'] = marker
        if 'color' not in kwargs:
            kwargs['color'] = color


        for i in range(0,len(z)):
            theta=[]
            rho=[]
            for t in [0, z[i]]:
                theta.append(np.angle(t))
                rho.append(np.abs(t))
            line_shaft = Line2D(theta, rho, **kwargs)
            line_arrow = arrows(theta, rho, **kwargs)

            self.ax.add_line(line_shaft)
            self.ax.add_line(line_arrow)
            line_compass.append([line_shaft, line_arrow])
        self.ax.autoscale_view()

        return line_compass

    def set_prop(self, name: str, value):
        # name = name.lower()
        # 字体
        if name == "FontName":
            ax_setting.set_ax_fontfamily(self.ax, value)
        elif name == "FontAngle":
            ax_setting.set_ax_fontstyle(self.ax, value)
        elif name == "FontWeight":
            ax_setting.set_ax_fontweight(self.ax, value)
        elif name == "FontSize":
            ax_setting.set_ax_fontsize(self.ax, value)
        # 刻度
        elif name == "XTick":
            # ax_setting.set_ax_ticks(self.ax, "X", value)
            ax_setting.set_ax_ticks_ticklabels(self.ax, "X", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "XTickLabel":
            ax_setting.set_ax_ticklabels(self.ax, "X", value)
        elif name == "YTick":
            # ax_setting.set_ax_ticks(self.ax, "Y", value)
            ax_setting.set_ax_ticks_ticklabels(self.ax, "Y", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "YTickLabel":
            ax_setting.set_ax_ticklabels(self.ax, "Y", value)
        elif name == "XTickMode":
            ax_setting.reset_ticks(self.ax, "X", value)
            print(self.ax.get_xticklabels())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "YTickMode":
            ax_setting.reset_ticks(self.ax, "Y", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "XMinorTick":
            ax_setting.set_ax_minorticks(self.ax, "X", value)
        elif name == "YMinorTick":
            ax_setting.set_ax_minorticks(self.ax, "Y", value)
        elif name == "RTick":
            # 半径刻度值
            ax_setting.set_ax_ticks_ticklabels(self.ax, "R", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "RTickLabel":
            # 半径刻度标签
            ax_setting.set_ax_ticklabels(self.ax, "R", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "ThetaTick":
            # 用来显示线条的角度
            ax_setting.set_ax_ticks_ticklabels(self.ax, "Theta", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "ThetaTickLabel":
            # 角度线的标签
            ax_setting.set_ax_ticklabels(self.ax, "Theta", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "RTickMode":
            # 半径刻度值的选择模式
            ax_setting.reset_ticks(self.ax, "R", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "ThetaTickMode":
            # ThetaTick的选择模式
            ax_setting.reset_ticks(self.ax, "Theta", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "RMinorTick":
            # R轴上的次刻度线
            ax_setting.update_minorticks(self.ax,"X",value)
        elif name == "ThetaMinorTick":
            # 在角度线之间的次刻度线
            ax_setting.update_minorticks(self.ax,"Y",value)
        # 标尺
        elif name == "XLim":
            ax_setting.set_lim(self.ax, "X", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "XLimMode":
            ax_setting.set_limemode(self.ax, "X", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "YLim":
            ax_setting.set_lim(self.ax, "Y", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "YLimMode":
            ax_setting.set_limemode(self.ax, "Y", value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "XColor":
            ax_setting.set_xcolor(self.ax, value)
            self.fig.canvas.draw_idle()
        elif name == "YColor":
            ax_setting.set_ycolor(self.ax, value)
            self.fig.canvas.draw_idle()
        elif name == "XScale":
            ax_setting.set_xscale(self.ax, value)
        elif name == "YScale":
            ax_setting.set_yscale(self.ax, value)
        elif name == "Rlim":
            # 最小和最大半径范围
            ax_setting.set_lim(self.ax,"R",value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "RlimMode":
            # Rlim的选择模式
            ax_setting.set_limemode(self.ax,"R",value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "Thetalim":
            # 最小和最大角度值
            ax_setting.set_lim(self.ax,"Theta",value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "ThetalimMode":
            # ThetaLim的选择模式
            ax_setting.set_limemode(self.ax,"Theta",value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Ticks", value = self.get_prop_ticks())
        elif name == "RAxisLocation":
            # R轴的位置
            self.update_rlabel_position(value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.draw_idle()
        elif name == "RAxisLocationMode":
            # RAxisLocation的选择模式
            self.reset_rlabel_position(value)
            self.fig.canvas.send_event("property_update", key="Axes", child_key = "Rulers", value = self.get_prop_rulers())
            self.fig.canvas.draw_idle()
        elif name == "RColor":
            # R轴的颜色
            ax_setting.set_rcolor(self.ax,value)
            self.fig.canvas.draw_idle()
        elif name == "ThetaColor":
            # theta轴的颜色
            ax_setting.set_thetacolor(self.ax,value)
            self.fig.canvas.draw_idle()
        # 网格
        elif name == "XGrid":
            ax_setting.set_xmajorgrid_status(self.ax, value)
        elif name == "YGrid":
            ax_setting.set_ymajorgrid_status(self.ax, value)
        elif name == "GridLineStyle":
            ax_setting.set_major_linestyle(self.ax, value)
        elif name == "GridLineColor":
            ax_setting.set_major_gridcolor(self.ax, value)
        elif name == "GridLineAlpha":
            ax_setting.set_major_gridalpha(self.ax, float(value))
        elif name == "XMinorGrid":
            ax_setting.set_xminorgrid_status(self.ax, value)
        elif name == "YMinorGrid":
            ax_setting.set_yminorgrid_status(self.ax, value)
        elif name == "MinorGridLineStyle":
            ax_setting.set_minor_linestyle(self.ax, value)
        elif name == "MinorGridLineColor":
            ax_setting.set_minor_gridcolor(self.ax, value)
        elif name == "MinorGridLineAlpha":
            ax_setting.set_minor_gridalpha(self.ax, float(value))
        elif name == "RGrid":
            # 显示R轴网格线
            self.grid_y_visible(value)
            self.fig.canvas.draw_idle()
        elif name == "ThetaGrid":
            # 显示theta轴网格线
            self.grid_x_visible(value)
            self.fig.canvas.draw_idle()
        elif name == "Layer":
            # 网格线和刻度线的位置
            self.update_layer(value)
        elif name == "RMinorGrid":
            # 显示R轴次网格线
            self.minor_grid_y_visible(value)
        elif name == "ThetaMinorGrid":
            # 显示theta轴次网格线
            self.minor_grid_x_visible(value)
        # 框样式
        elif name == "Color":
            ax_setting.set_ax_color(self.ax, value)
        elif name == "LineWidth":
            ax_setting.set_ax_linewidth(self.ax, value)
        # 位置
        elif name == "Position":
            ax_setting.set_position(self.ax, value)
        elif name == "x_datum_line":
            # x轴标线
            dline = CDrawDatumLine(self.ax,"x")
            # 调用点击事件
            dline.connect()
            # dline对象需要被接收，否则对象会被回收，从而connect()不会起作用
            self.dline = dline
        elif name == "y_datum_line":
            # y轴标线
            dline = CDrawDatumLine(self.ax,"y")
            # 调用点击事件
            dline.connect()
            # dline对象需要被接收，否则对象会被回收，从而connect()不会起作用
            self.dline = dline
        elif name == "paste":
            # 做粘贴前数据量判断
            self.line_paste_before()
        elif name == "paste_reminder":
            if value:
                # 用户选择继续粘贴
                self.line_paste()
            else:
                # 用户取消粘贴
                pass

    def minor_grid_x_visible(self,state):
        if state:
            visible = True
            self.minor_tick_change(True)
            self.update_grid(state = visible, which = 'minor', linestyle = ax_setting.get_minor_linestyle(self.ax))
        else:
            visible = False
            if self.change_minor_tick:
                self.minor_tick_change(False)
            #else:
                #ax_minorticks_off()
            self.update_grid(state = visible, which = 'minor')

    def minor_tick_change(self,state):
        self.change_minor_tick = state

    def minor_grid_y_visible(self,state):
        if state:
            visible = True
            self.minor_tick_change(True)
            self.update_grid(state = visible, axis = 'y', which = 'minor', linestyle = ax_setting.get_minor_linestyle(self.ax))
            self.fig.canvas.draw_idle()
        else:
            visible = False
            if self.change_minor_tick:
                self.minor_tick_change(False)
            #else:
                #ax_minorticks_off()
            self.update_grid(state = visible, axis = 'y', which = 'minor')
            self.fig.canvas.draw_idle()

    def update_layer(self, layer):
        if layer == 'bottom':
            self.ax.xaxis.set_zorder(1.5)
            self.ax.yaxis.set_zorder(1.5)
        if layer == 'top':
            self.ax.xaxis.set_zorder(3)
            self.ax.yaxis.set_zorder(3)

    def grid_x_visible(self, state):
        if state:
            visible = True
        else:
            visible = False
        self.update_grid(state = visible)

    def grid_y_visible(self,state):
        if state:
            visible = True
        else:
            visible = False
        self.update_grid(state = visible, axis = 'y')

    def update_grid(self, which = 'major', axis = 'x', state = True, **kwargs):
        self.ax.grid(b = state, which = which, axis = axis, **kwargs)

        bx_major, by_major, bx_minor, by_minor = mw_get_grid_status(self.ax)
        if bx_major and by_major:
            mw_get_cax(self.ax).grid = True
            mw_get_cax().update_action_state()
            self.fig.canvas.draw_idle()
        else:
            mw_get_cax(self.ax).grid = False
            mw_get_cax().update_action_state()
            self.fig.canvas.draw_idle()

    def reset_rlabel_position(self,location_mode):
        if location_mode:
            self.ax.set_rlabel_position(80)
            self.ax.stale = True
            mw_get_cax(self.ax).location_auto = True
        else:
            mw_get_cax(self.ax).location_auto = False

    def update_rlabel_position(self,lineedit):
        try:
            position = float(lineedit)
        except ValueError:
            position = self.ax.get_rlabel_position()
            return

        position = position % 360

        self.ax.set_rlabel_position(position)
        self.ax.stale = True
        mw_get_cax(self.ax).location_auto = False

    def get_prop_font(self):
        prop_font = {}
        font_family, font_size, font_italic, font_weight = ax_setting.get_ax_font(self.ax)
        prop_font["FontName"] = get_chinese_name(font_family)
        prop_font["FontAngle"] = font_italic
        prop_font["FontWeight"] = font_weight
        prop_font["FontSize"] = font_size

        return prop_font

    def get_prop_ticks(self):
        prop_ticks = {}
        if isinstance(self.ax, PolarAxes):
            prop_ticks["RTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "R")]
            prop_ticks["RTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "R")
            prop_ticks["ThetaTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "Theta")]
            prop_ticks["ThetaTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "Theta")
            prop_ticks["RTickMode"] = self.tick_auto["Y"]
            prop_ticks["ThetaTickMode"] = self.tick_auto["X"]
            prop_ticks["RMinorTick"] = self.minor_tick['X']
            prop_ticks["ThetaMinorTick"] = self.minor_tick['Y']
        elif isinstance(self.ax, Axes3D):
            prop_ticks["XTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "X")]
            prop_ticks["XTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "X")
            prop_ticks["YTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "Y")]
            prop_ticks["YTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "Y")
            prop_ticks["ZTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "Z")]
            prop_ticks["ZTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "Z")
            prop_ticks["XTickMode"] = self.tick_auto["X"]
            prop_ticks["YTickMode"] = self.tick_auto["Y"]
            prop_ticks["ZTickMode"] = self.tick_auto["Z"]
        else:
            prop_ticks["XTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "X")]
            prop_ticks["XTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "X")
            prop_ticks["YTick"] = [float(i) for i in ax_setting.get_ticks(self.ax, axis = "Y")]
            prop_ticks["YTickLabel"] = ax_setting.get_ticklabels(self.ax, axis = "Y")
            prop_ticks["XTickMode"] = self.tick_auto["X"]
            prop_ticks["YTickMode"] = self.tick_auto["Y"]
            prop_ticks["XMinorTick"] = self.minor_tick["X"]
            prop_ticks["YMinorTick"] = self.minor_tick["Y"]


        return prop_ticks

    def get_prop_rulers(self):
        prop_rulers = {}
        if isinstance(self.ax, PolarAxes):
            prop_rulers["Rlim"] = ax_setting.get_lim(self.ax, "R")
            prop_rulers["RlimMode"] = ax_setting.get_limmode(self.ax, "R")
            prop_rulers["Thetalim"] = ax_setting.get_lim(self.ax, "Theta")
            prop_rulers["ThetalimMode"] = ax_setting.get_limmode(self.ax, "Theta")
            prop_rulers["RAxisLocation"] = self.ax.get_rlabel_position()
            prop_rulers["RAxisLocationMode"] = self.location_auto
            prop_rulers["RColor"] = color_to_hex(self.ax.spines['start'].get_edgecolor())
            prop_rulers["ThetaColor"] = color_to_hex(self.ax.spines['polar'].get_edgecolor())
        else:
            prop_rulers["XLim"] = ax_setting.get_lim(self.ax, "X")
            prop_rulers["XLimMode"] = ax_setting.get_limmode(self.ax, "X")
            prop_rulers["YLim"] = ax_setting.get_lim(self.ax, "Y")
            prop_rulers["YLimMode"] = ax_setting.get_limmode(self.ax, "Y")
            prop_rulers["XColor"] = color_to_hex(ax_setting.get_xcolor(self.ax))
            prop_rulers["YColor"] = color_to_hex(ax_setting.get_ycolor(self.ax))
            prop_rulers["XScale"] = ax_setting.get_xscale(self.ax)
            prop_rulers["YScale"] = ax_setting.get_yscale(self.ax)
        
        if isinstance(self.ax, Axes3D):
            prop_rulers["ZLim"] = ax_setting.get_lim(self.ax, "Z")
            prop_rulers["ZLimMode"] = ax_setting.get_limmode(self.ax, "Z")

        return prop_rulers
    
    def get_prop_grids(self):
        prop_grids = {}
        if isinstance(self.ax, PolarAxes):
            # 网格线状态
            bx_major, by_major, bx_minor, by_minor = mw_get_grid_status(self.ax)
            prop_grids["RGrid"] = by_major
            prop_grids["ThetaGrid"] = bx_major
            current_layer = None
            if self.ax.xaxis.get_zorder() == 1.5:
                current_layer = 'bottom'
            else:
                current_layer = 'top'
            prop_grids["Layer"] = current_layer
            prop_grids["RMinorGrid"] = by_minor
            prop_grids["ThetaMinorGrid"] = bx_minor
        else:
            prop_grids["XGrid"] = ax_setting.get_xmajorgrid_status(self.ax)
            prop_grids["YGrid"] = ax_setting.get_ymajorgrid_status(self.ax)
            prop_grids["XMinorGrid"] = ax_setting.get_xminorgrid_status(self.ax)
            prop_grids["YMinorGrid"] = ax_setting.get_yminorgrid_status(self.ax)

        prop_grids["GridLineStyle"] = ax_setting.get_major_linestyle(self.ax)
        prop_grids["GridLineColor"] = color_to_hex(ax_setting.get_major_gridcolor(self.ax))
        prop_grids["GridLineAlpha"] = ax_setting.get_major_gridalpha(self.ax)
        prop_grids["MinorGridLineStyle"] = ax_setting.get_minor_linestyle(self.ax)
        prop_grids["MinorGridLineColor"] = color_to_hex(ax_setting.get_minor_gridcolor(self.ax))
        prop_grids["MinorGridLineAlpha"] = ax_setting.get_minor_gridalpha(self.ax)

        return prop_grids
    
    def get_prop_labels(self):
        prop_labels = {}
        prop_labels["Title"] = ""
        prop_labels["XLabel"] = ""
        prop_labels["Ylabel"] = ""
        prop_labels["Legend"] = ""

        return prop_labels
    
    def get_prop_box_styling(self):
        prop_box_styling = {}
        prop_box_styling["Color"] = color_to_hex(ax_setting.get_ax_color(self.ax))
        prop_box_styling["LineWidth"] = ax_setting.get_ax_linewidth(self.ax)

        return prop_box_styling
    
    def get_prop_position(self):
        prop_position = {}
        prop_position["Position"] = ax_setting.get_position(self.ax)

        return prop_position

    def get_all_props(self):
        props = {}

        props["Fonts"] = self.get_prop_font()

        props["Ticks"] = self.get_prop_ticks()
        

        props["Rulers"] =  self.get_prop_rulers()

        props["Grids"] = self.get_prop_grids()

        props["Labels"] = self.get_prop_labels()

        props["BoxStyling"] = self.get_prop_box_styling()

        props["Position"] = self.get_prop_position()

        return props
    
    def get_cobjs_2d(self):
        """
        获取所有的绘图类型对象
        """
        return [self.lines,self.scatters,self.pies,self.errorbars,self.stems,
                self.bar_containers,self.areas,self.histograms,self.hists,self.contours,
                self.heatmaps,self.fimplicitlines,self.cwordclouds,self.cboxcharts,self.patchs,
                self.quivers,self.compasss,self.streamlines,self.feathers,self.feather_baselines]

    def swap_cobjs(self, start1, end1, start2, end2):
        """
        在children数组里更换当前对象与目标对象的位置
        """
        children = self.ax._children

        if end2 < end1:
            start1,end1,start2,end2 = start2,end2, start1,end1
        
        children[start2:end2+1],children[start1:end1+1] = children[start1:end1+1],children[start2:end2+1]
    
    def is_top_level(self,cobj):
        """
        判断是否是顶层对象
        """
        # 通过跟获取的最大图层对象进行对比
        return cobj == self.get_max_level()

    def get_max_level(self):
        """
        获取最大图层对象
        """
        # 不同类型绘图的列表
        cobjs_2d = self.get_cobjs_2d()
        
        max_level = float('-inf')
        max_index = 0
        max_level_plot = None
        
        for cobjs in cobjs_2d:
            for _cobj in cobjs:
                # 获取最大的zorder，如果有多个最大的zorder时，根据在children数组中的顺序判断
                if not hasattr(_cobj,"get_zorder"):
                    break
                if _cobj.get_zorder() > max_level or (_cobj.get_zorder() == max_level and _cobj.get_firstindex() > max_index):
                    max_level = _cobj.get_zorder()
                    max_index = _cobj.get_firstindex()
                    max_level_plot = _cobj
        return max_level_plot

    def is_bottom_level(self,cobj):
        """
        判断是否是底层对象
        """
        # 通过跟获取的最小底层对象进行对比
        return cobj == self.get_min_level()

    def get_min_level(self):
        """
        获取最小图层对象
        """
        # 不同类型绘图的列表
        cobjs_2d = self.get_cobjs_2d()
        
        min_level = float('inf')
        min_index = float('inf')
        min_level_plot = None
        
        for cobjs in cobjs_2d:
            for _cobj in cobjs:
                if not hasattr(_cobj,"get_zorder"):
                    break
                # 获取最小的zorder，如果有多个最小的zorder时，根据在children数组中的顺序判断
                if _cobj.get_zorder() < min_level or (_cobj.get_zorder() == min_level and _cobj.get_firstindex() < min_index):
                    min_level = _cobj.get_zorder()
                    min_index = _cobj.get_firstindex()
                    min_level_plot = _cobj
        return min_level_plot

    def set_level_top(self,cobj):
        """
        置于顶层
        """
        # 移动在_children中的位置
        start_index = cobj.get_firstindex()
        end_index = cobj.get_lastindex()
        target_array = self.ax._children[start_index:end_index+1]
        self.ax._children[:] = self.ax._children[0:start_index] + self.ax._children[end_index+1:len(self.ax._children)]
        self.ax._children[-1:-1] = target_array
        
        max_level_plot = self.get_max_level()
        # 交换zorder
        cobj.set_zorder(max_level_plot.get_zorder()+self.LEVEL_OFFSET)
        update_legend(self.ax)
        self.fig.canvas.draw_idle()

    def set_level_bottom(self,cobj):
        """
        置于底层
        """
        # 移动在_children中的位置
        start_index = cobj.get_firstindex()
        end_index = cobj.get_lastindex()
        target_array = self.ax._children[0:start_index] + self.ax._children[end_index+1:len(self.ax._children)]
        self.ax._children[:] = self.ax._children[start_index:end_index+1]
        self.ax._children.extend(target_array)
        
        min_level_plot = self.get_min_level()
        # 交换zorder
        cobj.set_zorder(min_level_plot.get_zorder()-self.LEVEL_OFFSET)
        update_legend(self.ax)
        self.fig.canvas.draw_idle()

    def set_level_up(self,cobj):
        """
        上移一层
        """
        # 整体逻辑：
        # 1.获取相同大小的zorder对象，若不存在与zorder相同的对象，再获取比zorder大的最邻近的zorder对象，返回一个数组cobjs
        # 2.获取cobjs中所有对象的firstindex，找到大于当前对象的index的最接近的对象，返回一个对象target_cobj
        # 3.互换当前对象与target_cobj的zorder
        # 4.互换当前对象与target_cobj的index
        
        # 获取相同大小的zorder对象
        zorder = cobj.get_zorder()
        next_cobj = None
        cobjs = self.get_same_zorder_cobjs(cobj)

        # 若存在与zorder相同的对象，再找到大于当前对象的index的最接近的对象 
        if len(cobjs) > 0:
            next_cobj = self.get_next_cobj(cobjs,cobj.get_firstindex(),is_same_zorder=True)

        # 若不存在与zorder相同的对象，或者存在与zorder相同的对象，但是当前对象已经是最大的index
        if next_cobj == None:
            cobjs = self.get_next_zorder_cobjs(zorder)
            next_cobj = self.get_next_cobj(cobjs,cobj.get_firstindex(),is_same_zorder=False)

        # 互换zorder
        cobj.set_zorder(next_cobj.get_zorder())
        next_cobj.set_zorder(zorder)

        # 互换index
        self.swap_cobjs(cobj.get_firstindex(),cobj.get_lastindex(),
        next_cobj.get_firstindex(),next_cobj.get_lastindex())
        update_legend(self.ax)
        self.fig.canvas.draw_idle()

    def set_level_down(self,cobj):
        """
        下移一层
        """
        # 整体逻辑：
        # 1.获取相同大小的zorder对象，若不存在与zorder相同的对象，再获取比zorder小的最邻近的zorder对象，返回一个数组cobjs
        # 2.获取cobjs中所有对象的firstindex，找到小于当前对象的index的最接近的对象，返回一个对象target_cobj
        # 3.互换当前对象与target_cobj的zorder
        # 4.互换当前对象与target_cobj的index

        # 获取相同大小的zorder对象
        zorder = cobj.get_zorder()
        previous_cobj = None
        cobjs = self.get_same_zorder_cobjs(cobj)

        # 若存在与zorder相同的对象，再找到小于当前对象的index的最接近的对象 
        if len(cobjs) > 0:
            previous_cobj = self.get_previous_cobj(cobjs,cobj.get_firstindex(),is_same_zorder=True)

        # 若不存在与zorder相同的对象，或者存在与zorder相同的对象，但是当前对象已经是最小的index
        if previous_cobj == None:
            cobjs = self.get_previous_zorder_cobjs(zorder)
            previous_cobj = self.get_previous_cobj(cobjs,cobj.get_firstindex(),is_same_zorder=False)

        # 互换zorder
        cobj.set_zorder(previous_cobj.get_zorder())
        previous_cobj.set_zorder(zorder)

        # 互换index
        self.swap_cobjs(cobj.get_firstindex(),cobj.get_lastindex(),
        previous_cobj.get_firstindex(),previous_cobj.get_lastindex())
        update_legend(self.ax)
        self.fig.canvas.draw_idle()

    def get_same_zorder_cobjs(self,cobj):
        """
        获取相同zorder的对象
        """
        cobjs_samezorder = []
        cobjs_2d = self.get_cobjs_2d()

        for cobjs in cobjs_2d:
            for _cobj in cobjs:
                if not hasattr(_cobj,"get_zorder"):
                    break
                if _cobj.get_zorder() == cobj.get_zorder() and _cobj != cobj:
                    cobjs_samezorder.append(_cobj)
        return cobjs_samezorder

    def get_next_zorder_cobjs(self,cur_zorder):
        """
        获取比zorder大的最邻近的zorder对象
        """
        re_cobjs = []
        cobjs_2d = self.get_cobjs_2d()
        # 最接近 cur_zorder 的 zorder
        closest_zorder = float("inf")
        for cobjs in cobjs_2d:
            for _cobj in cobjs:
                if not hasattr(_cobj,"get_zorder"):
                    break
                if _cobj.get_zorder() <= cur_zorder:
                    continue
                # 进入下列判断的cobj.get_zorder() 一定大于 cur_zorder
                if _cobj.get_zorder() == closest_zorder:
                    re_cobjs.append(_cobj)
                elif _cobj.get_zorder() < closest_zorder:
                    re_cobjs = [_cobj]
                    closest_zorder = _cobj.get_zorder()
        return re_cobjs

    def get_previous_zorder_cobjs(self,cur_zorder):
        """
        获取比zorder小的最邻近的zorder对象
        """
        re_cobjs = []
        cobjs_2d = self.get_cobjs_2d()
        # 最接近 cur_zorder 的 zorder
        closest_zorder = float("-inf")
        for cobjs in cobjs_2d:
            for _cobj in cobjs:
                if not hasattr(_cobj,"get_zorder"):
                    break
                if _cobj.get_zorder() >= cur_zorder:
                    continue
                # 进入下列判断的_cobj.get_zorder() 一定小于 cur_zorder
                if _cobj.get_zorder() == closest_zorder:
                    re_cobjs.append(_cobj)
                elif _cobj.get_zorder() > closest_zorder:
                    re_cobjs = [_cobj]
                    closest_zorder = _cobj.get_zorder()
        return re_cobjs

    def get_next_cobj(self,cobjs,start_index,is_same_zorder):
        """
        获取cobjs中所有对象的firstindex，找到大于当前对象的index的最接近的对象
        """
        next_cobj = None
        closets_start_index = float("inf")
        min_index = float("inf")
        for cobj in cobjs:
            if is_same_zorder and start_index < cobj.get_firstindex() < closets_start_index:
                next_cobj = cobj
                closets_start_index = cobj.get_firstindex()
            elif not is_same_zorder and cobj.get_firstindex() < min_index:
                next_cobj = cobj
                min_index = cobj.get_firstindex()

        return next_cobj

    def get_previous_cobj(self,cobjs,start_index,is_same_zorder):
        """
        获取cobjs中所有对象的firstindex，找到小于当前对象的index的最接近的对象
        """
        previous_cobj = None
        closets_start_index = float("-inf")
        max_index = float("-inf")
        for cobj in cobjs:
            if is_same_zorder and closets_start_index < cobj.get_firstindex() < start_index:
                previous_cobj = cobj
                closets_start_index = cobj.get_firstindex()
            elif not is_same_zorder and cobj.get_firstindex() > max_index:
                previous_cobj = cobj
                max_index = cobj.get_firstindex()

        return previous_cobj
    
    def xlim_changed(self, ax):
        lims = self.ax.viewLim
        if np.abs(lims.width - self.current_lim) > 1e-8:
            # 获取 x 范围的变化比
            self.current_lim = lims.width
            if mw_get_cfig(self.fig).sampling:
                self.resample()
                if self.__class__.__name__ == "CAxesYyaxis":
                    self.cax2.current_lim = lims.width
                    self.cax2.resample()

    def update_current_lim(self):
        self.current_lim = self.ax.viewLim.width

    def get_scale_factor(self):
        return self.ax.dataLim.width/self.current_lim

    def resample(self):
        if not mw_get_cfig(self.fig).sampling:
            return

        if isinstance(self.ax, PolarAxes) or isinstance(self.ax, Axes3D):
            return

        scale_factor = self.ax.dataLim.width/self.current_lim

        for cline in self.lines:
            cline.resample(scale_factor)

        for cscatter in self.scatters:
            cscatter.resample(scale_factor)

        # self.ax.figure.canvas.draw_idle()

    def unsample(self):        
        if isinstance(self.ax, PolarAxes) or isinstance(self.ax, Axes3D):
            return
            
        for cline in self.lines:
            cline.unsample()

        for cscatter in self.scatters:
            cscatter.unsample()

        # self.ax.figure.canvas.draw_idle()

    def get_pixel_aspect(self):
        """
        获取坐标轴像素高/长
        """
        ax_width, ax_height = self.ax._originalPosition.width, self.ax._originalPosition.height
        fig_width, fig_height = self.fig.get_size_inches() * self.fig.dpi
        ax_pixel_width, ax_pixel_height = ax_width * fig_width, ax_height * fig_height
        pixel_aspect =  ax_pixel_height / ax_pixel_width

        return pixel_aspect
