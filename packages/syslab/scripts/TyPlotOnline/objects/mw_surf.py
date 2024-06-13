"""
名称：stem
功能：此文件用于初始化针状图
实现：实现针状图的事件、槽函数、右键菜单等
接口：针状图类
依赖：
"""

from numbers import Number
# from PyQt5.QtWidgets import QMenu, QAction
# from PyQt5.QtGui import QCursor
from matplotlib import colors as mcolors
from matplotlib.collections import QuadMesh

from TyPlotOnline.objects.mw_interface import *
# from settings.mw_setting_base import CPropertySetting
from TyPlotOnline.objects.mw_axes import CAxes
from mpl_toolkits.mplot3d import proj3d

import numpy as np

class CSurf(object):
    """
    实现针状图的一些槽函数、右键菜单等

    Attributes:
        stem_container：包含基线、标记线、针状线
    """
    def __init__(self, poly_collection, **special_kwargs):
        self.init_attrs(poly_collection, **special_kwargs)
        self.init_customize(**special_kwargs)

    def init_attrs(self, poly_collection, **special_kwargs):
        self.poly_collection = poly_collection
        self.press = None
        self.select_points = []
        self.pick = False
        self.type = "surface"

        self.dict_style = {'实线' : ['-', 'solid'],
                            '虚线' : ['--', 'dashed'],
                            '点线' : [':', 'dotted'],
                            '点划线' : ['-.', 'dashdot'],
                            '无' : ['none', ' ', '', 'None']}

    def init_customize(self, **special_kwargs):
        self.replace_function()

        if 'facealpha' in special_kwargs:
            self.facealpha = special_kwargs['facealpha']
        else:
            self.facealpha = 1
        if 'edgealpha' in special_kwargs:
            self.edgealpha = special_kwargs['edgealpha']
        else:
            self.edgealpha = 1
        if 'linestyle' in special_kwargs:
            self.linestyle = special_kwargs['linestyle']
        else:
            self.linestyle = '-'

        if 'facecolor' in special_kwargs:
            self.facecolor = special_kwargs['facecolor']
        else:
            self.facecolor = self.poly_collection.get_facecolor()

        if 'edgecolor' in special_kwargs:
            self.edgecolor = special_kwargs['edgecolor']
        else:
            self.edgecolor = self.poly_collection.get_edgecolor()

        self.cmap = self.poly_collection.get_cmap()

        self.fig = self.poly_collection.get_figure()
        self.ax = self.poly_collection.axes
        self.poly_collection.set_facecolor(self.facecolor)
        self.poly_collection.set_edgecolor(self.edgecolor)

        self.connect()

    def before_export(self):
        self.poly_collection.set_facecolor = self.rep_dict["set_facecolor"]
        self.poly_collection.set_edgecolor = self.rep_dict["set_edgecolor"]
        self.poly_collection._set_mappable_flags = self.rep_dict["_set_mappable_flags"]
        self.poly_collection.update_scalarmappable = self.rep_dict["update_scalarmappable"]

    def after_export(self):
        self.replace_function()

    def after_import(self):
        self.replace_function()

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

    def replace_function(self):
        self.rep_dict = {}
        self.rep_dict["set_facecolor"] = self.poly_collection.set_facecolor
        self.rep_dict["set_edgecolor"] = self.poly_collection.set_edgecolor
        self.rep_dict["_set_mappable_flags"] = self.poly_collection._set_mappable_flags
        self.rep_dict["update_scalarmappable"] = self.poly_collection.update_scalarmappable
        
        self.poly_collection.set_facecolor = self.set_facecolor
        self.poly_collection.set_edgecolor = self.set_edgecolor
        self.poly_collection._set_mappable_flags = self._set_mappable_flags
        self.poly_collection.update_scalarmappable = self.update_scalarmappable

    def connect(self):
        # 暂时不适配mesh、surf等函数的交互功能
        return
        self.cidpress = self.data_line.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)

    def contains_self(self, event):
        # 暂时不适配mesh、surf等函数的交互功能
        return False, None
        contains, attrd = self.poly_collection.contains(event)
        if contains:
            return contains, attrd

        return False, None

    def on_press(self):
        # 暂时不适配mesh、surf等函数的交互功能
        return
        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

    def pick_self(self, pick_only = False):
        """曲线选中状态"""
        # 暂时不适配mesh、surf等函数的交互功能
        return
        #indexes = np.unique(self.poly_collection.get_paths()[0].vertices,axis=0)
        aa = self.poly_collection.get_paths()
        #print(indexes)
        b = aa[0].vertices[0]
        #print(aa[0].vertices[0])
        x = proj3d.proj_transform(b[0],b[1],0, self.ax.get_proj())
        #print(x)
        # x_data = indexes[:, 0]
        # y_data = indexes[:, 1]

        # pick_line = self.ax.plot(x_data,y_data,'s',clip_on = False,
        #     markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785',zorder = 2.1)
        # self.select_points.append(pick_line)

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
        # 暂时不适配mesh、surf等函数的交互功能
        return
        for point in self.select_points:
            point[0].remove()

        self.select_points.clear()
        self.pick = False

    def context_menu(self):
        return
        # context_menu = QMenu()

        # action_facecolor = context_menu.addAction('面颜色...')
        # action_edgecolor = context_menu.addAction('边颜色...')

        # menu_linestyle = context_menu.addMenu('线型')
        # linestyle = self.linestyle
        # for key, value in self.dict_style.items():
        #     action  = menu_linestyle.addAction(key)
        #     if linestyle in value:
        #         action.setCheckable(True)
        #         action.setChecked(True)
        #     action.triggered.connect(self.action_linestyle)

        # menu_linewidth = context_menu.addMenu('线宽')
        # lst_linewidth= ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        # lineswidth = self.poly_collection.get_linewidth()
        # for value in lst_linewidth:
        #     action = menu_linewidth.addAction(value)
        #     if lineswidth == float(value):
        #         action.setCheckable(True)
        #         action.setChecked(True)
        #     action.triggered.connect(self.action_linewidth)

        # context_menu.addSeparator()

        # action_prop = context_menu.addAction('打开属性检查器')

        # # 连接action槽函数
        # action_facecolor.triggered.connect(self.action_facecolor)
        # action_edgecolor.triggered.connect(self.action_edgecolor)
        # action_prop.triggered.connect(self.action_prop)

        # context_menu.exec_(QCursor().pos())

    def action_facecolor(self):
        color = self.poly_collection.get_facecolor()
        if len(color) > 0:
            current_color = float_tuple_to_color(color[0])
        else:
            current_color = 'none'
        dlg_color = DlgColor(current_color)
        if dlg_color.exec_() == QDialog.Accepted:
            self.poly_collection._face_is_mapped = False
            select_color = dlg_color.get_color()
            facecolor = mcolors.to_rgba(select_color.name(), self.facealpha)
            self.poly_collection.set_facecolor(facecolor)
            self.facecolor = facecolor
            update_legend(self.ax)

    def action_edgecolor(self):
        color = self.poly_collection.get_edgecolor()
        if len(color) > 0:
            current_color = float_tuple_to_color(color[0])
        else:
            current_color = 'none'
        dlg_color = DlgColor(current_color)
        if dlg_color.exec_() == QDialog.Accepted:
            self.poly_collection._edge_is_mapped = False
            select_color = dlg_color.get_color()
            if self.linestyle == 'none':
                edgecolor = mcolors.to_rgba(select_color.name(), 0.0)
            else:
                edgecolor = mcolors.to_rgba(select_color.name(), self.edgealpha)
            self.edgecolor = edgecolor
            self.poly_collection.set_edgecolor(edgecolor)
            update_legend(self.ax)

    #  曲线样式
    def action_linestyle(self):
        action = QAction()
        sender = action.sender()
        style = self.dict_style[sender.text()][0]
        if style == 'none':
            color = self.poly_collection.get_edgecolor()
            if len(color) > 0:
                current_color = float_tuple_to_color(color[0])
            else:
                current_color = 'none'
                return
            #current_color = color_to_qcolor(self.poly_collection.get_edgecolor()[0])
            edgecolor = mcolors.to_rgba(current_color.name(), 0.0)
            #self.poly_collection.set_edgecolor(edgecolor)
            for _poly_collection in [self.poly_collection]:
                _poly_collection._edgecolor3d = mcolors.to_rgba_array(
                    _poly_collection._edgecolor3d, 0)
        else:
            color = self.poly_collection.get_edgecolor()
            if len(color) > 0:
                current_color = float_tuple_to_color(color[0])
            else:
                current_color = 'none'
                return

            current_color = color_to_qcolor(self.poly_collection.get_edgecolor()[0])
            edgecolor = mcolors.to_rgba(current_color.name(), self.edgealpha)
            self.poly_collection.set_edgecolor(edgecolor)
            self.poly_collection.set_linestyle(style)

        self.linestyle = style
        self.fig.canvas.draw()
        update_legend(self.ax)

    # 曲线线宽
    def action_linewidth(self):
        action = QAction()
        sender = action.sender()
        linewidth = float(sender.text())
        self.poly_collection.set_linewidth(linewidth)
        update_legend(self.ax)

    # 属性面板
    def action_prop(self):
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.fig], [self.ax], [self.poly_collection]])
        prop_dlg.set_current_index(2)
        prop_dlg.connect()
        prop_dlg.exec_()

    def set_facecolor(self, c):
        c = arrayvalue_to_ndarray(c)
        self_color = c
        if c == 'flat':
            self.poly_collection._face_is_mapped = True
            color = self.poly_collection.to_rgba(self.poly_collection._A, self.facealpha)
        elif c == 'none':
            self.poly_collection._face_is_mapped = False
            color = [0, 0, 0, 0]
        elif len(c) > 1 and not isinstance(c[0], Number) and len(c[0]) > 1:
            self.poly_collection._face_is_mapped = True
            color = mcolors.to_rgba_array(c, self.facealpha)
            self_color = 'flat'
        elif c == []:
            raise ValueError("指定的facecolor无效")
        else:
            self.poly_collection._face_is_mapped = False
            color = mcolors.to_rgba_array(c, self.facealpha)
            

        if isinstance(color, str) and color.lower() in ("none", "face"):
            color = color.lower()
        self.poly_collection._original_facecolor = color
        self.poly_collection._set_facecolor(color)
        self.poly_collection._facecolor3d = PolyCollection.get_facecolor(self.poly_collection)
        self.facecolor = self_color

    def set_edgecolor(self, c):
        c = arrayvalue_to_ndarray(c)
        self_color = c
        if c == 'flat':
            self.poly_collection._edge_is_mapped = True
            color = self.poly_collection.to_rgba(self.poly_collection._A, self.edgealpha)
        elif c== 'none':
            self.poly_collection._edge_is_mapped = False
            color = [0, 0, 0, 0]
        elif len(c) > 1 and not isinstance(c[0], Number) and len(c[0]) > 1:
            self.poly_collection._edge_is_mapped = True
            color = mcolors.to_rgba_array(c, self.edgealpha)
            self_color = 'flat'
        elif c == []:
            raise ValueError("指定的edgecolor无效")
        else:
            self.poly_collection._edge_is_mapped = False
            color = mcolors.to_rgba_array(c, self.edgealpha)

        if isinstance(color, str) and color.lower() in ("none", "face"):
            color = color.lower()
        self.poly_collection._original_edgecolor = color
        self.poly_collection._set_edgecolor(color)
        self.poly_collection._edgecolor3d = PolyCollection.get_edgecolor(self.poly_collection)
        self.edgecolor = self_color

    def _set_mappable_flags(self):
        edge0 = self.poly_collection._edge_is_mapped
        face0 = self.poly_collection._face_is_mapped
        self.poly_collection._edge_is_mapped = False
        self.poly_collection._face_is_mapped = False

        if self.facecolor == 'flat':
            self.poly_collection._face_is_mapped = True
        else:
            self.poly_collection._face_is_mapped = False

        if self.edgecolor == 'flat':
            self.poly_collection._edge_is_mapped = True
        else:
            self.poly_collection._edge_is_mapped = False

        mapped = self.poly_collection._face_is_mapped or self.poly_collection._edge_is_mapped
        changed = (edge0 is None or face0 is None
                    or self.poly_collection._edge_is_mapped != edge0
                    or self.poly_collection._face_is_mapped != face0)

        return mapped or changed

    def update_scalarmappable(self):
        if not self.poly_collection._set_mappable_flags():
            return
        # Allow possibility to call 'self.set_array(None)'.
        if self.poly_collection._A is not None:
            # QuadMesh can map 2d arrays (but pcolormesh supplies 1d array)
            if self.poly_collection._A.ndim > 1 and not isinstance(self.poly_collection, QuadMesh):
                raise ValueError('Collections can only map rank 1 arrays')
            if np.iterable(self.poly_collection._alpha):
                if self.poly_collection._alpha.size != self.poly_collection._A.size:
                    raise ValueError(
                        f'Data array shape, {self.poly_collection._A.shape} '
                        'is incompatible with alpha array shape, '
                        f'{self.poly_collection._alpha.shape}. '
                        'This can occur with the deprecated '
                        'behavior of the "flat" shading option, '
                        'in which a row and/or column of the data '
                        'array is dropped.')
                # pcolormesh, scatter, maybe others flatten their _A
                self.poly_collection._alpha = self.poly_collection._alpha.reshape(self.poly_collection._A.shape)
            self.poly_collection._mapped_colors = self.poly_collection.to_rgba(self.poly_collection._A, self.poly_collection._alpha)

        if self.facecolor != 'none':
            if self.poly_collection._face_is_mapped:
                facecolor = self.poly_collection.to_rgba(self.poly_collection._A, self.facealpha)
                self.poly_collection._facecolors = facecolor
            else:
                self.poly_collection._facecolors = mcolors.to_rgba_array(self.poly_collection._original_facecolor, self.facealpha)

        if self.edgecolor != 'none':
            if self.poly_collection._edge_is_mapped:
                edgecolor = self.poly_collection.to_rgba(self.poly_collection._A, self.edgealpha)
                self.poly_collection._edgecolors = edgecolor
            else:
                self.poly_collection._edgecolors = mcolors.to_rgba_array(self.poly_collection._original_edgecolor, self.edgealpha)
        self.stale = True

    def set_facealpha(self, alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha values should be within 0-1 range")
        if self.facecolor != 'none':
            self.poly_collection._face_is_mapped = False
            self.poly_collection._facecolor3d = mcolors.to_rgba_array(
                self.poly_collection._facecolor3d, alpha)
            self.poly_collection._facecolors = mcolors.to_rgba_array(
                self.poly_collection._facecolors, alpha)
            self.poly_collection.stale = True
        self.facealpha = alpha

    def set_edgealpha(self, alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha values should be within 0-1 range")
        self.edgealpha = alpha
        if self.edgecolor != 'none' and self.linestyle not in ['none', '']:
            self.poly_collection._edgecolor3d = mcolors.to_rgba_array(
                self.poly_collection._edgecolor3d, self.edgealpha)
        

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.ax).surfs.remove(self)

        self.poly_collection.remove()
