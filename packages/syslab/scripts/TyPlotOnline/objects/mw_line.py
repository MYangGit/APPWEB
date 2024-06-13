"""
名称：line
功能：此文件用于初始化曲线
实现：实现曲线的事件、槽函数、右键菜单等
接口：曲线类
依赖：
"""

from mpl_toolkits.mplot3d.art3d import Line3D
# from PyQt5.QtWidgets import QMenu, QAction
# from PyQt5.QtGui import QCursor

# from settings.mw_setting_base import CPropertySetting
from TyPlotOnline.objects.mw_interface import *
# from objects.mw_plot3 import*
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
import copy

import numpy as np

class CLine(object):
    """
    实现曲线的一些槽函数、右键菜单等

    Attributes:
        line：目标曲线
    """
    def __init__(self, line):
        self.init_attrs(line)
        self.init_customize(line)
    
    def init_attrs(self, line):
        self.line = line
        self.press = None
        self.background = None
        self.select_points = []
        self.pick = False
        self.originDataX = None
        self.originDataY = None
        self.sampled = False
        # self.line.set_linewidth(0.5)

        #没有*
        #没有六角形
        # TODO：还具有matlab不具有的形状，暂未列出
        self.dict_marker = {'+' : ['+'],
                            'o' : ['o'],
                            '.' : ['.'],
                            'x' : ['x'],
                            '四方形' : ['s'],
                            '菱形' : ['D', 'd'],
                            'v' : ['v'],
                            '^' : ['^'],
                            '>' : ['>'],
                            '<' : ['<'],
                            '五角形' : ['*'],
                            '无' : ['None', ' ', '', 'none']}

        self.dict_style = {'实线' : ['-', 'solid'],
                            '虚线' : ['--', 'dashed'],
                            '点线' : [':', 'dotted'],
                            '点划线' : ['-.', 'dashdot'],
                            '无' : ['None', ' ', '', 'none']}

    def init_customize(self, line):
        self.line.set_markeredgewidth(self.line.get_linewidth())
        self.ax = self.line.axes
        self.fig = self.line.get_figure()
        self.connect()
        self.init_origin_data()

    def init_origin_data(self):
        self.originDataX = self.line.get_xdata()
        self.originDataY = self.line.get_ydata() 

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

    def after_import(self):
        self.connect()

    def set_zorder(self,zorder):
        self.line.zorder = zorder
        self.fig.canvas.draw_idle()

    def get_zorder(self):
        return self.line.zorder

    def get_firstindex(self):
        return self.ax._children.index(self.line)

    def get_lastindex(self):
        return self.ax._children.index(self.line)

    def connect(self):
        self.cid_key_press = self.ax.figure.canvas.mpl_connect(
             'key_press_event', self.on_key_press)
        # self.cidpress = self.line.figure.canvas.mpl_connect(
        #     'button_press_event', self.on_press)
    
    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_key_press)

    def on_key_press(self, event):
        if self.pick and (event.key == 'delete' or event.key == 'backspace'):
            self.delete_self()
            update_legend(self.ax)
            return

    def on_press(self, event):
        if (event.inaxes != self.line.axes):
            return

        contains, attrd = self.line.contains(event)
        if not contains:
            return

        if not mw_get_cfig().edit_mode:
            return

        #按键仅选中
        self.pick_self()

    def on_press(self):
        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            # 非多选曲线情况下，可清除曲线选中状态
            if mw_get_cfig().is_multiple_pick == False:
                mw_clear_status()
            self.pick_self()
            
            cfig = mw_get_cfig(self.fig)
            if "Line" in cfig.prop_objs and cfig.prop_objs["Line"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Line")
            else:
                cax = mw_get_cax(self.ax)
                props = get_property(cfig, cax, self, "Line")
                self.fig.canvas.send_event("property_init", props=props, current_prop="Line", font_list = get_font_lst())
        elif self.pick and mw_get_cfig().is_multiple_pick == True:
            # 多选时，对于选中的曲线，再次点击可以取消选中
            self.dis_pick_self()
            # 取消选中时，将当前曲线从current_objs删除，避免在粘贴或者再次选中时出问题
            mw_get_cfig().current_objs.remove(self)
            # 当所有曲线都取消选中时，默认选中Figure，属性面板也切换到Figure
            if len(mw_get_cfig().current_objs) == 0:
                mw_clear_status()
                mw_get_cfig().pick_self()
                self.fig.canvas.send_event("property_change", current_prop="Figure")


    def pick_self(self, pick_only = False):
        """曲线选中状态"""
        # 当前曲线选中时，开启对当前曲线的复制快捷键监听
        line_xdata = self.line.get_xdata()
        line_ydata = self.line.get_ydata()
        line_zdata = None
        if isinstance(self.line, Line3D):
            line_xdata,line_ydata,line_zdata = self.line.get_data_3d()

        arr_index = self.get_index(line_xdata)
        x_data = []
        y_data = []
        z_data = []
        for index in arr_index:
            x_data.append(line_xdata[index])
            y_data.append(line_ydata[index])
            #z_data.append(line_zdata[index])

        if isinstance(self.line, Line3D):
            for index in arr_index:
                z_data.append(line_zdata[index])

            pick_line = Line3D(x_data,y_data,z_data, marker = 's',clip_on = True,linestyle='none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)

            pick_line.set_transform(self.ax.transData)
            pick_line.set_clip_box(self.ax.bbox)
            self.fig.add_artist(pick_line)
            pick_line.axes = self.ax
            self.select_points.append(pick_line)
        else:
            # pick_line = self.line.axes.plot(x_data,y_data,'s',clip_on = True,
            #     markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)[0]
            pick_line = Line2D(x_data,y_data,marker = 's',clip_on = True, linestyle='none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)
            pick_line.set_transform(self.ax.transData)
            pick_line.set_clip_box(self.ax.bbox)
            self.fig.add_artist(pick_line)
            pick_line.axes = self.ax
            self.select_points.append(pick_line)

        self.pick = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)
        self.fig.canvas.draw_idle()

    def get_index(self, arr, numElems = 16):
        '''获取选中点下标序列'''
        if len(arr) <= 16:
            return np.arange(len(arr))
        else:
            return np.round(np.linspace(0, len(arr) - 1, numElems)).astype(int)

    def dis_pick_self(self):
        """取消选中状态"""
        # 取消选中当前曲线时，关闭当前曲线的复制快捷键监听
        for point in self.select_points:
            point.remove()

        self.select_points.clear()
        self.pick = False
        self.fig.canvas.draw_idle()

    def get_self_ax(self):
        return self.line

    def context_menu(self):
        menu_list = []
        cax = mw_get_cax()
        # 曲线层级调整右键菜单前置判断
        # 判断是否是顶层图层
        istop = cax.is_top_level(self)
        # 判断是否是底层图层
        isbottom = cax.is_bottom_level(self)
        # 判断当前是否多选
        ismultipick = len(mw_get_cfig().current_objs) > 1
        copy_disable = isinstance(self.ax,PolarAxes) or isinstance(mw_get_cax().ax,Axes3D)
        menu_list.append({"value": "copy", "label": "复制", "children": [], "default_value": "","disabled":copy_disable})

        # delete
        menu_list.append({"value": "delete", "label": "删除", "children": [], "default_value":""})

        # color
        color_list = []
        line_color = mcolors.to_hex(self.line.get_color())
        menu_list.append({"value": "color", "label": "颜色...", "children": color_list, "default_value": line_color})

        # linestyle
        lst_linestyle_dict = []
        linestyle = self.line.get_linestyle()
        for key, value in self.dict_style.items():
            lst_linestyle_dict.append({"label": key, "value": value[0]})
            if linestyle in value:
                linestyle = value[0]
        menu_list.append({"value": "linestyle", "label": "线型", "children": lst_linestyle_dict, "default_value":linestyle})

        # linewith
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        lineswidth = self.line.get_linewidth()
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "linewidth", "label": "线宽", "children": lst_linewidth_dict, "default_value":lineswidth})

        # marker
        lst_marker_dict = []
        marker = self.line.get_marker()
        for key, value in self.dict_marker.items():
            lst_marker_dict.append({"label": key, "value": value[0]})
            if marker in value:
                marker = value[0]
        menu_list.append({"value": "marker", "label": "标记", "children": lst_marker_dict, "default_value":marker})

        # markersize
        lst_markersize_label = [2, 4, 5, 6, 7, 8, 9, 10, 12, 18, 24, 48]
        lst_markersize_value = ['2','4','5','6','7','8','9','10','12','18','24','48']
        lst_markersize_dict = []
        markersize = self.line.get_markersize()
        for i in range(0, len(lst_markersize_label)):
            markersize_dict = {"label": lst_markersize_label[i], "value": lst_markersize_value[i]}
            lst_markersize_dict.append(markersize_dict)

        menu_list.append({"value": "markersize", "label": "标记大小", "children": lst_markersize_dict, "default_value": str(int(markersize))})

        # 置于顶层与上移一层
        lst_leveltop_label = ['置于顶层','上移一层']
        lst_leveltop_value = ['level_top','level_up']
        lst_leveltop_dict = []
        for i in range(0,len(lst_leveltop_label)):
            leveltop_dict = {"label":lst_leveltop_label[i],"value":lst_leveltop_value[i]}
            lst_leveltop_dict.append(leveltop_dict)
        level_top_disable = istop or ismultipick
        menu_list.append({"value":"top_level","label":"置于顶层","children":lst_leveltop_dict,"default_value":"","disabled":level_top_disable})

        # 置于底层与下移一层
        lst_levelbottom_label = ['置于底层','下移一层']
        lst_levelbottom_value = ['level_bottom','level_down']
        lst_levelbottom_dict = []
        for i in range(0,len(lst_levelbottom_label)):
            levelbottom_dict = {"label":lst_levelbottom_label[i],"value":lst_levelbottom_value[i]}
            lst_levelbottom_dict.append(levelbottom_dict)
        level_bottom_disable = isbottom or ismultipick
        menu_list.append({"value":"bottom_level","label":"置于底层","children":lst_levelbottom_dict,"default_value":"","disabled":level_bottom_disable})
        
        # prop
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "Line"})

        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    def set_color(self, color):
        self.line.set_color(color)
        update_legend(self.ax)

    #  曲线样式
    def set_linestyle(self, style): 
        self.line.set_linestyle(style)
        update_legend(self.ax)

    # 曲线线宽
    def set_linewidth(self, linewidth):
        self.line.set_linewidth(linewidth)
        self.line.set_markeredgewidth(linewidth)
        update_legend(self.ax)

    # marker
    def set_marker(self, marker):
        self.line.set_marker(marker)
        update_legend(self.ax)

    # markersize
    def set_markersize(self, markersize):
        self.line.set_markersize(markersize)
        update_legend(self.ax)

    # 属性面板
    def action_prop(self):
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.fig.gca()], [self.line]])
        prop_dlg.set_current_index(2)
        prop_dlg.connect()
        prop_dlg.exec_()

    def line_copy(self):
        # 获取当前line的dict
        prop = copy.copy(self.line.__dict__)
        
        # 下列属性会影响曲线的显示及删除，因此需在更新属性前删除
        keys_to_remove = ['_transformed_path', 'clipbox', '_transform', 'figure', '_remove_method','_clippath']
        for key in keys_to_remove:
            if key in prop:
                del prop[key]

        CGlobalSetting.line_copy_prop.append(prop)

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.ax).lines.remove(self)
        self.line.remove()
        # 更新Axes范围以适应剩余曲线
        self.ax.relim()
        # 自动调整坐标轴范围
        self.ax.autoscale_view()

    
    def set_prop(self, name, value):
        name = name.lower()

        dict_marker = {'+' : ['+'],
                'o' : ['o'],
                '.' : ['.'],
                'x' : ['x'],
                'square' : ['s'],
                'diamond' : ['D', 'd'],
                'v' : ['v'],
                '^' : ['^'],
                '>' : ['>'],
                '<' : ['<'],
                'pentagram' : ['*'],
                '|' : ['|'],
                '_' : ['_'],
                'none' : ['None', ' ', '', 'none']}

        if name == "color":
            self.set_color(value)
            update_legend(self.ax)
        elif name == "linestyle":
            self.set_linestyle(value)
            update_legend(self.ax)
        elif name == "linewidth":
            self.set_linewidth(value)
            update_legend(self.ax)
        elif name == "marker":
            if value in self.dict_marker:
                value = self.dict_marker[value][0]
            elif value in dict_marker:
                value = dict_marker[value][0]
            # value = "None" if value == "none" else value

            self.set_marker(value)
            update_legend(self.ax)
        elif name == "markersize":
            self.set_markersize(value)
            update_legend(self.ax)
        elif name == "markeredgecolor":
            self.line.set_markeredgecolor(value)
            update_legend(self.ax)
        elif name == "markerfacecolor":
            self.line.set_markerfacecolor(value)
            update_legend(self.ax)
        elif name == "displayname":
            self.line.set_label(value)
            update_legend(self.ax)
        elif name == "delete":
            self.delete_self()
            update_legend(self.ax)
        elif name == "prop":
            # 属性面板
            pass
        elif name == "copy":
            self.line_copy()
        elif name == "top_level":
            if value == "level_top":
                mw_get_cax().set_level_top(self)
            elif value == "level_up":
                mw_get_cax().set_level_up(self)
        elif name == "bottom_level":
            if value == "level_bottom":
                mw_get_cax().set_level_bottom(self)
            elif value == "level_down":
                mw_get_cax().set_level_down(self)

        if name in ["color", "linestyle", "linewidth"]:
            self.fig.canvas.send_event("property_update", key="Line", child_key = "ColorAndStyle", value = self.get_color_and_style())
        
    def get_color_and_style(self):
        props_ColorAndStyle = {}
        props_ColorAndStyle["Color"] = color_to_hex(self.line.get_color())
        props_ColorAndStyle["LineStyle"] = self.line.get_linestyle()
        props_ColorAndStyle["LineWidth"] = self.line.get_linewidth()
        return props_ColorAndStyle

    def get_markers(self):
        props_Markers = {}
        props_Markers["Marker"] = self.line.get_marker()
        props_Markers["MarkerSize"] = self.line.get_markersize()
        props_Markers["MarkerEdgeColor"] = color_to_hex(self.line._markeredgecolor)
        props_Markers["MarkerFaceColor"] = color_to_hex(self.line._markerfacecolor)
        return props_Markers
    
    def get_legend(self):
        props_Legend = {}
        props_Legend["DisplayName"] = self.line.get_label()
        return props_Legend
    
    def get_all_props(self):
        props = {}

        props_ColorAndStyle = self.get_color_and_style()
        props["ColorAndStyle"] = props_ColorAndStyle

        props_Markers = self.get_markers()
        props["Marker"] = props_Markers

        props_Legend = self.get_legend()
        props["Legend"] = props_Legend

        return props
    
    def resample(self, scale_factor):
        # 当x轴或y轴为log形式，不采样
        if self.ax.get_xscale() == "log" or self.ax.get_yscale() == "log":
            return
        aspect_ratio=mw_get_cax(self.ax).get_pixel_aspect()
        xdata, ydata = get_resample_data(self.originDataX, self.originDataY, scale_factor, aspect_ratio=aspect_ratio)
        if len(xdata) == len(self.originDataX) and len(ydata) == len(self.originDataY):
            self.unsample()
        else:
            self.sampled = True
            self.line.set_data(xdata, ydata)
            self.fig.canvas.draw_idle()
    
    def unsample(self):
        if self.sampled:
            self.line.set_data(self.originDataX, self.originDataY)
            self.sampled = False
            self.fig.canvas.draw_idle()

def mw_plot(ax, *args, **kwargs):
    normalize_kwargs = mw_normalize_kwargs('line', **kwargs)
    linewidth_kwargs = normalize_kwargs.pop('linewidth','')
    linewidth = 1 if linewidth_kwargs == '' else linewidth_kwargs
    if linewidth <= 0:
        return None

    markerfacecolor_kwargs = normalize_kwargs.pop('markerfacecolor','')
    markerfacecolor = 'none' if markerfacecolor_kwargs == '' else markerfacecolor_kwargs

    lines = ax.plot(*args, markerfacecolor = markerfacecolor, linewidth = linewidth, **normalize_kwargs)
    return lines