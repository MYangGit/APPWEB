"""
名称：title
功能：此文件用于初始化坐标轴标题
实现：将坐标轴的标题对象作为本类的成员，实现title的拖拽、右键菜单等交互
接口：标题类
依赖：mw_interface
"""
from TyPlotOnline.objects.mw_interface import *
from matplotlib.backend_bases import MouseButton
from matplotlib.text import _get_textbox
from matplotlib.transforms import Affine2D
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
# from matplotlib.text import _log

class CTextBase(object):
    """
    text基类

    Attributes:
        text : text对象
        type : text类型, {"title", "xlabel", "ylabel"}

    """
    def __init__(self, ax, text, type):
        self.type = type
        self.text = text
        if self.type == "text":
            self.text.set_animated(True)
        self.axes = ax
        self.figure = self.text.figure
        self.pick = False
        self.press = False
        self.block = False
        # if not CGlobalSetting.isOnline:
        #     self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)

        self.text.update_bbox_position_size = self.update_bbox_position_size
        if self.type == "text":
            self.connect()
        self.create_pick_state()

        if self.text._bbox_patch is None:
            self.text.set_bbox(dict(facecolor='none',edgecolor='none'))

        # self.draw_id = self.figure.canvas.mpl_connect(
        #     'resize_event', self.on_resize)

        self.dict_edge_style = {'实线' : ['-', 'solid'],
                            '虚线' : ['--', 'dashed'],
                            '点线' : [':', 'dotted'],
                            '点划线' : ['-.', 'dashdot'],
                            }

    def before_export(self):
        self.text.update_bbox_position_size = Text.update_bbox_position_size
        self.background = None

    def after_export(self):
        self.text.update_bbox_position_size = self.update_bbox_position_size
        if not CGlobalSetting.isOnline:
            self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)

    def connect(self):
        self.press_id = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.move_id = self.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_move)
        self.release_id = self.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.draw_id = self.figure.canvas.mpl_connect(
            'draw_event', self.on_draw)

    def on_pick(self):
        """
        选中对象
        """
        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            mw_clear_status()
            self.pick_self()

            # 点击切换属性面板
            cfig = mw_get_cfig(self.axes.figure)
            if "Text" in cfig.prop_objs and cfig.prop_objs["Text"] == self:
                self.axes.figure.canvas.send_event("property_change", current_prop="Text")
            else:
                    cax = mw_get_cax(self.axes.figure.gca())
                    props = get_property(cfig, cax, self, "Text")
                    self.axes.figure.canvas.send_event("property_init", props=props, current_prop="Text", font_list = get_font_lst())
            
    def context_menu(self):
        """右键菜单函数"""
        menu_list = []

        # 删除
        menu_list.append({"value": "text_delete", "label": "删除", "children": [], "default_value": ""})
        
        # 编辑文本
        # 接收当前文本作为默认值
        text = self.get_string()
        menu_list.append({"value": "text_edit", "label": "编辑文本内容", "children": [], "default_value": text})
       
        # 颜色
        # 接收当前颜色作为默认值
        color = self.get_color()
        menu_list.append({"value": "color", "label": "文本颜色", "children": [], "default_value": color})
      
        # 打开属性检查器
        menu_list.append({"value": "property", "label": "打开属性检查器", "children": [], "default_value": "Text"})
        
        self.axes.figure.canvas.send_event("contextmenu", menu_list=menu_list)

    def set_prop(self,name,value):
        """接受前端返回数据，并进行相应操作"""
        # name = name.lower()
        if name == "text_delete":
            # 删除
            self.delete_self()
        elif name == "text_edit":
            # 编辑文本 右键菜单
            self.set_string(value)
        elif name == "color":
            # 颜色
            self.set_color(value)
        elif name == "Color":
            # 颜色
            self.set_color(value)
        elif name == "BackgroundColor":
            # 背景颜色
            self.set_backgroundcolor(value)
        elif name == "EdgeColor":
            # 边颜色
            self.set_edgecolor(value)
        elif name == "LineWidth":
            # 线宽 
            self.set_linewidth(value)
        elif name == "LineStyle":
            # 线型
            self.set_linestyle(value)
        elif name == "String":
            # 属性管理器编辑文本
            self.set_string(value)
        elif name == "FontName":
            # 字体名称
            self.set_fontname(value)
        elif name == "FontAngle":
            # 字体角度
            if value:
                self.set_fontangle('italic')
            else:
                self.set_fontangle('normal')
        elif name == "FontWeight":
            # 字体粗细
            if value:
                self.set_fontweight('bold')
            else:
                self.set_fontweight('normal')
        elif name == "FontSize":
            # 字体大小
            self.set_fontsize(value)
        elif name == "Margin":
            try:
                value=float(value)
            except Exception as e:
                return
            # 外边距
            self.set_margin(value)
        elif name == "HorizontalAlignment":
            # 水平对齐
            self.set_horizontalalignment(value)
        elif name == "VerticalAlignment":
            # 竖直对齐
            self.set_verticalalignment(value)
        elif name == "Rotation":
            # 旋转角度
            self.set_rotation(value)
        elif name == "Position":
            # 文本坐标
            self.set_position(value)

    def get_string(self):
        """获取当前文本内容"""
        return self.text.get_text()
    
    def set_string(self,string):
        """设置当前文本内容"""
        self.text.set_text(string)
        self.axes.figure.canvas.draw_idle()

    def get_linestyle(self):
        """获取当前文本线型"""
        # self.text._bbox_patch.get_linestyle()为当前线型，不过为'solid'格式，需转换为'-'格式返回
        for key, value in self.dict_edge_style.items():
            if self.text._bbox_patch.get_linestyle() in value:
                return value[0]
        return None
    
    def set_linestyle(self,linestyle):
        """设置当前文本线型"""
        self.text._bbox_patch.set_linestyle(linestyle)
        self.axes.figure.canvas.draw_idle()

    def get_linewidth(self):
        """获取当前文本线宽"""
        return self.text._bbox_patch.get_linewidth()
    
    def set_linewidth(self,linewidth):
        """设置当前文本线宽"""
        self.text._bbox_patch.set_linewidth(linewidth)
        self.axes.figure.canvas.draw_idle()

    def get_fontsize(self):
        """获取当前文本字体大小"""
        return self.text.get_fontsize()
    
    def set_fontsize(self, fontsize):
        """设置当前文本字体大小"""
        fontdict={'size': fontsize}
        self.text.update(fontdict)
        self.axes.figure.canvas.draw_idle()

    def get_fontweight(self):
        """获取当前文本字体粗细"""
        return self.text.get_fontweight()
    
    def set_fontweight(self, fontweight):
        """设置当前文本字体粗细"""
        fontdict={'weight': fontweight}
        self.text.update(fontdict)
        self.axes.figure.canvas.draw_idle()

    def get_fontangle(self):
        """获取当前文本字体角度"""
        return self.text.get_fontstyle()
    
    def set_fontangle(self, fontangle):
        """设置当前文本字体角度"""
        fontdict={'style': fontangle}
        self.text.update(fontdict)
        self.axes.figure.canvas.draw_idle()

    def get_fontname(self):
        """获取当前文本字体名称"""
        return self.text.get_fontname()
    
    def set_fontname(self, fontname):
        """设置当前文本字体名称"""
        fontname = get_real_name(fontname)
        fontdict={'family': fontname}
        self.text.update(fontdict)
        self.axes.figure.canvas.draw_idle()

    def get_verticalalignment(self):
        """获取当前文本竖直对齐属性"""
        return self.text.get_verticalalignment()
    
    def set_verticalalignment(self, alignment):
        """设置当前文本竖直对齐属性"""
        if alignment not in ['baseline', 'bottom', 'top', 'cap', 'middle']:
            return

        if alignment == 'baseline' or alignment == 'bottom':
            text_va = 'bottom'
        elif alignment == 'top' or alignment == 'cap':
            text_va = 'top'
        else:
            text_va = 'center'

        self.text.set_verticalalignment(text_va)
        # self.calculate_text_position()

        self.axes.figure.canvas.draw_idle()

    def get_horizontalalignment(self):
        """获取当前文本水平对齐属性"""
        return self.text.get_horizontalalignment()
    
    def set_horizontalalignment(self, alignment):
        """设置当前文本水平对齐属性"""
        if alignment not in ['left', 'center', 'right']:
            return

        self.text.set_horizontalalignment(alignment)
        # self.calculate_text_position()

        self.axes.figure.canvas.draw_idle()

    def get_color(self):
        """获取当前文本文本颜色"""
        return mcolors.to_rgb(self.text.get_color())
    
    def set_color(self, color):
        """设置当前文本文本颜色"""
        self.text.set_color((color))
        self.axes.figure.canvas.draw_idle()

    def get_backgroundcolor(self):
        """获取当前文本背景颜色"""
        return mcolors.to_rgb(self.text._bbox_patch.get_facecolor())
    
    def set_backgroundcolor(self, color):
        """设置当前文本背景颜色"""
        self.text._bbox_patch.set_facecolor((color))
        self.axes.figure.canvas.draw_idle()

    def get_edgecolor(self):
        """获取当前文本边颜色"""
        return mcolors.to_rgb(self.text._bbox_patch.get_edgecolor())
    
    def set_edgecolor(self, color):
        """设置当前文本边颜色"""
        self.text._bbox_patch.set_edgecolor((color))
        self.axes.figure.canvas.draw_idle()

    def get_rotation(self):
        """获取当前文本角度"""
        return self.text.get_rotation()
    
    def set_rotation(self,rotation):
        """设置当前文本角度"""
        self.text.set_rotation(rotation)
        self.axes.figure.canvas.draw_idle()

    def get_position(self):
        """获取当前文本坐标"""
        # 实现了Units属性后，此函数可能需要进一步修改
        return self.text.get_position()
    
    def set_position(self,position):
        """设置当前文本坐标"""
        # 实现了Units属性后，此函数可能需要进一步修改
        self.text.set_position(position)
        self.axes.figure.canvas.draw_idle()

    def get_margin(self):
        """获取当前文本外边距"""
        # 参考CDTextArrow类的margin处理，与单机版效果基本一致
        return self.text.get_bbox_patch().get_boxstyle().pad
    
    def set_margin(self, text_margin):
        """获取当前文本外边距"""
        # 参考CDTextArrow类的margin处理，与单机版效果基本一致
        self.text.get_bbox_patch().set_boxstyle("square",pad=text_margin)
        self.axes.figure.canvas.draw_idle()

    def get_all_props(self):
        """获取所有属性"""
        props = {}

        # 分为四部分，文本、字体、文本框、位置
        # 文本
        props_text = {}
        #   文本内容
        props_text["String"] = self.get_string()
        #   文本颜色
        props_text["Color"] = color_to_hex(self.get_color())
        props["Text"] = props_text

        # 字体
        props_font = {}
        #   字体名称
        props_font["FontName"] = get_chinese_name(self.get_fontname())
        #   字体角度
        props_font["FontAngle"] = self.get_fontangle()
        if self.get_fontangle() == "italic":
            props_font["FontAngle"] = True
        else:
            props_font["FontAngle"] = False
        #   字体粗细
        if self.get_fontweight() == "bold":
            props_font["FontWeight"] = True
        else:
            props_font["FontWeight"] = False
        #   字体大小
        props_font["FontSize"] = self.get_fontsize()
        props["Fonts"] = props_font

        # 文本框
        props_textbox = {}
        #   旋转角度
        props_textbox["Rotation"] = self.get_rotation()
        #   边颜色
        props_textbox["EdgeColor"] = color_to_hex(self.get_edgecolor())
        #   背景颜色
        props_textbox["BackgroundColor"] = color_to_hex(self.get_backgroundcolor())
        #   线型
        props_textbox["LineStyle"] = self.get_linestyle()
        #   线宽
        props_textbox["LineWidth"] = self.get_linewidth()
        #   外边距
        props_textbox["Margin"] = self.get_margin()
        props["TextBox"] = props_textbox

         # 位置
        props_position = {}
        # 坐标
        props_position["Position"] = self.get_position()
        # 单位
        props_position["Units"] = ""
        # 水平对齐
        props_position["HorizontalAlignment"] = self.get_horizontalalignment()
        # 竖直对齐
        props_position["VerticalAlignment"] = self.get_verticalalignment()
        props["Position"] = props_position

        return props

    def on_press(self, event):
        if not mw_get_cfig().edit_mode:
            return

        if not self.pick:
            return

        if event.button is MouseButton.RIGHT:
            return

        if not self.contains_self(event):
            return

        self.press = True
        self.block = True
        self.pos_x = event.x
        self.pos_y = event.y
        self.start_pos = self.text.get_transform().transform(self.text.get_position())
        event.canvas.setCursor(Qt.SizeAllCursor)

    def on_move(self, event):
        if not self.pick:
            return

        if not self.press:
            self.motion_status(event)
        else:
            dx = event.x - self.pos_x
            dy = event.y - self.pos_y
            self.update_offset(dx, dy)

        self._update()

    def on_release(self, event):
        self.press = False
        self.block = False

    def update_offset(self, dx, dy):
        self.axes._autotitlepos = False
        self.axes.xaxis._autolabelpos = False
        self.text.set_position(self.text.get_transform().inverted().transform((self.start_pos[0] + dx, self.start_pos[1] + dy)))
        #self._update()

    def on_resize(self, event):
        self.set_pickbox_pos()

    def on_draw(self,event):
        '''用于动画效果'''
        self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)

        if self.background is not None:
            self.figure.canvas.restore_region(self.background)

        self.draw_self()

    def motion_status(self, event):
        # 判读每个点是否被选中，若被选中，切换相应鼠标状态
        contains = self.contains_self(event)
        if contains:
            event.canvas.setCursor(Qt.SizeAllCursor)
            return

        event.canvas.setCursor(Qt.ArrowCursor)

    def pick_self(self, pick_only = False):
        """选中状态"""
        self.pick_state.set_visible(True)
        self.pick = True

        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        self.pick_state.set_visible(False)
        self.pick = False

    def contains_self(self, event):
        if self.text.get_text() == '':
            return False

        contains_text, attrd = self.text.contains(event)
        contains_pick_state, attrd = self.pick_state.contains(event)
        return contains_text or contains_pick_state

    def action_delete(self):
        '''删除动作'''
        self.text.set_color('k')
        self.text.set_bbox(dict(facecolor='none',edgecolor='none'))
        mw_clear_status()
        mw_get_cax(self.figure.gca()).pick_self()
        self.change_pos_mode()

    def action_edit(self):
        '''编辑动作'''
        self.text_edit=DlgEditGraphicsText(self,self.text)
        # self.text_edit.text_layout.TextChanged.connect(self.set_pickbox_pos)
        # self.text_edit.text_layout.TextDelete.connect(self.action_delete)
        self.text_edit.exec()

    def action_font_color(self):
        '''字体颜色设置动作'''
        init_color=color_to_qcolor(self.text.get_color())
        dlg_color = DlgColor(init_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color()
            self.text.set_color(select_color.name())
        self.text.stale = True
        self.text.figure.canvas.draw()

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

        self.text.stale = True
        self.text.figure.canvas.draw()

    def action_edge_color(self):
        '''字体边框颜色设置动作'''
        edge_color='none'
        if not self.text._bbox_patch is None:
            tuple_edge_color = self.text._bbox_patch.get_edgecolor()
            edge_color = color_to_qcolor(tuple_edge_color)
            if tuple_edge_color[3]==0.0:
                edge_color='none'
        dlg_color = DlgColor(edge_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            if self.text._bbox_patch is None:
                self.text.set_bbox(dict(facecolor='none', edgecolor=select_color))
            else:
                self.text._bbox_patch.update(dict(edgecolor=select_color))
            self.text._update_clip_properties()

        self.text.stale = True
        self.text.figure.canvas.draw()

    def action_font(self):
        '''设置字体动作'''
        self.font=DlgTitlebaseFont(self,self.text)
        self.font.font_layout.FontSizeChanged.connect(self.set_pickbox_pos)
        self.font.exec()

    def action_edgestyle(self):
        '''边框样式'''
        action = QAction()
        sender = action.sender()
        style = self.dict_edge_style[sender.text()][0]
        self.text._bbox_patch.set_linestyle(style)
        self.figure.canvas.draw()

    def action_edgewidth(self):
        '''边框宽度'''
        action = QAction()
        sender = action.sender()
        linewidth = float(sender.text())
        self.text._bbox_patch.set_linewidth(linewidth)
        self.figure.canvas.draw()

    def action_prop(self):
        '''打开属性面板'''
        from TyPlotOnline.settings.mw_setting_base import CPropertySetting
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.figure], [self.axes], [self.text]])
        prop_dlg.set_current_index(2)
        prop_dlg.connect()
        prop_dlg.exec_()

    def draw_self(self):
        self.axes.draw_artist(self.text)
        self.figure.draw_artist(self.pick_state)

    def _update(self):
        '''用于动画效果'''
        if not self.pick:
            return

        update_all(self.figure)

    def create_pick_state(self):
        '''
        初始化选中状态边框
        '''
        self.picker_point = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        picker_point_x, picker_point_y=[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]
        self.pick_state = Line2D(picker_point_x, picker_point_y, marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785')

        if self.type == "text":
            self.pick_state.set_animated(True)
        self.pick_state.set_in_layout(False)
        self.pick_state.set_transform(self.figure.get_transform())
        self.pick_state.set_zorder(10)
        self.figure.add_artist(self.pick_state)

        self.set_pickbox_pos()

    def set_pickbox_pos(self,event=None):
        '''计算边框中六个点的位置'''
        if self.text.get_text() == '':
            self.dis_pick_self()
            self.pickable=False
            return

        #self.text.draw(self.text._renderer)
        bbox = self.text.get_bbox_patch()
        if bbox == None:
            self.text.set_bbox(dict(facecolor='none', edgecolor = 'none'))
            bbox = self.text.get_bbox_patch()

        bbox_patch_tr = bbox.get_transform()
        path=bbox_patch_tr.transform_path_non_affine(bbox.get_path())
        vertices=path.vertices

        for i in range(0,4):
            self.picker_point[i]=bbox_patch_tr.transform(vertices[i])
            self.picker_point[i+4]=bbox_patch_tr.transform((vertices[i]+vertices[i+1])/2)

        picker_point_x = [value[0] for value in self.picker_point[0:4]]
        picker_point_y = [value[1] for value in self.picker_point[0:4]]

        if vertices[1][0]-vertices[0][0] > 17:
            picker_point_x += [self.picker_point[4][0],self.picker_point[6][0]]
            picker_point_y += [self.picker_point[4][1],self.picker_point[6][1]]

        if vertices[2][1]-vertices[0][1] > 35:
            picker_point_x += [self.picker_point[5][0],self.picker_point[7][0]]
            picker_point_y += [self.picker_point[5][1],self.picker_point[7][1]]

        # self.pick_state._xorig = picker_point_x
        # self.pick_state._yorig = picker_point_y
        self.pick_state.set_data(picker_point_x,picker_point_y)

    def update_bbox_position_size(self, renderer):
        """
        Update the location and the size of the bbox.

        This method should be used when the position and size of the bbox needs
        to be updated before actually drawing the bbox.
        """
        if self.text._bbox_patch:
            # don't use self.get_unitless_position here, which refers to text
            # position in Text:
            posx = float(self.text.convert_xunits(self.text._x))
            posy = float(self.text.convert_yunits(self.text._y))
            posx, posy = self.text.get_transform().transform((posx, posy))

            x_box, y_box, w_box, h_box = _get_textbox(self.text, renderer)
            self.text._bbox_patch.set_bounds(0., 0., w_box, h_box)
            self.text._bbox_patch.set_transform(
                Affine2D()
                .rotate_deg(self.text.get_rotation())
                .translate(posx + x_box, posy + y_box))
            fontsize_in_pixel = renderer.points_to_pixels(self.text.get_size())
            self.text._bbox_patch.set_mutation_scale(fontsize_in_pixel)
            self.set_pickbox_pos()

    def change_pos_mode(self, mode = True):
        if self.type is 'xlabel':
            self.axes.xaxis._autolabelpos = mode
        elif self.type is 'ylabel':
            self.axes.yaxis._autolabelpos = mode
        elif self.type is 'zlabel':
            self.axes.zaxis._autolabelpos = mode
        elif self.type is 'title':
            self.axes._autotitlepos = mode

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.ax).texts.remove(self)

        self.text.remove()

class CTitle(CTextBase):
    """
    坐标轴标题类

    Attributes:
    title : 坐标轴标题

    """

    def __init__(self, ax, title):
        super().__init__(ax, title, 'title')

    def action_delete(self):
        self.axes.set_title('')
        self.text.set_rotation(0)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class CXlabel(CTextBase):
    """
    坐标轴x轴标签

    Attributes:
    xlabel : 坐标轴x轴标签

    """

    def __init__(self, ax, xlabel):
        super().__init__(ax, xlabel, 'xlabel')

    def action_delete(self):
        self.axes.set_xlabel('')
        self.text.set_rotation(0)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class CYlabel(CTextBase):
    """
    坐标轴y轴标签

    Attributes:
    ylabel : 坐标轴y轴标签

    """

    def __init__(self, ax, ylabel):
        super().__init__(ax, ylabel, 'ylabel')

    def action_delete(self):
        self.axes.set_ylabel('')
        self.text.set_rotation(90)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class CZlabel(CTextBase):
    """
    坐标轴y轴标签

    Attributes:
    ylabel : 坐标轴y轴标签

    """

    def __init__(self, ax, zlabel):
        super().__init__(ax, zlabel, 'zlabel')

    def action_delete(self):
        self.axes.set_zlabel('')
        self.text.set_rotation(90)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class CText(CTextBase):
    """
    坐标轴文本标签

    Attributes:
    ----------------------------
    text : 文本标签

    """

    def __init__(self, ax, text):
        super().__init__(ax, text, 'text')
        self.dis_pick_self()

    def action_delete(self):
        pass

    def delete_self(self):
        self.action_delete()

class CColorbarXlabel(CTextBase):
    """
    colorbar坐标轴x轴标签

    Attributes:
    xlabel : 坐标轴x轴标签

    """

    def __init__(self, ax, connect_ax, xlabel):
        super().__init__(connect_ax, xlabel, 'xlabel')
        self.colorbar_ax = ax

    def action_delete(self):
        self.colorbar_ax.set_xlabel('')
        self.text.set_rotation(0)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class CColorbarYlabel(CTextBase):
    """
    colorbar坐标轴y轴标签

    Attributes:
    ylabel : 坐标轴y轴标签

    """

    def __init__(self, ax, connect_ax, ylabel):
        super().__init__(connect_ax, ylabel, 'xlabel')
        self.colorbar_ax = ax

    def action_delete(self):
        self.colorbar_ax.set_ylabel('')
        self.text.set_rotation(90)
        CTextBase.action_delete(self)

    def delete_self(self):
        self.action_delete()

class DrawText(object):
    """
    添加坐标轴文本标签
    """
    def __init__(self, texts, **kwargs):
        self.ax = None
        self.texts = texts
        self.text_index = 0
        self.text = self.texts[self.text_index]
        self.kwargs = kwargs
        self.dtexts = []
        self.fig = plt.gcf()

    def connect(self):
        self.cid_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        self.cid_key_press = self.fig.canvas.mpl_connect(
            'key_press_event', self.on_key_press)
        self.cid_figure_close = self.fig.canvas.mpl_connect(
            'close_event', self.on_figure_close)

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_press)
        self.fig.canvas.mpl_disconnect(self.cid_release)
        self.fig.canvas.mpl_disconnect(self.cid_motion)
        self.fig.canvas.mpl_disconnect(self.cid_key_press)
        self.fig.canvas.mpl_disconnect(self.cid_figure_close)

    def on_press(self, event):
        if event.inaxes:
            self.ax = event.inaxes
        else:
            self.ax = plt.gca()

        pos_x, pos_y = event.x, event.y
        self.draw_text = Text(x=pos_x,y=pos_y,
                        text=self.text,
                        bbox=dict(fc="none", ec="none"),
                        **self.kwargs)
                        # verticalalignment='baseline',)
                        # horizontalalignment='center',)
        self.draw_text.set_transform(self.fig.get_transform())
        # self.text.set_animated(True)
        # self.text.set_in_layout(False)
        self.fig.add_artist(self.draw_text)

        ctext = CText(self.ax, self.draw_text)
        mw_get_cax(self.ax).texts.append(ctext)
        self.dtexts.append(self.draw_text)

        self.text_index = self.text_index + 1
        if len(self.texts) > self.text_index:
            self.text = self.texts[self.text_index]
        else:
            self.disconnect()
            self.fig.canvas.stop_event_loop()

    def on_motion(self, event):
        pass

    def on_release(self, event):
        pass

    def on_key_press(self, event):
        self.on_press(event)

    def on_figure_close(self, event):
        self.disconnect()
        self.fig.canvas.stop_event_loop()

    def __call__(self, timeout = 30):
        try:
            self.fig.canvas.start_event_loop(timeout = timeout)
        finally:
            self.disconnect()

        # print(len(self.dtexts))
        if len(self.dtexts) == 1:
            return self.dtexts[0]
        else:
            return self.dtexts

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.fig).draw_text = None

        self.texts.remove()

def mw_gtext(fig, texts, **kwargs):
    """
    使用鼠标将文本添加到图窗

    Parameters:
    -------------------------
    ax : 目标坐标轴
    texts : 需要添加的文本
    """
    # disable_keymap()

    button = mw_get_toolbutton(fig, 'edit_mode')
    if button.isChecked():
        button.setChecked(False)

    # 禁用工具栏和数据提示功能
    mw_enable_toolbar(fig, False)
    mw_get_cfig().current_mplcursor.checked_tool_num += 1

    cfig = mw_get_cfig()
    cfig.draw_text = DrawText(texts, **kwargs)
    cfig.draw_text.connect()
    res = cfig.draw_text(timeout=30)

    # 开启工具栏和数据提示功能
    mw_enable_toolbar(fig, True)
    if mw_get_cfig(fig) != None:
        mw_get_cfig(fig).current_mplcursor.checked_tool_num -= 1

    return res