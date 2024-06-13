"""
名称：scatter
功能：此文件用于初始化散点图
实现：实现散点图的事件、槽函数、右键菜单等
接口：散点图类
依赖：
"""
from numbers import Number
import numpy
# from PyQt5.QtWidgets import QMenu,QAction
# from PyQt5.QtGui import QCursor
from mpl_toolkits.mplot3d.art3d import Path3DCollection,_zalpha
import mpl_toolkits.mplot3d.proj3d as proj3d
from matplotlib import colors as mcolors
from matplotlib.offsetbox import AuxTransformBox
from matplotlib.collections import QuadMesh
from mpl_toolkits.mplot3d.art3d import Line3D

import matplotlib.markers as mmarkers

from TyPlotOnline.objects.mw_interface import *
import TyPlotOnline.settings.mw_setting_scatter as sc_setting
# from settings.mw_setting_base import CPropertySetting

import numpy as np

class CScatter(object):
    """
    实现散点图的一些槽函数、右键菜单等

    Attributes:
    """
    def __init__(self, path_collection, **special_kwargs):
        self.init_attrs(path_collection, **special_kwargs)
        self.init_customize(**special_kwargs)

    def init_attrs(self, path_collection, **special_kwargs):
        self.path_collection = path_collection

        # self.marker = special_kwargs['marker']
        self.marker = "o"

        self.press = None
        self.select_points = []
        self.pick = False
        self.pick_line = None

        self.originDataX = None
        self.originDataY = None
        self.sampled = False

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

    def init_customize(self, **special_kwargs):
        self.replace_fcnction()

        if 'facealpha' in special_kwargs:
            self.facealpha = special_kwargs['facealpha']
        else:
            facecolor = self.path_collection.get_facecolor()
            self.facealpha = facecolor[0][3]
        if 'edgealpha' in special_kwargs:
            self.edgealpha = special_kwargs['edgealpha']
        else:
            edgecolor = self.path_collection.get_edgecolor()
            self.edgealpha = edgecolor[0][3]
        if 'linestyle' in special_kwargs:
            self.linestyle = special_kwargs['linestyle']
        else:
            self.linestyle = '-'

        if 'markerfacecolor' in special_kwargs:
            self.facecolor = special_kwargs['markerfacecolor']
        else:
            self.facecolor = "flat"
        if 'markeredgecolor' in special_kwargs:
            self.edgecolor = special_kwargs['markeredgecolor']
        else:
            self.edgecolor = "flat"

        self.path_collection.set_edgecolor(self.edgecolor)
        self.path_collection.set_facecolor(self.facecolor)

        self.path_collection._alpha = None
        self.cmap = self.path_collection.get_cmap()
        self.is_3D = isinstance(self.path_collection,Path3DCollection)
        self.fig = self.path_collection.get_figure()
        self.ax = self.path_collection.axes
        self.box = AuxTransformBox(self.ax.figure.get_transform())

        # self.connect()
        self.init_origin_data()

    def init_origin_data(self):
        if '_offsets3d' in self.path_collection.__dict__:
            _offsets3d = self.path_collection.__dict__['_offsets3d']
            self.originDataX = _offsets3d[0]
            self.originDataY = _offsets3d[1]
        else:
            offsets = self.path_collection.get_offsets().data
            self.originDataX = offsets[:, 0]
            self.originDataY = offsets[:, 1]

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

    def replace_fcnction(self):
        self.path_collection.set_facecolor = self.set_facecolor
        self.path_collection.set_edgecolor = self.set_edgecolor
        self.path_collection._set_mappable_flags = self._set_mappable_flags
        self.path_collection.update_scalarmappable = self.update_scalarmappable

    def set_zorder(self,zorder):
        self.path_collection.zorder = zorder
        self.fig.canvas.draw_idle()

    def get_zorder(self):
        return self.path_collection.zorder

    def get_firstindex(self):
        return self.ax._children.index(self.path_collection)

    def get_lastindex(self):
        return self.ax._children.index(self.path_collection)

    def connect(self):
        pass
        # self.cidpress = self.data_line.figure.canvas.mpl_connect(
        #     'button_press_event', self.on_press)

    def contains_self(self, event):
        contains, attrd = self.path_collection.contains(event)
        if contains:
            return True

        return False

    def on_press(self):
        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

            cfig = mw_get_cfig(self.fig)
            if "Scatter" in cfig.prop_objs and cfig.prop_objs["Scatter"] == self:
                self.fig.canvas.send_event("property_change", current_prop="Scatter")
            else:
                cax = mw_get_cax(self.ax)
                props = get_property(cfig, cax, self, "Scatter")
                self.fig.canvas.send_event("property_init", props=props, current_prop="Scatter", font_list = get_font_lst())

    def pick_self(self, pick_only = False):
        """曲线选中状态"""
        line_xdata,line_ydata,line_zdata = self.get_external_cube()

        #plt.pause(1)

        if self.is_3D:
            pick_line = Line3D(line_xdata,line_ydata,line_zdata, marker = 's',clip_on = True,linestyle='none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)
            pick_line.set_transform(self.ax.transData)
            pick_line.set_clip_box(self.ax.bbox)
            self.fig.add_artist(pick_line)
            pick_line.axes = self.ax
        else:
            pick_line = Line2D(line_xdata,line_ydata,marker = 's',clip_on = True, linestyle='none',
                markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)
            pick_line.set_transform(self.ax.transData)
            pick_line.set_clip_box(self.ax.bbox)
            self.fig.add_artist(pick_line)
            pick_line.axes = self.ax

        self.select_points.append(pick_line)

        self.pick = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def get_index(self, arr, numElems = 16):
        '''获取选中点下标序列'''
        if len(arr) <= 16:
            return np.arange(len(arr))
        else:
            return np.round(np.linspace(0, len(arr) - 1, numElems)).astype(int)

    def dis_pick_self(self):
        """取消选中状态"""
        if self.is_3D:
            for point in self.select_points:
                point.remove()
        else:
            for point in self.select_points:
                point.remove()

        self.select_points.clear()
        self.pick = False

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
        # markerfacecolor

        # markeredgecolor

        # marker
        lst_marker_dict = []
        marker = self.marker
        for key, value in self.dict_marker.items():
            lst_marker_dict.append({"label": key, "value": value[0]})
            if marker in value:
                marker = value[0]
        menu_list.append({"value": "Marker", "label": "标记", "children": lst_marker_dict, "default_value":marker})

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

        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

    def action_markerfacecolor(self):
        if self.is_3D:
            color = self.path_collection._facecolors
        else:
            color = self.path_collection.get_facecolor()
        if len(color) > 0:
            current_color = float_tuple_to_color(color[0])
        else:
            current_color = 'none'
        #current_color = color_to_qcolor(self.facecolor)
        dlg_color = DlgColor(current_color)
        if dlg_color.exec_() == QDialog.Accepted:
            self.path_collection._face_is_mapped = False
            select_color = dlg_color.get_color()
            if self.is_3D:
                self.path_collection.set_facecolor(mcolors.to_rgba_array(select_color.name(),self.facealpha))
                self.facecolor = self.path_collection._facecolors[0]
            else:
                self.path_collection.set_facecolor(select_color.name())
                self.facecolor = mcolors.to_rgba(select_color.name(), self.facealpha)
            update_legend(self.ax)

    def action_markeredgecolor(self):
        if self.is_3D:
            color = self.path_collection._edgecolors
        else:
            color = self.path_collection.get_edgecolor()
        if len(color) > 0:
            current_color = float_tuple_to_color(color[0])
        else:
            current_color = 'none'
        #current_color = color_to_qcolor(self.edgecolor)
        dlg_color = DlgColor(current_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color()
            self.path_collection._edge_is_mapped = False
            if self.is_3D:
                self.path_collection.set_edgecolor(mcolors.to_rgba_array(select_color.name(),self.edgealpha))
                self.edgecolor = self.path_collection._edgecolors[0]
            else:
                self.path_collection.set_edgecolor(select_color.name())
                self.edgecolor = mcolors.to_rgba(select_color.name(), self.edgealpha)
            update_legend(self.ax)

    # marker
    def set_marker(self, marker):
        self.marker = marker
        if isinstance(marker, mmarkers.MarkerStyle):
            marker_obj = marker
        else:
            marker_obj = mmarkers.MarkerStyle(marker)
        path = marker_obj.get_path().transformed(
            marker_obj.get_transform())
        self.path_collection.set_paths((path,))

        update_legend(self.ax)

    # 属性面板
    def action_prop(self):
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.ax], [self.path_collection]])
        prop_dlg.set_current_index(2)
        prop_dlg.connect()
        prop_dlg.exec_()

    # 更新self.facecolor和self.edgecolor
    def update_facecolor_and_edgecolor(self, update_alpha = False):
        update_facecolor_and_edgecolor(self, update_alpha)

    #替换art3d中Path3DCollection类中的do_3d_projection函数
    def do_3d_projection_to_replace(self, renderer):
        # 由于在源码中,facecolor和edgecolor共用一个透明度(self._alpha),故在此处替换掉_update_scalarmappable函数的作用
        #_update_scalarmappable(self.path_collection)
        # if self.path_collection._A is not None:
        #     copy_state = self.path_collection._update_dict['array']
        #     if self.path_collection._A.ndim > 1 and not isinstance(self.path_collection, QuadMesh):
        #         raise ValueError('Collections can only map rank 1 arrays')
        #     if self.path_collection._check_update("array"):
        #         if self.path_collection._is_filled and self.facecolor == "flat":
        #             self.path_collection._facecolors = self.path_collection.to_rgba(self.path_collection._A, self.facealpha)
        #         elif self.path_collection._is_stroked and self.edgecolor == "flat":
        #             self.path_collection._edgecolors = self.path_collection.to_rgba(self.path_collection._A, self.edgealpha)
        #         self.stale = True
        #     if copy_state:
        #         if self.path_collection._is_filled and self.facecolor == "flat":
        #             self.path_collection._facecolor3d = self.path_collection._facecolors
        #         elif self.path_collection._is_stroked and self.edgecolor == "flat":
        #             self.path_collection._edgecolors = self.path_collection._edgecolors

        xs, ys, zs = self.path_collection._offsets3d
        vxs, vys, vzs, vis = proj3d.proj_transform_clip(xs, ys, zs, renderer.M)
        fcs = (_zalpha(self.path_collection._facecolors, vzs) if self.path_collection._depthshade else
               self.path_collection._facecolors)
        ecs = (_zalpha(self.path_collection._edgecolors, vzs) if self.path_collection._depthshade else
               self.path_collection._edgecolors)
        sizes = self.path_collection._sizes3d
        lws = self.path_collection._linewidth3d

        # Sort the points based on z coordinates
        # Performance optimization: Create a sorted index array and reorder
        # points and point properties according to the index array
        z_markers_idx = np.argsort(vzs)[::-1]

        # Re-order items
        vzs = vzs[z_markers_idx]
        vxs = vxs[z_markers_idx]
        vys = vys[z_markers_idx]
        if len(fcs) > 1 and isinstance(fcs,numpy.ndarray):
            fcs = fcs[z_markers_idx]
        if len(ecs) > 1 and isinstance(ecs,numpy.ndarray):
            ecs = ecs[z_markers_idx]
        if len(sizes) > 1:
            sizes = sizes[z_markers_idx]
        if len(lws) > 1:
            lws = lws[z_markers_idx]
        vps = np.column_stack((vxs, vys))

        fcs = mcolors.to_rgba_array(fcs, self.path_collection._alpha)
        ecs = mcolors.to_rgba_array(ecs, self.path_collection._alpha)

        self.path_collection.set_edgecolors(ecs)
        self.path_collection.set_facecolors(fcs)
        self.path_collection.set_sizes(sizes)
        self.path_collection.set_linewidth(lws)

        PathCollection.set_offsets(self.path_collection, vps)

        return np.min(vzs) if vzs.size else np.nan

    def get_external_cube(self):
        if self.is_3D:
            bbox=self.ax.xy_dataLim
            (minx,miny,maxx,maxy)=bbox.x0,bbox.y0,bbox.x1,bbox.y1
            bbox=self.ax.zz_dataLim
            (minz,maxz)=min(bbox.x0,bbox.y0),max(bbox.x1,bbox.y1)

            points=[
                [minx,miny,minz],
                [minx,miny,maxz],
                [minx,maxy,minz],
                [minx,maxy,maxz],
                [maxx,miny,minz],
                [maxx,miny,maxz],
                [maxx,maxy,minz],
                [maxx,maxy,maxz],
            ]

            x_data = [point[0] for point in points]
            y_data = [point[1] for point in points]
            z_data = [point[2] for point in points]
        else:
            points = self.path_collection.get_datalim(self.ax.transData).get_points()
            x0 = points[0,0]
            y0 = points[0,1]
            x1 = points[1,0]
            y1 = points[1,1]
            x_data = []
            y_data = []
            z_data = []
            x_data.append(x0)
            y_data.append(y0)

            x_data.append(x0)
            y_data.append(y1)

            x_data.append(x1)
            y_data.append(y0)

            x_data.append(x1)
            y_data.append(y1)

        return x_data,y_data,z_data

    def set_facecolor(self, c):
        c = arrayvalue_to_ndarray(c)
        self_color = c
        if c == 'flat':
            if self.path_collection._A is None:
                color = mcolors.to_rgba_array(self.path_collection._facecolors, self.facealpha)
            else:
                color = self.path_collection.to_rgba(
                    self.path_collection._A, self.facealpha)
        elif c == 'none':
            self.path_collection._face_is_mapped = False
            color = [0, 0, 0, 0]
        elif len(c) > 1 and not isinstance(c[0], Number) and len(c[0]) > 1:
            self.path_collection._face_is_mapped = True
            color = mcolors.to_rgba_array(c, self.facealpha)
            self_color = 'flat'
        else:
            self.path_collection._face_is_mapped = False
            color = mcolors.to_rgba_array(c, self.facealpha)

        if isinstance(color, str) and color.lower() in ("none", "face"):
            color = color.lower()
        self.path_collection._original_facecolor = color
        self.path_collection._set_facecolor(color)
        self.path_collection._facecolor3d = PolyCollection.get_facecolor(self.path_collection)
        self.facecolor = self_color

    def set_edgecolor(self, c):
        c = arrayvalue_to_ndarray(c)
        self_color = c
        if c == 'flat':
            if self.path_collection._A is None:
                if self.path_collection._edgecolors == 'face':
                    egdecolor = self.path_collection._facecolors
                else:
                    egdecolor = self.path_collection._edgecolors
                color = mcolors.to_rgba_array(egdecolor, self.edgealpha)
            else:
                color = self.path_collection.to_rgba(
                    self.path_collection._A, self.edgealpha)
        elif c == 'none':
            self.path_collection._edge_is_mapped = False
            color = [0, 0, 0, 0]
        elif len(c) > 1 and not isinstance(c[0], Number) and len(c[0]) > 1:
            self.path_collection._edge_is_mapped = True
            color = mcolors.to_rgba_array(c, self.edgealpha)
            self_color = 'flat'
        else:
            self.path_collection._edge_is_mapped = False
            color = mcolors.to_rgba_array(c, self.edgealpha)

        if isinstance(color, str) and color.lower() in ("none", "face"):
            color = color.lower()
        self.path_collection._original_edgecolor = color
        self.path_collection._set_edgecolor(color)
        self.path_collection._edgecolor3d = PolyCollection.get_edgecolor(self.path_collection)
        self.edgecolor = self_color

    def _set_mappable_flags(self):
        edge0 = self.path_collection._edge_is_mapped
        face0 = self.path_collection._face_is_mapped
        self.path_collection._edge_is_mapped = False
        self.path_collection._face_is_mapped = False

        if self.path_collection._A is not None:
            if self.facecolor == 'flat':
                self.path_collection._face_is_mapped = True
            else:
                self.path_collection._face_is_mapped = False

            if self.edgecolor == 'flat':
                self.path_collection._edge_is_mapped = True
            else:
                self.path_collection._edge_is_mapped = False

        mapped = self.path_collection._face_is_mapped or self.path_collection._edge_is_mapped
        changed = (edge0 is None or face0 is None
                    or self.path_collection._edge_is_mapped != edge0
                    or self.path_collection._face_is_mapped != face0)

        return mapped or changed

    def update_scalarmappable(self):
        if not self.path_collection._set_mappable_flags():
            return
        # Allow possibility to call 'self.set_array(None)'.
        if self.path_collection._A is not None:
            # QuadMesh can map 2d arrays (but pcolormesh supplies 1d array)
            if self.path_collection._A.ndim > 1 and not isinstance(self.path_collection, QuadMesh):
                raise ValueError('Collections can only map rank 1 arrays')
            if np.iterable(self.path_collection._alpha):
                if self.path_collection._alpha.size != self.path_collection._A.size:
                    raise ValueError(
                        f'Data array shape, {self.path_collection._A.shape} '
                        'is incompatible with alpha array shape, '
                        f'{self.path_collection._alpha.shape}. '
                        'This can occur with the deprecated '
                        'behavior of the "flat" shading option, '
                        'in which a row and/or column of the data '
                        'array is dropped.')
                # pcolormesh, scatter, maybe others flatten their _A
                self.path_collection._alpha = self.path_collection._alpha.reshape(self.path_collection._A.shape)
            self.path_collection._mapped_colors = self.path_collection.to_rgba(self.path_collection._A, self.path_collection._alpha)

        if self.facecolor != 'none':
            if self.path_collection._face_is_mapped:
                facecolor = self.path_collection.to_rgba(self.path_collection._A, self.facealpha)
                self.path_collection._facecolors = facecolor
            else:
                self.path_collection._facecolors = mcolors.to_rgba_array(self.path_collection._original_facecolor, self.facealpha)

        if self.edgecolor != 'none':
            if self.path_collection._edge_is_mapped:
                edgecolor = self.path_collection.to_rgba(self.path_collection._A, self.edgealpha)
                self.path_collection._edgecolors = edgecolor
            else:
                self.path_collection._edgecolors = mcolors.to_rgba_array(self.path_collection._original_edgecolor, self.edgealpha)
        self.stale = True

    def set_facealpha(self, alpha):
        self.facealpha = alpha
        if self.facecolor != 'none':
            self.path_collection.set_facecolor(mcolors.to_rgba_array(self.path_collection._facecolors, alpha))
        self.path_collection.stale = True

    def set_edgealpha(self, alpha):
        self.edgealpha = alpha
        if self.edgecolor != 'none':
            self.path_collection.set_edgecolor(mcolors.to_rgba_array(self.path_collection._edgecolors, alpha))
        self.path_collection.stale = True

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.ax).scatters.remove(self)
        self.path_collection.remove()

    def set_prop(self, name, value):
        name = name.lower()
        # 标记
        if name == "marker":
            sc_setting.set_marker(self.path_collection, value)
            update_legend(self.ax)
        elif name == "linewidth":
            sc_setting.set_linewidth(self.path_collection, value)
            update_legend(self.ax)
        elif name == "markerfacecolor":
            sc_setting.set_markerfacecolor(self.path_collection, value)
            update_legend(self.ax)
        elif name == "markeredgecolor":
            sc_setting.set_markeredgecolor(self.path_collection, value)
            update_legend(self.ax)
        # 透明度
        elif name == "markerfacealpha":
            sc_setting.set_markerfacealpha(self.path_collection, value)
            update_legend(self.ax)
        elif name == "markeredgealpha":
            sc_setting.set_markeredgealpha(self.path_collection, value)
            update_legend(self.ax)
        # 颜色和大小数据
        elif name == "sizedata":
            sc_setting.set_sizedata(self.path_collection, value)
            update_legend(self.ax)
        # 图例
        elif name == "markeredgealpha":
            sc_setting.set_displayname(self.path_collection, value)
            update_legend(self.ax)
        elif name == "legend":
            sc_setting.set_displayname(self.path_collection,value)
            update_legend(self.ax)
        elif name == "prop":
            # 属性面板
            pass
        elif name == "top_level":
            # 置于顶层
            if value == "level_top":
                mw_get_cax().set_level_top(self)
            # 上移一层
            elif value == "level_up":
                mw_get_cax().set_level_up(self)
        elif name == "bottom_level":
            # 置于底层
            if value == "level_bottom":
                mw_get_cax().set_level_bottom(self)
            # 下移一层
            elif value == "level_down":
                mw_get_cax().set_level_down(self)


        if name in ["marker"]:
            self.fig.canvas.send_event("property_update", key="Scatter", child_key = "Markers", value = self.get_markers())

    def get_markers(self):
        props_Markers = {}
        props_Markers["Marker"] = self.marker
        props_Markers["LineWidth"] = sc_setting.get_linewidth(self.path_collection)
        props_Markers["MarkerEdgeColor"] = color_to_hex(sc_setting.get_markeredgecolor(self.path_collection))
        props_Markers["MarkerFaceColor"] = color_to_hex(sc_setting.get_markerfacecolor(self.path_collection))

        return props_Markers

    def get_alpha(self):
        props_Alpha = {}
        props_Alpha["MarkerFaceAlpha"] = float(sc_setting.get_markerfacealpha(self.path_collection))
        props_Alpha["MarkerEdgeAlpha"] = float(sc_setting.get_markeredgealpha(self.path_collection))

        return props_Alpha
    
    def get_color_sizedata(self):
        props_Color_SizeData = {}
        props_Color_SizeData["SizeData"] = str(sc_setting.get_sizedata(self.path_collection))
        return props_Color_SizeData

    def get_legend(self):
        props_Legend = {}
        props_Legend["DisplayName"] = sc_setting.get_displayname(self.path_collection)
        return props_Legend
        
    def get_all_props(self):
        props = {}

        props_Markers = self.get_markers()
        props["Markers"] = props_Markers

        props_Alpha = self.get_alpha()
        props["Alpha"] = props_Alpha

        props_Color_SizeData = self.get_color_sizedata()
        props["Color_SizeData"] = props_Color_SizeData

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
            offsets = np.column_stack((xdata,ydata))
            self.path_collection.set_offsets(offsets)
            self.fig.canvas.draw_idle()

    def unsample(self):
        if self.sampled:
            offsets = np.column_stack((self.originDataX, self.originDataY))
            self.path_collection.set_offsets(offsets)
            self.sampled = False
            self.fig.canvas.draw_idle()
        
#更新CScatter中的facecolor和edgecolor
def update_facecolor_and_edgecolor(CScatter, update_alpha = False):
    #使用np.ndarray形式的四元向量作为颜色数据
        if CScatter.is_3D:
            facecolor = CScatter.path_collection._facecolors
        else:
            facecolor = CScatter.path_collection._facecolors

        if len(facecolor) > 1 and isinstance(facecolor,numpy.ndarray):
            CScatter.facecolor = 'flat'
            # if update_alpha:
            #     CScatter.facealpha = CScatter.path_collection.get_alpha()
        else:
            if len(facecolor) == 0:
                CScatter.facecolor = 'none'
            else:
                CScatter.facecolor = facecolor[0]
                if isinstance(CScatter.facecolor, str):
                    CScatter.facecolor = mcolors.to_rgba(CScatter.facecolor)
                    CScatter.facealpha = 1.0
                else:
                    if len(CScatter.facecolor) == 3:
                        CScatter.facealpha = 1.0
                    elif CScatter.facecolor[3] == 0:
                        CScatter.facecolor = 'none'
                        CScatter.facealpha = 1.0
                    elif update_alpha:
                        CScatter.facealpha = CScatter.facecolor[3]

        if CScatter.is_3D:
            edgecolor = CScatter.path_collection._edgecolors
        else:
            edgecolor = CScatter.path_collection._edgecolors

        if len(edgecolor) > 1 and isinstance(edgecolor,numpy.ndarray):
            CScatter.edgecolor = 'flat'
            # if update_alpha:
            #     CScatter.edgealpha = CScatter.path_collection.get_alpha()
        else:
            if len(edgecolor) == 0:
                CScatter.edgecolor = 'none'
            else:
                CScatter.edgecolor = edgecolor[0]
                if isinstance(CScatter.edgecolor, str):
                    CScatter.edgecolor = mcolors.to_rgba(CScatter.edgecolor)
                    CScatter.edgealpha = 1.0
                else:
                    if len(CScatter.edgecolor) == 3:
                        CScatter.edgealpha = 1.0
                    elif CScatter.edgecolor[3] == 0:
                        CScatter.edgecolor = 'none'
                        CScatter.edgealpha = 1.0
                    elif update_alpha:
                        CScatter.edgealpha = CScatter.edgecolor[3]

        CScatter.path_collection._alpha = None
        # if self.bars[0].get_facecolor()[3] == 0:
        #     self.facecolor = 'none'
        # else:
        #     self.facecolor = self.bars[0].get_facecolor()
        #     self.facealpha = self.bars[0].get_facecolor()[3]

        # if self.bars[0].get_edgecolor()[3] == 0:
        #     self.edgecolor = 'none'
        # else:
        #     self.edgecolor = self.bars[0].get_edgecolor()
        #     self.edgealpha = self.bars[0].get_edgecolor()[3]

def mw_scatter(ax, x, y, s = None, c = None, label = None, **kwargs):
    normalize_kwargs = mw_normalize_kwargs('surf', **kwargs)

    is_filled = False
    if 'filled' in kwargs:
        is_filled = kwargs.pop('filled')
    # special_kwargs['filled'] = is_filled

    if is_filled and 'markerfacecolor' not in normalize_kwargs:
        normalize_kwargs['markerfacecolor'] = 'flat'
    elif 'markerfacecolor' not in normalize_kwargs:
        normalize_kwargs['markerfacecolor'] = 'none'

    if is_filled and 'markeredgecolor' not in normalize_kwargs:
        normalize_kwargs['markeredgecolor'] = 'none'
    elif 'markeredgecolor' not in normalize_kwargs:
        normalize_kwargs['markeredgecolor'] = 'flat'

    if 'linewidths' not in normalize_kwargs:
        normalize_kwargs['linewidths'] = 0.5

    if normalize_kwargs['linewidths'] < 0:
        return 'linewidths'

    special_kwargs, kwargs = pop_special_kwargs(['markerfacecolor', 'markeredgecolor'], **normalize_kwargs)

    if special_kwargs['facealpha'] < 0:
        return 'facealpha'
    if special_kwargs['edgealpha'] < 0:
        return 'edgealpha'

    if 'markeredgecolor' not in special_kwargs:
        special_kwargs['markeredgecolor'] = 'flat'

    if 'facecolor' in kwargs:
        kwargs.pop('facecolor','')
    if 'facecolors' in kwargs:
        kwargs.pop('facecolors','')
    if 'markerfacecolor' in kwargs:
        kwargs.pop('markerfacecolor','')

    if 'edgecolor' in kwargs:
        kwargs.pop('edgecolor','')
    if 'edgecolors' in kwargs:
        kwargs.pop('edgecolors','')
    if 'markeredgecolor' in kwargs:
        kwargs.pop('markeredgecolor','')

    if 'marker' in kwargs:
        special_kwargs['marker'] = kwargs['marker']
    else:
        special_kwargs['marker'] = 'o'

    if 'filled' in kwargs:
        kwargs.pop('filled')

    s = ax.scatter(x, y, s = s, c = c, **kwargs)
    s._face_is_mapped = False
    s._edge_is_mapped = True
    if 'markerfacecolor' in special_kwargs and special_kwargs['markerfacecolor'] == 'flat':
        s._face_is_mapped = True
    if 'markeredgecolor' in special_kwargs and special_kwargs['markeredgecolor'] != 'flat':
        s._edge_is_mapped = False

    if label == None:
        label = mw_get_unique_legend_name(ax, s)
    s.set_label(label)
    update_legend(ax)

    from TyPlotOnline.objects.mw_figure import mw_update_scatters
    fig = plt.gcf()
    mw_update_scatters(fig, [s], 'zorder' in kwargs,**special_kwargs)

    return s
