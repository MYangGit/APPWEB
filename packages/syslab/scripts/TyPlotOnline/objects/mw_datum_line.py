"""
名称：datum_line
功能：此文件用于初始化标线
实现：实现标线的事件、槽函数、右键菜单等
接口：
依赖：
"""

from TyPlotOnline.objects.mw_interface import *
from matplotlib.backend_bases import MouseButton
from matplotlib.backend_tools import Cursors
from matplotlib.widgets import TextBox

import numpy as np

class CDrawDatumLine(object):
    """
    实现标线绘制的一些槽函数等

    Attributes:
        ax
        type_axes：标线类型
    """
    def __init__(self,ax,type_axes):
        # 标线类型，x轴标线与y轴标线
        self.type = type_axes
        self.ax = ax
  
    def connect(self):
        """进行连接的槽函数"""
        self.cid_press = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.onpress)
        self.cid_release = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.onrelease)
    
    def disconnect(self):
        """断开信号槽连接"""
        self.ax.figure.canvas.mpl_disconnect(self.cid_press)
        self.ax.figure.canvas.mpl_disconnect(self.cid_release)

    def onpress(self, event):
        """点击事件，主要用于点击生成标线等功能"""
        line = None
        # 只能左键生成
        if event.button is MouseButton.LEFT:
            # 标线坐标
            coord = None
            if self.type == "x":
                # 绘制 xline
                line = self.ax.axvline(x=event.xdata,color='black')
                coord = round(event.xdata,4)
            else:
                # 绘制 yline
                line = self.ax.axhline(y=event.ydata,color='black')
                coord = round(event.ydata,4)
            
            # 下列操作只能在鼠标左键下进行
            # 局部重绘
            self.ax.figure.canvas.draw_idle()
            # 构建CDatumLine对象
            cline = CDatumLine(self.ax,line,coord,self.type)
            # 在mw_axes的lst_datum_lines里添加当前点击生成的标线对象
            mw_get_cax().lst_datum_lines.append(cline)

    def onmove(self):
        """鼠标移动监听"""
        pass

    def onrelease(self, event):
        """鼠标松开监听"""
        # 判断当前cfigure里是否存在CAxes对象,如果存在要移除，恢复点击右键生成标线前的current_objs
        if mw_get_cfig().current_objs.count(mw_get_cax(event.inaxes)) != 0:
            mw_get_cfig().current_objs.remove(mw_get_cax(event.inaxes))
        # 创建完成，将axes的dline置空，用于datatips生成时判断当前是否在生成标线
        mw_get_cax().dline = None
        # 断开连接 实现一次点击仅能生成一根标线
        self.disconnect()

class CDatumLine(object):
    """
    实现标线的一些槽函数、右键菜单等

    Attributes:
        ax
        line：目标标线
        coord：标线初始坐标
        type_axes：标线类型
    """
    def __init__(self,ax,line,coord,type_axes):
        # 当前对象的标线
        self.line = line

        self.ax = ax

        # 线型字典
        self.dict_style = {'实线' : ['-', 'solid'],
                    '虚线' : ['--', 'dashed'],
                    '点线' : [':', 'dotted'],
                    '点划线' : ['-.', 'dashdot']}
        
        # 当前标线坐标
        self.coord = coord

        # 当前标线为x轴标线还是y轴标线
        self.type = type_axes

        # 展现当前标线坐标
        self.coordinate = None

        # 是否进行拖拽x轴标线
        self.drag_x_datum_line = False

        # 是否进行拖拽y轴标线
        self.drag_y_datum_line = False

        # 是否显示标线坐标文本
        self.show_coordinate_flag = True

        self.show_coordinate(self.coord)

        self.connect()

    def show_coordinate(self,coord):
        """展示标线坐标"""
        # 先清空当前标线坐标展示
        if self.coordinate is not None:
            self.coordinate.remove()

        if self.type == "x":
            # 标线坐标的文本
            coordinate_text = 'x={}'.format(coord)
            # 获取当前y轴的极小值，将坐标信息展现在极小值的x轴线附近
            ymin,ymax = self.ax.get_ylim()
            # 展示标线坐标
            self.coordinate = self.ax.annotate(coordinate_text, xy=(coord, 0), xytext=(coord, ymin),
                 ha='right')
        else:
            # 标线坐标的文本
            coordinate_text = 'y={}'.format(coord)
            # 获取当前y轴的极小值，将坐标信息展现在极小值的x轴线附近
            xmin,xmax = self.ax.get_xlim()
            # 展示标线坐标
            self.coordinate = self.ax.annotate(coordinate_text, xy=(0, coord), xytext=(xmin, coord),
                 ha='left')
 
    def delete_datum_line(self):
        """删除标线"""
        # 从mw_get_cfig().current_objs删除当前对象
        mw_get_cfig().current_objs.remove(self)
        # 从lst_datum_lines里删除当前对象
        mw_get_cax().lst_datum_lines.remove(self)
        # 删除标线
        self.line.remove()

        # 清空当前标线坐标展示
        if self.coordinate is not None:
            self.coordinate.remove()

        # 局部重绘
        self.ax.figure.canvas.draw_idle()
        # 解除信号槽绑定
        self.disconnect()

    def disconnect(self):
        """解除信号槽绑定"""
        self.ax.figure.canvas.mpl_disconnect(self.cid_press)
        self.ax.figure.canvas.mpl_disconnect(self.cid_motion)
        self.ax.figure.canvas.mpl_disconnect(self.cid_release)

    def on_press(self,event):
        """点击事件"""
        if event.inaxes != self.ax:
            return
        
        # 游标优先级高于标线
        if mw_get_cax(event.inaxes) == None or mw_get_cax(event.inaxes).cursor:
            return
        
        if mw_get_cfig().edit_mode:
            return
        
        # 双击标线，标线不可移动
        if event.dblclick:
            return
        
        # 只有鼠标左键才能进行拖动
        if event.button is MouseButton.LEFT:
            #  通过遍历mw_get_cax().lst_datum_lines的方式，解决标线交点拖拽会全部拖拽的问题
             for line_datum in mw_get_cax().lst_datum_lines:
                if line_datum.line.contains(event)[0]:
                    if line_datum.type == 'x':
                        line_datum.drag_x_datum_line = True
                        return
                    else:
                        line_datum.drag_y_datum_line = True
                        return
            
    def on_motion(self, event):
        """鼠标移动监听"""
        if mw_get_cfig().edit_mode:
            return
        
        if (event.inaxes != self.ax):
            return
        
        # 当鼠标悬浮经过标线上方时，要改变鼠标形态
        for line_datum in mw_get_cax().lst_datum_lines:
            if line_datum.line.contains(event)[0]:
                if line_datum.type == 'x':
                    line_datum.line.figure.canvas.send_event("cursor", cursor="e-resize")
                else:
                    line_datum.line.figure.canvas.send_event("cursor", cursor="n-resize")
                break
            else:
                line_datum.line.figure.canvas.send_event("cursor", cursor="default")

        # 移动标线并更新标线坐标显示
        if self.drag_x_datum_line:
            new_pos = event.xdata
            # 更新标线位置
            self.line.set_xdata([new_pos, new_pos])
            # 更新坐标展示位置
            coord = round(new_pos,4)
            # 更新当前坐标
            self.coord = coord 
            # 只有在显示坐标文本情况下才能在移动时显示
            if self.show_coordinate_flag:
                self.update_annotation_position(coord)
            # 小部件重绘 使用这个方法可以避免标线移动过慢
            self.ax.figure.canvas.draw_idle()
            return
        elif self.drag_y_datum_line:
            new_pos = event.ydata
            # 更新标线位置
            self.line.set_ydata([new_pos, new_pos])
            # 更新坐标展示位置
            coord = round(new_pos,4) 
            # 更新当前坐标
            self.coord = coord
            # 只有在显示坐标文本情况下才能在移动时显示
            if self.show_coordinate_flag:
                self.update_annotation_position(coord)
            # 小部件重绘 使用这个方法可以避免标线移动过慢
            self.ax.figure.canvas.draw_idle()
            return
        
    def pick_self(self, bool):
        """用于解决标线创建后点击编辑模式按钮后调用pickself函数的问题"""
        # 由于无需选中状态，因此只需pass
        pass

    def on_release(self, event):
        """鼠标释放监听"""
        if mw_get_cfig().edit_mode:
            return
        
        # 将两个拖拽标识都重置为False
        self.drag_x_datum_line = False
        self.drag_y_datum_line = False
        if mw_get_cfig().current_objs.count(self) > 0:
            mw_get_cfig().current_objs.remove(self)

    def connect(self):
        """连接槽函数"""
        # 鼠标点击事件
        self.cid_press = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        # 鼠标移动事件连接
        self.cid_motion = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        # 鼠标释放事件连接
        self.cid_release = self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def context_menu(self):
        """右键菜单"""
        menu_list = []

        # 线型
        lst_linestyle_dict = []
        linestyle = self.get_datum_linestyle()
        for key, value in self.dict_style.items():
            lst_linestyle_dict.append({"label": key, "value": value[0]})
            if linestyle in value:
                linestyle = value[0]
        menu_list.append({"value": "datumline_linestyle", "label": "线型", "children": lst_linestyle_dict, "default_value":linestyle})

         # 线宽
        lst_linewidth_label = ['0.5','1.0','1.5','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0','11.0','12.0']
        lst_linewidth_value = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
        lst_linewidth_dict = []
        lineswidth = self.get_datum_linewidth()
        for i in range(0, len(lst_linewidth_value)):
            linewidth_dict = {"label": lst_linewidth_label[i], "value": lst_linewidth_value[i]}
            lst_linewidth_dict.append(linewidth_dict)
        menu_list.append({"value": "datumline_linewidth", "label": "线宽", "children": lst_linewidth_dict, "default_value":lineswidth})

        menu_list.append({"value": "adjust_datumline_coordinate", "label": "调整标线坐标", "children": [], "default_value": ""})
        
        if self.show_coordinate_flag:
            coordinate_label = "隐藏坐标文本"
        else:
            coordinate_label = "显示坐标文本"
        #显示或隐藏坐标文本 
        menu_list.append({"value": "toggle_coordinate_labels", "label": coordinate_label, "children": [], "default_value": ""})

        # 删除当前标线右键菜单
        menu_list.append({"value": "delete_datum_line", "label": "删除当前标线", "children": [], "default_value": ""})
        
        self.ax.figure.canvas.send_event("contextmenu", menu_list=menu_list)

    def set_prop(self, name: str, value):
        """接收右键传回的值并进行处理"""
        if name == "delete_datum_line":
            # 删除当前标线
            self.delete_datum_line()
        elif name == "datumline_linewidth":
            # 标线线宽
            self.set_datum_line_width(value)
        elif name == "datumline_linestyle":
            # 标线线型
            self.set_datum_line_style(value)
        elif name == "adjust_datumline_coordinate":
            # 根据坐标调整标线坐标
            self.datum_line_by_usercoord(value)
        elif name == "toggle_coordinate_labels":
            # 显示或隐藏坐标文本
            self.toggle_coordinate_label()

    def toggle_coordinate_label(self):
        if self.show_coordinate_flag:
            if self.coordinate is not None:
                self.coordinate.remove()
                self.coordinate = None
            self.show_coordinate_flag = False
            # 局部重绘
            self.ax.figure.canvas.draw_idle()
        else:
            self.update_annotation_position(self.coord)
            self.show_coordinate_flag = True
            # 局部重绘
            self.ax.figure.canvas.draw_idle()
    
    def datum_line_by_usercoord(self,coordinate):
        """根据用户输入的数值修改标线坐标"""
        try:
            coordinate=float(coordinate)
        except Exception as e:
            return
        
        # 判断用户输入数值是否合法，主要是看用户输入数值是否超过当前x轴或者y轴范围  考虑是否加一步，将输入的值转为浮点数
        if self.type == 'x':
            # 获取当前x轴范围
            xmin,xmax = self.ax.get_xlim()
            if coordinate < xmax and coordinate > xmin:
                # 修改 xline坐标
                self.line.set_xdata([coordinate, coordinate])
                coord = round(coordinate,4)
                # 当前为显示坐标状态下进行更新，关闭状态下不需更新，因为再开启时会专门再调用
                if self.show_coordinate_flag:
                    # 更新标线展示坐标
                    self.update_annotation_position(coord)
                # 实时更新坐标
                self.coord = coord
                # 局部重绘
                self.ax.figure.canvas.draw_idle()
            else:
                # 如果数据不合法，不做操作
                pass
        if self.type == 'y':
            # 获取当前y轴范围
            ymin,ymax = self.ax.get_ylim()
            if coordinate < ymax and coordinate > ymin:
                # 修改 yline坐标
                self.line.set_ydata([coordinate, coordinate])
                coord = round(coordinate,4)
                # 当前为显示坐标状态下进行更新，关闭状态下不需更新，因为再开启时会专门再调用
                if self.show_coordinate_flag:
                    # 更新标线展示坐标
                    self.update_annotation_position(coord)
                # 实时更新坐标
                self.coord = coord
                # 局部重绘
                self.ax.figure.canvas.draw_idle()
            else:
                # 如果数据不合法，不做操作
                pass

        # 防止其他标线坐标修改影响本标线
        mw_get_cfig().current_objs.remove(self)

    def set_datum_line_width(self,linewidth):
        """根据用户右键选择的线宽调整线宽"""
        # 调整被选中标线
        self.line.set_linewidth(linewidth)
        # 当前为显示坐标状态下进行更新，关闭状态下不需更新，因为再开启时会专门再调用
        if self.show_coordinate_flag:
            # 更新标线展示坐标
            self.update_annotation_position(self.coord)
        # 局部重绘
        self.ax.figure.canvas.draw_idle()
        # 从mw_get_cfig().current_objs删除当前对象
        # 如果此处不及时删除当前对象，那么当对其他标线右键修改属性时，当前标线属性也会修改
        mw_get_cfig().current_objs.remove(self)

    def get_datum_linewidth(self):
        """获取当前标线线宽"""
        return self.line.get_linewidth()

    def get_datum_linestyle(self):
        """获取当前标线线型"""
        return self.line.get_linestyle()

    def set_datum_line_style(self,linestyle):
        """根据用户右键选择的线型调整线型"""
        # 调整被选中标线
        self.line.set_linestyle(linestyle)
        # 局部重绘
        self.ax.figure.canvas.draw_idle()
        # 从mw_get_cfig().current_objs删除当前对象
        # 如果此处不及时删除当前对象，那么当对其他标线右键修改属性时，当前标线属性也会修改
        mw_get_cfig().current_objs.remove(self)
    
    def update_annotation_position(self,coord):
        """根据线宽动态调整坐标文本范围"""
        if self.type == 'x':
            coord_data = coord
            ymin,ymax = self.ax.get_ylim()
            ymin_data = ymin
            
            # 将数据坐标转换为像素坐标
            coord_pixel, ymin_pixel = self.ax.transData.transform([(coord_data, ymin_data)])[0]
            
            # 考虑线宽因素
            linewidth = self.line.get_linewidth()
            offset_pixels = linewidth*0.8
            new_coord_pixel = coord_pixel - offset_pixels
            
            # 将新像素坐标转换回数据坐标
            new_coord_pixel, ymin_pixel = self.ax.transData.inverted().transform([(new_coord_pixel, ymin_pixel)])[0]
            # 标线坐标的文本
            coordinate_text = 'x={}'.format(coord)

            # 更新坐标文本的内容与坐标，当点击隐藏坐标文本后self.coordinate会置空，因此需考虑此情境
            if self.coordinate == None:
                self.coordinate = self.ax.annotate(coordinate_text, xy=(coord, 0), xytext=(new_coord_pixel, ymin_pixel),
                 ha='right')
            else:
                self.coordinate.set_position((new_coord_pixel, ymin_pixel))
                self.coordinate.set_text(coordinate_text)
            # 局部重绘
            self.ax.figure.canvas.draw_idle()
        else:
            coord_data = coord
            xmin,xmax = self.ax.get_xlim()
            xmin_data = xmin
            
            # 将数据坐标转换为像素坐标
            xmin_pixel, coord_pixel = self.ax.transData.transform([(xmin_data, coord_data)])[0]
            
            # 考虑线宽因素
            linewidth = self.line.get_linewidth()
            offset_pixels = linewidth*0.8
            new_coord_pixel = coord_pixel + offset_pixels
            
            # 将新像素坐标转换回数据坐标
            xmin_pixel, new_coord_pixel = self.ax.transData.inverted().transform([(xmin_pixel, new_coord_pixel)])[0]
     
            # 标线坐标的文本
            coordinate_text = 'y={}'.format(coord)
            # 更新坐标文本的内容与坐标，当点击隐藏坐标文本后self.coordinate会置空，因此需考虑此情境
            if self.coordinate == None:
                self.coordinate = self.ax.annotate(coordinate_text, xy=(0, coord), xytext=(xmin_pixel, new_coord_pixel),
                 ha='left')
            else:
                self.coordinate.set_position((xmin_pixel, new_coord_pixel))
                self.coordinate.set_text(coordinate_text)
            # 局部重绘
            self.ax.figure.canvas.draw_idle()