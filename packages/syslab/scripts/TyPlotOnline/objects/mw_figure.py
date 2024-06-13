"""
figure图窗类，用于初始化图窗界面
"""
from TyPlotOnline.objects.mw_scatter import CScatter
from TyPlotOnline.objects.mw_line import CLine
# from PyQt5.QtWidgets import QMenu
# from PyQt5.QtGui import QCursor, QColor
from matplotlib.backend_bases import MouseButton

from TyPlotOnline.objects.mw_axes import CAxes
from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.utility.mw_plotting_utils import RadialTick
from matplotlib.offsetbox import AuxTransformBox
import matplotlib.transforms as mtransforms
import numpy as np
import matplotlib.colors as mcolors

from matplotlib import cbook, rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import TransformedBbox, Bbox
import matplotlib.tight_layout as tl
import matplotlib.image as mimage
import matplotlib.projections.polar as mpolar
from matplotlib.collections import PatchCollection
from TyPlotOnline.data_tips.data_tips import Cursor
import TyPlotOnline.settings.mw_setting_figure as fig_setting
from TyPlotOnline.mw_actions import *
from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
from pathlib import Path
import os
import json

class CFigure(object):
    """
    实现图窗的一些槽函数、右键菜单等

    Attributes
    -------------------
        fig : 目标图窗
        axs : 初始化后的坐标轴列表
        pick : 当前图窗选中状态
        current_objs : 存储当前选中的对象
        edit_mode : 编辑模式
        global_font : 坐标轴全局字体
            字体名，字体大小，是否斜体，是否加粗（默认为空）
            global_font = ('DejaVu Sans', 10, False, False)
        zoom_flag : 缩放模式
        pan_flag : 平移模式
        rect : 存储绘制的矩形
        data_tips : 数据提示是否开启
    """

    def __init__(self, fig,**kwargs):
        self.init_attrs(fig)
        self.init_customize(**kwargs)
        
    def init_attrs(self, fig):
        self.fig = fig
        self.axs = []
        self.pick = False
        self.current_objs = []
        self.edit_mode = False
        self.current_mplcursor = None
        # self.global_font = ('Microsoft YaHei', 10, False, False)
        self.zoom_flag = False
        self.pan_flag = False
        self.rect = []
        self.draw_graphics = None
        self.draw_lines = []
        self.lst_draw_graphics = []
        self.drawing = False
        self.colorbars = []
        self.data_tips = False
        self.current_mplcursor = None
        self.auto_adjust_view = False
        self.data_tips_on = False
        self.colororder = [(0.00,0.45,0.74),(0.85,0.33,0.10),(0.93,0.69,0.13),
            (0.49,0.18,0.56),(0.47,0.67,0.19),(0.30,0.75,0.93),(0.64,0.08,0.18)]
        self.cursor_lines = []
        self.draw_text = None
        self.big_axes = {}
        self.prop_objs = {}
        # 用来判断当前是否进行曲线多选操作
        self.is_multiple_pick = False
        self.sampling = False
        self.min_sampling_num = 30000
        self.sampling_algorithm = "default"
        self.sampling_num = 30000
        self.x_bit = None
        self.y_bit = None
        self.sampling_draw = True

    def init_customize(self, **kwargs):
        self.current_mplcursor = Cursor(self.fig, None)

        if 'figsize' not in kwargs.keys():
            self.fig.set_size_inches(7.0, 5.2)
        if 'facecolor' not in kwargs.keys():
            if CGlobalSetting.isOnline:
                self.fig.set_facecolor('#ffffff')
            else:
                self.fig.set_facecolor('#f0f0f0')

        # if not CGlobalSetting.isOnline:
        #     self.fig.canvas.manager.window.setWindowIcon(QtGui.QIcon(CGlobalSetting.icon_path + r"matplotlib.png"))

        pos_lst = mw_get_default_ax_pos()
        self.fig.subplots_adjust(left=pos_lst[0], bottom=pos_lst[1], right=pos_lst[2], top=pos_lst[3])

        self.create_pick_state()
        #self.init_Axes()

        tl.auto_adjust_subplotpars = auto_adjust_subplotpars
        tl.get_tight_layout_figure = get_tight_layout_figure
        mpolar.RadialTick = RadialTick
        #self.fig.draw = self.draw
        self.connect()
        self.init_savefile_list()
        self.read_sampling_setting()

        # set_toolbutton_enabled(self.fig, 'AdjustMargin', not self.auto_adjust_view)
        
    def read_sampling_setting(self):
        setting_path = self.get_sampling_setting_dir()
        if os.path.exists(setting_path):
            with open(setting_path, "r") as f:
                try:
                    sampling_setting = json.load(f)
                except:
                    sampling_setting = {}
                self.sampling = sampling_setting.get("Sampling", True)
                try:
                    self.sampling = bool(self.sampling)
                except:
                    self.sampling = True

                self.min_sampling_num = sampling_setting.get("MinSamplingNum", 30000)
                try:
                    self.min_sampling_num = int(self.min_sampling_num)
                    if self.min_sampling_num < 0:
                        self.min_sampling_num = 30000
                except:
                    self.min_sampling_num = 30000

                self.sampling_algorithm = sampling_setting.get("SamplingAlgorithm", 'default')
                self.sampling_algorithm = str(self.sampling_algorithm)
                if self.sampling_algorithm not in ['default']:
                    self.sampling_algorithm = 'default'

    def write_sampling_setting(self, parent=None):
        setting_path = self.get_sampling_setting_dir()
        if not os.path.exists(setting_path):
            setting_path.parent.mkdir(parents=True, exist_ok=True)
        
        sampling_setting = {
            "Sampling": self.sampling,
            "MinSamplingNum": self.min_sampling_num,
            "SamplingAlgorithm": self.sampling_algorithm,
        }
        with open(setting_path, "w") as f:
            sampling_setting = json.dump(sampling_setting, f)

        title = "保存"
        message = f"保存成功，位于{setting_path.__str__()}"
        self.fig.canvas.send_event("show_dialog",title=title,message=message)

    def get_sampling_setting_dir(self) -> Path:
        homedir = str(Path.home())
        setting_path = Path(homedir + "/SyslabCloud/.syslab-oss/samplingSetting.json")
        return setting_path

    def __getstate__(self):
        # self.objs = {"CBar": self.bar_containers[0].__dict__}
        state = self.__dict__.copy()
        state["GlobalFont"] = CGlobalSetting.cGlobalFont
        del state["current_objs"]

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
        self.connect()

    def before_export(self):
        """
        在导出前需要处理一些属性，使figure对象可以正常序列化
        """
        self.current_edit_mode = self.edit_mode
        editmode_disable(self.fig)
        curser_disable(self.fig)
        # set_toolbutton_checked(self.fig, 'edit_mode', False)
        # set_toolbutton_checked(self.fig, 'cursor_line', False)

        if self.current_mplcursor:
            self.current_mplcursor.before_export()
        
        for cg in self.lst_draw_graphics:
            cg.before_export()

        for cl in self.draw_lines:
            cl.before_export()

        for cax in self.axs:
            cax.before_export()

    def after_export(self):
        """
        在导出完毕需要将导出前的操作影响去除
        """
        if self.current_mplcursor:
            self.current_mplcursor.after_export()

        # set_toolbutton_checked(self.fig, 'edit_mode', self.edit_mode)

        for cax in self.axs:
            cax.after_export()

        for cg in self.lst_draw_graphics:
            cg.after_export()

        for cl in self.draw_lines:
            cl.after_export()

        if self.current_edit_mode:
            editmode_enable(self.fig)

    def after_import(self):
        """
        在导入后需要重新初始化部分属性，使图窗的功能完备
        """
        if self.current_mplcursor:
            self.current_mplcursor.after_import()

        for cg in self.lst_draw_graphics:
            cg.after_import()

        for cl in self.draw_lines:
            cl.after_import()
            
        if not hasattr(self,"sampling"):
            self.sampling = True
            self.min_sampling_num = 30000
            self.sampling_algorithm = "default"
            self.sampling_num = 30000
            self.x_bit = None
            self.y_bit = None
            self.read_sampling_setting()
        
        self.create_pick_state()

        tl.auto_adjust_subplotpars = auto_adjust_subplotpars
        tl.get_tight_layout_figure = get_tight_layout_figure
        mpolar.RadialTick = RadialTick

        self.connect()
        self.init_savefile_list()

    def init_savefile_list(self):
        pop_keys = ['eps', 'pdf', 'pgf', 'ps']
        for key in pop_keys:
            if key in self.fig.canvas.filetypes.keys():
                self.fig.canvas.filetypes.pop(key)

    def connect(self):
        self.cid_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('resize_event', self.on_figure_size_change)
        self.cid_key_press = self.fig.canvas.mpl_connect(
             'key_press_event', self.on_key_press)
        self.cid_key_release = self.fig.canvas.mpl_connect(
             'key_release_event', self.on_key_release)
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event',self.scroll_zoom)

    def scroll_zoom(self,event):
        """实现鼠标滚轮缩放"""
        # https://gist.github.com/tacaswell/3144287

        figure = plt.gcf()
        if mw_get_cfig().current_mplcursor is None:
            return
        canvas = figure.canvas
        toolbar = canvas.manager.toolbar
        mode = toolbar.mode.name
        if mode != "ZOOM":
            return

        # 如果点击位置不在坐标轴内，直接返回
        if event.inaxes is None:
            return
        
        # 初始缩放比例
        base_scale = 1/0.9375
        if event.button == 'up':
            # 放大
            scl = base_scale
        elif event.button == 'down':
            # 缩小
            scl = 1/base_scale
        else:
            # 处理不应该发生的情况，设置为不缩放
            scl = 1

        # 获取所在坐标轴
        ax = event.inaxes
        # 3D坐标轴情况
        if isinstance(ax, Axes3D):
            minx, maxx, miny, maxy, minz, maxz = ax.get_w_lims()
            df = (1 - scl)
            dx = (maxx-minx)*df
            dy = (maxy-miny)*df
            dz = (maxz-minz)*df
            ax.set_xlim3d(minx - dx, maxx + dx)
            ax.set_ylim3d(miny - dy, maxy + dy)
            ax.set_zlim3d(minz - dz, maxz + dz)
            ax.get_proj()
            mw_get_cax(ax).ax3d.update_annotation()
            ax.figure.canvas.draw_idle()
        else:
            # 根据点击位置和缩放比例调用_set_view_from_bbox实现缩放，即设置视图
            ax._set_view_from_bbox([event.x, event.y, scl])

            # 处理CAxesPareto情况下的坐标轴
            if isinstance(mw_get_cax(ax),CAxesPareto):
                mw_get_cax(ax).ax._set_view_from_bbox([event.x, event.y, scl])

            # 局部重绘
            figure.canvas.draw_idle()  
            # 将当前视图保存
            toolbar.push_current()

    def on_key_press(self, event):
        if event.key == "shift":
            # 当按下shift键之后，开启多选曲线
            mw_get_cfig().is_multiple_pick = True
        elif event.key == 'ctrl+c' and len(self.axs) > 0 and self.edit_mode \
            and not isinstance(mw_get_cax().ax,Axes3D) and not isinstance(mw_get_cax().ax,PolarAxes):
            CGlobalSetting.line_copy_prop.clear()
            mw_get_cfig().set_current_objs_prop("copy", "")
            return

    def on_key_release(self,event):
        if event.key == "shift":
            # 当松开shift键之后，结束多选曲线
            mw_get_cfig().is_multiple_pick = False

    def init_Axes(self):
        for ax in self.fig.axes:
            c_ax = CAxes(ax)
            self.axs.append(c_ax)

    def on_press(self, event):
        """鼠标按下事件"""

        # 将此图窗设为当前图窗
        #plt.figure(self.fig.number)

        # if not mw_get_cfig().edit_mode:
        #     for cax in self.axs:
        #         for clegend in cax.legends:
        #             contains = clegend.contains_self(event)
        #             if contains:
        #                 clegend.on_press(event)
        #                 return
        #     return

        if self.drawing:
            return

        c_fig = mw_get_cfig()

        titles = []
        xlabels = []
        ylabels = []
        zlabels = []
        legends = []
        texts = []
        for cax in self.get_all_caxes():
            titles += cax.titles
            xlabels += cax.xlabels
            ylabels += cax.ylabels
            zlabels += cax.zlabels
            legends += cax.legends
            texts += cax.texts

        for colorbar in mw_get_cfig().colorbars:
            xlabels += colorbar.xlabels
            ylabels += colorbar.ylabels

        if len(legends) != 0:
            for c_legend in legends:
                contains = c_legend.contains_self(event)
                if contains:
                    c_legend.on_press(event)
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_legend.context_menu()
                    return

        if len(titles) != 0:
            for c_title in titles:
                contains = c_title.contains_self(event)
                if contains:
                    c_title.on_pick()
                    self.fig.sca(c_title.axes)
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_title.context_menu()
                    return

        if len(xlabels) != 0:
            for c_xlabel in xlabels:
                contains = c_xlabel.contains_self(event)
                if contains:
                    c_xlabel.on_pick()
                    self.fig.sca(c_xlabel.axes)
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_xlabel.context_menu()
                    return

        if len(ylabels) != 0:
            for c_ylabel in ylabels:
                contains = c_ylabel.contains_self(event)
                if contains:
                    c_ylabel.on_pick()
                    self.fig.sca(c_ylabel.axes)
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_ylabel.context_menu()
                    return

        if len(zlabels) != 0:
            for c_zlabel in zlabels:
                contains = c_zlabel.contains_self(event)
                if contains:
                    c_zlabel.on_pick()
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_zlabel.context_menu()
                    return

        if len(texts) != 0:
            for c_text in texts:
                contains = c_text.contains_self(event)
                if contains:
                    c_text.on_pick()
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                        c_text.context_menu()
                    return

        if len(self.draw_lines) != 0:
            for d_line in self.draw_lines:
                contains = d_line.contains_self(event)
                if contains:
                    d_line.on_pick()
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and self.edit_mode:
                        d_line.context_menu()
                    return

        if len(self.lst_draw_graphics) != 0:
            for d_graphics in self.lst_draw_graphics:
                contains = d_graphics.contains_self(event)
                if contains:
                    d_graphics.on_pick()
                    # 如果是右键则设置右键菜单
                    if event.button is MouseButton.RIGHT and self.edit_mode:
                        d_graphics.context_menu()
                    return 

        # 先判断是否在坐标轴内
        if event.inaxes:
            c_fig = mw_get_cfig()
            if len(c_fig.colorbars) != 0:
                for c_colorbar in c_fig.colorbars:
                    contains = c_colorbar.contains_self(event)
                    if contains:
                        #c_line.pick_self()
                        c_colorbar.on_press()
                        # 如果是右键则设置右键菜单
                        if event.button is MouseButton.RIGHT and c_fig.edit_mode:
                            c_colorbar.context_menu()
                        return

            current_ax = None
            for c_ax in self.get_all_caxes():
                if c_ax.ax == event.inaxes:
                    current_ax = c_ax
                    # break
                else:
                    range = c_ax.ax.get_window_extent()
                    if (event.x > range.x0 and event.x < range.x1
                        and event.y > range.y0 and event.y < range.y1):
                        current_ax = c_ax

                if current_ax != None:
                    # 判断坐标轴内是否有对象被选中
                    # TODO:其他图形的右键菜单
                    if len(current_ax.lines) != 0:
                        for c_line in current_ax.lines:
                            contains, attrd = c_line.line.contains(event)
                            if contains:
                                self.pick_yyaxis(c_line.ax)
                                #c_line.pick_self()
                                c_line.on_press()
                                # 如果是右键则设置右键菜单  
                                # is_multiple_pick的判断参考matlab，在按下shift键进行多选时，不可对曲线进行右键操作
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode\
                                    and mw_get_cfig().is_multiple_pick == False:
                                    c_line.context_menu()
                                return
                    
                    if len(current_ax.lst_datum_lines) != 0:
                        for d_datum in current_ax.lst_datum_lines:
                            contains, attrd = d_datum.line.contains(event)
                            if contains:
                                # 游标优先级高于标线
                                if mw_get_cax(event.inaxes).cursor:
                                    return
                                self.pick_yyaxis(d_datum.ax)
                                # on_pick先不设置
                                # d_datums.on_pick()
                                # 可在此处直接将d_datum对象加入到current_objs，而不用专门再写一个选中状态pick_self,同时需保证相同的对象在current_objs中最多只能有一个
                                if mw_get_cfig().current_objs.count(d_datum) == 0:
                                    mw_get_cfig().current_objs.append(d_datum)
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and not self.edit_mode:
                                    d_datum.context_menu()
                                return

                    if len(current_ax.bar_containers) != 0:
                        for c_bar in current_ax.bar_containers:
                            contains = c_bar.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_bar.ax)
                                c_bar.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_bar.context_menu()
                                return

                    if len(current_ax.bar3_containers) != 0:
                        for c_bar3 in current_ax.bar3_containers:
                            contains = c_bar3.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_bar3.ax)
                                c_bar3.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_bar3.context_menu()
                                return

                    if len(current_ax.pies) != 0:
                        for c_pie in current_ax.pies:
                            contains = c_pie.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_pie.ax)
                                c_pie.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_pie.context_menu()
                                return

                    if len(current_ax.errorbars) != 0:
                        for c_errorbars in current_ax.errorbars:
                            contains, attrd = c_errorbars.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_errorbars.ax)
                                c_errorbars.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_errorbars.context_menu()
                                return

                    if len(current_ax.stems) != 0:
                        for c_stem in current_ax.stems:
                            contains = c_stem.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_stem.ax)
                                c_stem.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_stem.context_menu()
                                return

                    if len(current_ax.scatters) != 0:
                        for c_catter in current_ax.scatters:
                            contains = c_catter.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_catter.ax)
                                c_catter.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_catter.context_menu()
                                return

                    if len(current_ax.areas) != 0:
                        for c_area in current_ax.areas:
                            contains, attrd = c_area.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_area.ax)
                                c_area.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_area.context_menu()
                                return

                    if len(current_ax.surfs) != 0:
                        for c_surf in current_ax.surfs:
                            contains, attrd = c_surf.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_surf.ax)
                                c_surf.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_surf.context_menu()
                                return

                    if len(current_ax.histograms) != 0:
                        for c_hist in current_ax.histograms:
                            contains, attrd, bar = c_hist.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_hist.ax)
                                c_hist.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_hist.context_menu()
                                return

                    if len(current_ax.histogram2s) != 0:
                        for c_histogram2 in current_ax.histogram2s:
                            contains = c_histogram2.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_histogram2.ax)
                                c_histogram2.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_histogram2.context_menu()
                                return

                    if len(current_ax.hists) != 0:
                        for c_hist in current_ax.hists:
                            contains = c_hist.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_hist.ax)
                                c_hist.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_hist.context_menu()
                                return

                    if len(current_ax.contours) != 0:
                        for c_contour in current_ax.contours:
                            contains = c_contour.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_contour.ax)
                                c_contour.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_contour.context_menu()
                                return

                    if len(current_ax.heatmaps) != 0:
                        for c_heatmap in current_ax.heatmaps:
                            contains = c_heatmap.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_heatmap.ax)
                                current_ax.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_heatmap.context_menu()
                                return

                    if len(current_ax.cimages) != 0:
                        for c_image in current_ax.cimages:
                            contains = c_image.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_image.ax)
                                c_image.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_image.context_menu()
                                return

                    if len(current_ax.fimplicitlines) != 0:
                        for c_fimplicitline in current_ax.fimplicitlines:
                            contains = c_fimplicitline.contains_self(event)
                            if contains:
                                self.pick_yyaxis(c_fimplicitline.ax)
                                c_fimplicitline.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_fimplicitline.context_menu()
                                return

                    if current_ax.cgeomap != None and current_ax.cgeomap.cdensity_plot != None:
                        cdensity_plot = current_ax.cgeomap.cdensity_plot
                        contains = cdensity_plot.contains_self(event)
                        if contains:
                            self.pick_yyaxis(cdensity_plot.ax)
                            cdensity_plot.on_press()
                            # 如果是右键则设置右键菜单
                            if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                cdensity_plot.context_menu()
                            return

                    if current_ax.cgeomap != None and current_ax.cgeomap.cbubble_plot != None:
                        cbubble_plot = current_ax.cgeomap.cbubble_plot
                        contains = cbubble_plot.contains_self(event)
                        if contains:
                            self.pick_yyaxis(cbubble_plot.ax)
                            cbubble_plot.on_press()
                            # 如果是右键则设置右键菜单
                            if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                cbubble_plot.context_menu()
                            return

                    if len(current_ax.cboxcharts) != 0:
                        for cboxchart in current_ax.cboxcharts:
                            contains = cboxchart.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cboxchart.ax)
                                cboxchart.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    pass
                                    # cboxchart.context_menu()
                                return

                    if len(current_ax.cwordclouds) != 0:
                        for cwordcloud in current_ax.cwordclouds:
                            contains = cwordcloud.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cwordcloud.ax)
                                cwordcloud.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    # cwordcloud.context_menu()
                                    pass
                                return

                    if len(current_ax.rectangles) != 0:
                        for crectangle in current_ax.rectangles:
                            contains = crectangle.contains_self(event)
                            if contains:
                                self.pick_yyaxis(crectangle.ax)
                                crectangle.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    crectangle.context_menu()
                                return

                    if len(current_ax.patchs) != 0:
                        for cpatch in current_ax.patchs:
                            contains = cpatch.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cpatch.ax)
                                cpatch.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cpatch.context_menu()
                                return

                    if len(current_ax.feathers) != 0:
                        for cfeather in current_ax.feathers:
                            contains = cfeather.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cfeather.ax)
                                cfeather.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cfeather.context_menu()
                                return

                    if len(current_ax.feather_baselines) != 0:
                        for c_line in current_ax.feather_baselines:
                            contains, attrd = c_line.line.contains(event)
                            if contains:
                                self.pick_yyaxis(c_line.ax)
                                #c_line.pick_self()
                                c_line.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    c_line.context_menu()
                                return

                    if len(current_ax.quiver3s) != 0:
                        for cquiver3 in current_ax.quiver3s:
                            contains = cquiver3.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cquiver3.ax)
                                cquiver3.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cquiver3.context_menu()
                                return

                    if len(current_ax.quivers) != 0:
                        for cquiver in current_ax.quivers:
                            contains = cquiver.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cquiver.ax)
                                cquiver.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cquiver.context_menu()
                                return

                    if len(current_ax.streamlines) != 0:
                        for cstreamline in current_ax.streamlines:
                            contains = cstreamline.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cstreamline.ax)
                                cstreamline.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cstreamline.context_menu()
                                return

                    if len(current_ax.compasss) != 0:
                        for ccompass in current_ax.compasss:
                            contains = ccompass.contains_self(event)
                            if contains:
                                self.pick_yyaxis(ccompass.ax)
                                ccompass.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    ccompass.context_menu()
                                return

                    if len(current_ax.pcolors) != 0:
                        for cpcolor in current_ax.pcolors:
                            contains = cpcolor.contains_self(event)
                            if contains:
                                self.pick_yyaxis(cpcolor.ax)
                                cpcolor.on_press()
                                # 如果是右键则设置右键菜单
                                if event.button is MouseButton.RIGHT and mw_get_cfig().edit_mode:
                                    cpcolor.context_menu()
                                return

                current_ax = None

            # 坐标轴右键菜单
            current_ax = mw_get_cax(event.inaxes)
            current_ax.on_press()

            # 判断鼠标是否在data tips上，如果是的话，不展示axes的右键菜单，从而展示data tips右键菜单
            for datatip in mw_get_cfig().current_mplcursor.selections:
                if datatip['value']['ann'].contains(event)[0]:
                    return
            
            if event.button is MouseButton.RIGHT:
                # 判断当前cfigure里是否存在CAxes对象，如果不存在则添加进来，以使得CAxes的set_prop可以起作用
                if mw_get_cfig().current_objs.count(mw_get_cax(event.inaxes)) == 0:
                    mw_get_cfig().current_objs.append(mw_get_cax(event.inaxes))
                current_ax.context_menu()
                return
            return

        c_fig = mw_get_cfig()
        if not c_fig.edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

            if "Figure" in self.prop_objs and self.prop_objs["Figure"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Figure")
            else:
                props = get_property(self)
                self.fig.canvas.send_event("property_init", props=props, current_prop="Figure", font_list = get_font_lst())

        # 图窗右键菜单
        if event.button is MouseButton.RIGHT:
            self.context_menu()

    def context_menu(self):
        """初始化右键菜单"""
        pass
        # 将右键菜单内容发送给前端
        # send_event()
        """
        context_menu = QMenu()
        action_color = context_menu.addAction('颜色...')
        context_menu.addSeparator()

        action_data_tips = context_menu.addAction('数据提示')
        if self.data_tips_on:
            action_data_tips.setCheckable(True)
            action_data_tips.setChecked(True)
        action_adjust_view = context_menu.addAction('自动调整边距')
        if self.auto_adjust_view:
            action_adjust_view.setCheckable(True)
            action_adjust_view.setChecked(True)
        context_menu.addSeparator()

        action_prop = context_menu.addAction('打开属性检查器')

        # 连接action槽函数
        action_color.triggered.connect(self.action_color)
        action_adjust_view.triggered.connect(self.action_adjust_view)
        action_data_tips.triggered.connect(self.action_data_tips)
        action_prop.triggered.connect(self.action_prop)

        context_menu.exec_(QCursor().pos())
        """

    def action_color(self):
        face_color = self.fig.get_facecolor()
        current_color = QColor.fromRgbF(face_color[0], face_color[1], face_color[2], face_color[3])

        dlg_color = DlgColor(current_color)

        if dlg_color.exec_() == QDialog.Accepted:
            color = dlg_color.get_color()
            mw_change_obj_color(color.name(),self.fig)

    def action_data_tips(self):
        self.data_tips_on = not self.data_tips_on
        # button = mw_get_toolbutton(self.fig, 'data_tips')
        # button.setEnabled(self.data_tips_on)

    def action_adjust_view(self):
        self.auto_adjust_view = not self.auto_adjust_view
        button = mw_get_toolbutton(self.fig, 'subplots')
        button.setEnabled(not self.auto_adjust_view)
        if self.auto_adjust_view:
            adjust_views(self.fig)

    def action_prop(self):
        if self.fig.get_axes() == []:
            prop_dlg = CPropertySetting()
            prop_dlg.add_tabs([[self.fig]])
            prop_dlg.set_current_index(0)
            prop_dlg.connect()
            prop_dlg.exec_()
            return

        if len(mw_get_cax().heatmaps) > 0:
            prop_dlg = CPropertySetting()
            prop_dlg.add_tabs([[self.fig], mw_get_cax().get_all_heatmaps()])
            prop_dlg.set_current_index(0)
            prop_dlg.connect()
            prop_dlg.exec_()
        else:
            prop_dlg = CPropertySetting()
            prop_dlg.add_tabs([[self.fig], [plt.gca()], mw_get_cax().get_all_lines()])
            prop_dlg.set_current_index(0)
            prop_dlg.connect()
            prop_dlg.exec_()

    def create_pick_state(self):
        width, height = self.fig.get_size_inches()*self.fig.dpi

        trans = mtransforms.blended_transform_factory(mtransforms.IdentityTransform(), mtransforms.IdentityTransform())
        self.box = AuxTransformBox(trans)
        self.pick_state = Line2D([10, 10, 10, width/2, width - 10, width - 10, width - 10, width/2],
                                    [height - 10, height/2, 10, 10, 10, height/2, height - 10, height - 10], marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785', zorder = 100)
        self.box.add_artist(self.pick_state)
        self.fig.add_artist(self.box)

        self.pick_state.set_visible(False)

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

    def on_figure_size_change(self, event = None):
        width, height = self.fig.get_size_inches()*self.fig.dpi
        self.pick_state.set_data([10, 10, 10, width/2, width - 10, width - 10, width - 10, width/2],
                                    [height - 10, height/2, 10, 10, 10, height/2, height - 10, height - 10])
        #if self.auto_adjust_view:
        adjust_views(self.fig)

    def get_all_axes(self):
        axes = []
        for c_ax in self.axs:
            axes.append(c_ax.ax)

        return axes

    def draw(self, renderer):
        # docstring inherited
        self.fig._cachedRenderer = renderer

        # draw the figure bounding box, perhaps none for white figure
        if not self.fig.get_visible():
            return

        artists = self.fig.get_children()
        artists.remove(self.fig.patch)
        artists = sorted(
            (artist for artist in artists if not artist.get_animated()),
            key=lambda artist: artist.get_zorder())

        for ax in self.fig.axes:
            locator = ax.get_axes_locator()
            if locator:
                pos = locator(ax, renderer)
                ax.apply_aspect(pos)
            else:
                ax.apply_aspect()

            for child in ax.get_children():
                if hasattr(child, 'apply_aspect'):
                    locator = child.get_axes_locator()
                    if locator:
                        pos = locator(child, renderer)
                        child.apply_aspect(pos)
                    else:
                        child.apply_aspect()

        try:
            renderer.open_group('figure', gid=self.fig.get_gid())
            if self.fig.get_constrained_layout() and self.fig.axes:
                self.fig.execute_constrained_layout(renderer)
            if self.fig.get_tight_layout() and self.fig.axes:
                try:
                    self.fig.tight_layout(**self.fig._tight_parameters)
                except ValueError:
                    pass
                    # ValueError can occur when resizing a window.

            # if self.auto_adjust_view:
            #     adjust_views(self.fig)

            self.fig.patch.draw(renderer)
            mimage._draw_list_compositing_images(
                renderer, self.fig, artists, self.fig.suppressComposite)

            renderer.close_group('figure')
        finally:
            self.fig.stale = False

        self.fig.canvas.draw_event(renderer)

    def get_all_caxes(self):
        all_axes = []
        for cax in self.axs:
            all_axes.append(cax)
            # if isinstance(cax, CAxesYyaxis):
            #     all_axes.append(cax.cax2)
        return all_axes

    def pick_yyaxis(self, ax):
        cax = mw_get_cax(ax)
        # if isinstance(cax, CAxesYyaxis):
        #     plt.sca(ax)

    def set_prop(self, name: str, value):
        if name == "BackgroundColor":
            fig_setting.set_color(self, value)
            self.fig.canvas.draw_idle()
        elif name == "AutoAdjustView":
            fig_setting.set_auto_adjust_view(self, value)
        elif name == "DataTipsOn":
            fig_setting.set_data_tips_on(self, value)
        elif name == "Sampling":
            fig_setting.open_sampling(self,value)
        elif name == "MinSamplingNum":
            fig_setting.set_samplingnum(self,value)
        elif name == "SamplingAlgorithm":
            fig_setting.change_sampling_algorithm(self,value)
        elif name == "SaveSamplingSetting":
            self.write_sampling_setting()
        elif name == "prop":
            pass

    def set_current_objs_prop(self, name, value):
        for current_obj in self.current_objs:
            current_obj.set_prop(name, value)

    def get_all_props(self):
        props = {}
        prop_Color = {}
        prop_Color["BackgroundColor"] = color_to_hex(fig_setting.get_color(self))
        props["Color"] = prop_Color
        
        prop_Setting = {}
        prop_Setting["AutoAdjustView"] = self.auto_adjust_view
        prop_Setting["DataTipsOn"] = self.data_tips_on
        props["Setting"] = prop_Setting

        cfig = mw_get_cfig(self.fig)
        sampling_setting = False
        for cax in cfig.axs:
            if not isinstance(cax.ax, Axes3D) \
                and not isinstance(cax.ax, PolarAxes) \
                and (len(cax.lines) > 0 or len(cax.scatters) > 0):
                    sampling_setting = True

        if sampling_setting:
            prop_sampling = {}
            prop_sampling["Sampling"] = self.sampling
            prop_sampling["MinSamplingNum"] = str(self.min_sampling_num)
            prop_sampling["SamplingAlgorithm"] = str(self.sampling_algorithm)
            props["Sampling"] = prop_sampling
        return props
    
# 更新cfigure的成员
def mw_update_caxes(current_fig, current_axs):
    c_fig = mw_get_cfig(current_fig)
    for current_ax in current_axs:
        if mw_get_cax(current_ax) == None:
            c_ax = CAxes(current_ax)
            c_fig.axs.append(c_ax)

def mw_update_caxe(current_fig, current_ax, position=[1,1,1]):
    c_fig = mw_get_cfig(current_fig)
    if mw_get_cax(current_ax) == None:
        c_ax = CAxes(current_ax, position)
        c_fig.axs.append(c_ax)

def mw_update_clines(current_fig, current_lines,is_zorder_custom=False):
    c_fig = mw_get_cfig(current_fig)
    for current_line in current_lines:
        current_ax = current_line.axes
        c_ax = mw_get_cax(current_ax, True)
        if c_ax == None:
            new_ax = CAxes(current_ax)
            c_fig.axs.append(new_ax)

            c_line = CLine(current_line)
            new_ax.lines.append(c_line)
            c_ax = new_ax
            if not is_zorder_custom:
                c_line.set_zorder(c_ax.get_max_level().get_zorder()+c_ax.LEVEL_OFFSET)
                update_legend(current_ax)
        else:
            if mw_get_cline(current_line) == None:
                c_line = CLine(current_line)
                c_ax.lines.append(c_line)
                if not is_zorder_custom:
                    c_line.set_zorder(c_ax.get_max_level().get_zorder()+c_ax.LEVEL_OFFSET)
                    update_legend(current_ax)
        
        if c_fig.sampling:
            # c_ax.update_current_lim()
            c_line.resample(c_ax.get_scale_factor())

        if c_ax.is_3d:
            #c_ax.action_grid()
            set_toolbutton_enabled(current_fig, 'Cursor', False)

def mw_update_scatters(current_fig, current_scatters, is_zorder_custom=False,**special_kwargs):
    c_fig = mw_get_cfig(current_fig)
    for current_scatter in current_scatters:
        current_ax = current_scatter.axes
        c_ax = mw_get_cax(current_ax, True)

        if c_ax == None:
            new_ax = CAxes(current_ax)
            c_fig.axs.append(new_ax)
            c_scatter = CScatter(current_scatter, **special_kwargs)
            new_ax.scatters.append(c_scatter)
            if not is_zorder_custom:
                c_scatter.set_zorder(c_ax.get_max_level().get_zorder()+c_ax.LEVEL_OFFSET)
                update_legend(current_ax)
        elif mw_get_cscatter(current_scatter) == None:
            c_scatter = CScatter(current_scatter, **special_kwargs)
            c_ax.scatters.append(c_scatter)
            if not is_zorder_custom:
                c_scatter.set_zorder(c_ax.get_max_level().get_zorder()+c_ax.LEVEL_OFFSET)
                update_legend(current_ax)

        if c_fig.sampling:
            c_ax.update_current_lim()
            c_scatter.resample(c_ax.get_scale_factor())
            
    # set_toolbutton_enabled(current_fig, 'Cursor', False)
    # plt.pause(0.01)

def auto_adjust_subplotpars(
        fig, renderer, nrows_ncols, num1num2_list, subplot_list,
        ax_bbox_list=None, pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Return a dict of subplot parameters to adjust spacing between subplots
    or ``None`` if resulting axes would have zero height or width.

    Note that this function ignores geometry information of subplot
    itself, but uses what is given by the *nrows_ncols* and *num1num2_list*
    parameters.  Also, the results could be incorrect if some subplots have
    ``adjustable=datalim``.

    Parameters
    ----------
    nrows_ncols : Tuple[int, int]
        Number of rows and number of columns of the grid.
    num1num2_list : List[int]
        List of numbers specifying the area occupied by the subplot
    subplot_list : list of subplots
        List of subplots that will be used to calculate optimal subplot_params.
    pad : float
        Padding between the figure edge and the edges of subplots, as a
        fraction of the font size.
    h_pad, w_pad : float
        Padding (height/width) between edges of adjacent subplots, as a
        fraction of the font size.  Defaults to *pad*.
    rect : Tuple[float, float, float, float]
        [left, bottom, right, top] in normalized (0, 1) figure coordinates.
    """
    rows, cols = nrows_ncols

    font_size_inches = (
        FontProperties(size=rcParams["font.size"]).get_size_in_points() / 72)
    pad_inches = pad * font_size_inches
    vpad_inches = h_pad * font_size_inches if h_pad is not None else pad_inches
    hpad_inches = w_pad * font_size_inches if w_pad is not None else pad_inches

    if len(num1num2_list) != len(subplot_list) or len(subplot_list) == 0:
        raise ValueError

    if rect is None:
        margin_left = margin_bottom = margin_right = margin_top = None
    else:
        margin_left, margin_bottom, _right, _top = rect
        margin_right = 1 - _right if _right else None
        margin_top = 1 - _top if _top else None

    vspaces = np.zeros((rows + 1, cols))
    hspaces = np.zeros((rows, cols + 1))

    if ax_bbox_list is None:
        ax_bbox_list = [
            Bbox.union([ax.get_position(original=True) for ax in subplots])
            for subplots in subplot_list]

    for subplots, ax_bbox, (num1, num2) in zip(subplot_list,
                                               ax_bbox_list,
                                               num1num2_list):
        if all(not ax.get_visible() for ax in subplots):
            continue

        bb = []
        for ax in subplots:
            if ax.get_visible():
                try:
                    bb += [ax.get_tightbbox(renderer, for_layout_only=True)]
                except TypeError:
                    bb += [ax.get_tightbbox(renderer)]

        tight_bbox_raw = Bbox.union(bb)
        tight_bbox = TransformedBbox(tight_bbox_raw,
                                     fig.transFigure.inverted())

        row1, col1 = divmod(num1, cols)
        if num2 is None:
            num2 = num1
        row2, col2 = divmod(num2, cols)

        for row_i in range(row1, row2 + 1):
            hspaces[row_i, col1] += ax_bbox.xmin - tight_bbox.xmin  # left
            hspaces[row_i, col2 + 1] += tight_bbox.xmax - ax_bbox.xmax  # right
        for col_i in range(col1, col2 + 1):
            vspaces[row1, col_i] += tight_bbox.ymax - ax_bbox.ymax  # top
            vspaces[row2 + 1, col_i] += ax_bbox.ymin - tight_bbox.ymin  # bot.

    fig_width_inch, fig_height_inch = fig.get_size_inches()

    # margins can be negative for axes with aspect applied, so use max(, 0) to
    # make them nonnegative.
    if not margin_left:
        margin_left = (max(hspaces[:, 0].max(), 0)
                       + pad_inches / fig_width_inch)
    if not margin_right:
        margin_right = (max(hspaces[:, -1].max(), 0)
                        + pad_inches / fig_width_inch)
    if not margin_top:
        margin_top = (max(vspaces[0, :].max(), 0)
                      + pad_inches / fig_height_inch)
        suptitle = fig._suptitle
        if suptitle and suptitle.get_in_layout():
            rel_suptitle_height = fig.transFigure.inverted().transform_bbox(
                suptitle.get_window_extent(renderer)).height
            margin_top += rel_suptitle_height + pad_inches / fig_height_inch
    if not margin_bottom:
        margin_bottom = (max(vspaces[-1, :].max(), 0)
                         + pad_inches / fig_height_inch)

    if margin_left + margin_right >= 1:
        # cbook._warn_external('Tight layout not applied. The left and right '
        #                      'margins cannot be made large enough to '
        #                      'accommodate all axes decorations. ')
        return None
    if margin_bottom + margin_top >= 1:
        # cbook._warn_external('Tight layout not applied. The bottom and top '
        #                      'margins cannot be made large enough to '
        #                      'accommodate all axes decorations. ')
        return None

    kwargs = dict(left=margin_left,
                  right=1 - margin_right,
                  bottom=margin_bottom,
                  top=1 - margin_top)

    if cols > 1:
        hspace = hspaces[:, 1:-1].max() + hpad_inches / fig_width_inch
        # axes widths:
        h_axes = (1 - margin_right - margin_left - hspace * (cols - 1)) / cols
        if h_axes < 0:
            # cbook._warn_external('Tight layout not applied. tight_layout '
            #                      'cannot make axes width small enough to '
            #                      'accommodate all axes decorations')
            return None
        else:
            kwargs["wspace"] = hspace / h_axes
            if kwargs["wspace"] < 0.4:
                kwargs["wspace"] = 0.4
            # print(kwargs["wspace"])
    if rows > 1:
        vspace = vspaces[1:-1, :].max() + vpad_inches / fig_height_inch
        v_axes = (1 - margin_top - margin_bottom - vspace * (rows - 1)) / rows
        if v_axes < 0:
            # cbook._warn_external('Tight layout not applied. tight_layout '
            #                      'cannot make axes height small enough to '
            #                      'accommodate all axes decorations')
            return None
        else:
            kwargs["hspace"] = vspace / v_axes
            if kwargs["hspace"] < 0.4:
                kwargs["hspace"] = 0.4
            # print(kwargs["hspace"])

    return kwargs

def get_tight_layout_figure(fig, axes_list, subplotspec_list, renderer,
                            pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Return subplot parameters for tight-layouted-figure with specified padding.

    Parameters
    ----------
    fig : Figure
    axes_list : list of Axes
    subplotspec_list : list of `.SubplotSpec`
        The subplotspecs of each axes.
    renderer : renderer
    pad : float
        Padding between the figure edge and the edges of subplots, as a
        fraction of the font size.
    h_pad, w_pad : float
        Padding (height/width) between edges of adjacent subplots.  Defaults to
        *pad*.
    rect : Tuple[float, float, float, float], optional
        (left, bottom, right, top) rectangle in normalized figure coordinates
        that the whole subplots area (including labels) will fit into.
        Defaults to using the entire figure.

    Returns
    -------
    subplotspec or None
        subplotspec kwargs to be passed to `.Figure.subplots_adjust` or
        None if tight_layout could not be accomplished.

    """

    subplot_list = []
    nrows_list = []
    ncols_list = []
    ax_bbox_list = []

    # Multiple axes can share same subplot_interface (e.g., axes_grid1); thus
    # we need to join them together.
    subplot_dict = {}

    subplotspec_list2 = []

    for ax, subplotspec in zip(axes_list, subplotspec_list):
        if subplotspec is None:
            continue

        subplots = subplot_dict.setdefault(subplotspec, [])

        if not subplots:
            myrows, mycols, _, _ = subplotspec.get_geometry()
            nrows_list.append(myrows)
            ncols_list.append(mycols)
            subplotspec_list2.append(subplotspec)
            subplot_list.append(subplots)
            ax_bbox_list.append(subplotspec.get_position(fig))

        subplots.append(ax)

    if len(nrows_list) == 0 or len(ncols_list) == 0:
        return {}

    max_nrows = max(nrows_list)
    max_ncols = max(ncols_list)

    num1num2_list = []
    for subplotspec in subplotspec_list2:
        rows, cols, num1, num2 = subplotspec.get_geometry()
        div_row, mod_row = divmod(max_nrows, rows)
        div_col, mod_col = divmod(max_ncols, cols)
        if mod_row != 0:
            # cbook._warn_external('tight_layout not applied: number of rows '
            #                      'in subplot specifications must be '
            #                      'multiples of one another.')
            return {}
        if mod_col != 0:
            # cbook._warn_external('tight_layout not applied: number of '
            #                      'columns in subplot specifications must be '
            #                      'multiples of one another.')
            return {}

        rowNum1, colNum1 = divmod(num1, cols)
        if num2 is None:
            rowNum2, colNum2 = rowNum1, colNum1
        else:
            rowNum2, colNum2 = divmod(num2, cols)

        num1num2_list.append((rowNum1 * div_row * max_ncols +
                              colNum1 * div_col,
                              ((rowNum2 + 1) * div_row - 1) * max_ncols +
                              (colNum2 + 1) * div_col - 1))

    kwargs = auto_adjust_subplotpars(fig, renderer,
                                     nrows_ncols=(max_nrows, max_ncols),
                                     num1num2_list=num1num2_list,
                                     subplot_list=subplot_list,
                                     ax_bbox_list=ax_bbox_list,
                                     pad=pad, h_pad=h_pad, w_pad=w_pad)

    # kwargs can be none if tight_layout fails...
    if rect is not None and kwargs is not None:
        # if rect is given, the whole subplots area (including
        # labels) will fit into the rect instead of the
        # figure. Note that the rect argument of
        # *auto_adjust_subplotpars* specify the area that will be
        # covered by the total area of axes.bbox. Thus we call
        # auto_adjust_subplotpars twice, where the second run
        # with adjusted rect parameters.

        left, bottom, right, top = rect
        if left is not None:
            if left < kwargs["left"]:
                left = kwargs["left"]
            #left += kwargs["left"]
        if bottom is not None:
            if bottom < kwargs["bottom"]:
                bottom = kwargs["bottom"]
            #bottom += kwargs["bottom"]
        if right is not None:
            if right > kwargs["right"]:
                right = kwargs["right"]
            #right -= (1 - kwargs["right"])
        if top is not None:
            if top > kwargs["top"]:
                top = kwargs["top"]
            #top -= (1 - kwargs["top"])

        kwargs = auto_adjust_subplotpars(fig, renderer,
                                         nrows_ncols=(max_nrows, max_ncols),
                                         num1num2_list=num1num2_list,
                                         subplot_list=subplot_list,
                                         ax_bbox_list=ax_bbox_list,
                                         pad=pad, h_pad=h_pad, w_pad=w_pad,
                                         rect=(left, bottom, right, top))

    return kwargs
