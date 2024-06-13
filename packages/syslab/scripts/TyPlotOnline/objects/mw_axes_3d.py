"""
名称：axes_3d
功能：此文件用于初始化当坐标轴为3d的情况
接口：初始化3d坐标轴类
依赖：
"""

from matplotlib.backend_bases import MouseButton
import weakref
from TyPlotOnline.objects.mw_interface import *
from mpl_toolkits.mplot3d import art3d, proj3d

class CAxes3D(object):
    """
    实现坐标轴的一些槽函数、右键菜单等

    Attributes
    -------------------
        ax : 目标坐标轴
        fig : 坐标轴所属图窗
    """
    def __init__(self, ax):
        self.ax = ax
        self.fig = self.ax.figure
        self.pressed = False
        self.zoom = False
        self.view = False

        self.ax.set_facecolor('none')
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

        #self.ax.margins(x = 0)
        self.init_connect()
        self.init_grid_style()
        self.init_axis()
        self.ax.set_box_aspect((1,1,0.75))
        self.ax.view_init(30, -127.5)

        self.ax.set_proj_type('ortho')

        ax.apply_aspect = apply_aspect
        self.ax._remove_method = self.ax_remove
        self.hide_labels = False

    def ax_remove(self,ax):
        self.fig.delaxes(ax)
        c_ax=mw_get_cax(self.ax)
        mw_get_cfig(self.fig).axs.remove(c_ax)
        self.dis_connect()

    def init_axis(self):
        self.ax.xaxis._axinfo["tick"]['outward_factor'] = 0
        self.ax.yaxis._axinfo["tick"]['outward_factor'] = 0
        self.ax.zaxis._axinfo["tick"]['outward_factor'] = 0

    def init_grid_style(self):
        self.ax.minorticks_off()
        self.ax.xaxis._axinfo["grid"]['color'] = (0.0, 0.0, 0.0, 0.15)
        self.ax.yaxis._axinfo["grid"]['color'] = (0.0, 0.0, 0.0, 0.15)
        self.ax.zaxis._axinfo["grid"]['color'] = (0.0, 0.0, 0.0, 0.15)

    def init_connect(self):
        self.press_id = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.release_id = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)

    def dis_connect(self):
        self.fig.canvas.mpl_disconnect(self.press_id)
        self.fig.canvas.mpl_disconnect(self.release_id)
        dict_connects = {**self.fig.canvas.callbacks._func_cid_map['motion_notify_event'],
        **self.fig.canvas.callbacks._func_cid_map['button_press_event'],
        **self.fig.canvas.callbacks._func_cid_map['button_release_event']}
        refs = weakref.getweakrefs(self.ax)
        for item in list(dict_connects.items()):
            if item[0] in refs:
                self.fig.canvas.mpl_disconnect(item[1])

    def on_press(self, event):
        """
        3d坐标轴鼠标按下事件
        """
        self.ax._button_release(event)

        # 在部分情况下，禁用掉3d坐标轴原有的鼠标事件
        if event.button is MouseButton.RIGHT:
            self.ax._button_release(event)
            return

        if event.inaxes is None or event.inaxes != self.ax:
            return

        data_tips = mw_get_cfig().current_mplcursor
        if data_tips.cid_motion_ann_pos is not None or data_tips.cid_motion_sel_pos is not None:
            return

        for cax in mw_get_cfig().axs:
            for clegend in cax.legends:
                if clegend.self_picked:
                    return

        pan_button = mw_get_toolbutton(plt.gcf(), 'pan')
        zoom_button = mw_get_toolbutton(plt.gcf(), 'zoom')

        # if pan_button.isChecked():
        #     self.ax._button_release(event)
        #     return

        if mw_get_cfig().edit_mode == True:
            self.ax._button_release(event)
            return

        # if zoom_button.isChecked():
        #     self.ax._button_release(event)
        #     self.zoom = True
        #     self.move_zoom_id = self.fig.canvas.mpl_connect(
        #         'motion_notify_event', self.on_move_zoom)
        #     return

        mw_get_cfig().current_mplcursor.checked_tool_num += 1
        self.view = True
        self.move_view_id = self.fig.canvas.mpl_connect(
        'motion_notify_event', self.on_move_view)

    def on_move_zoom(self, event):
        x, y = event.xdata, event.ydata
        # In case the mouse is out of bounds.
        if x is None:
            return

        dx, dy = x - self.ax.sx, y - self.ax.sy
        w = self.ax._pseudo_w
        h = self.ax._pseudo_h
        self.ax.sx, self.ax.sy = x, y

        minx, maxx, miny, maxy, minz, maxz = self.ax.get_w_lims()
        df = 1-((h - dy)/h)
        dx = (maxx-minx)*df
        dy = (maxy-miny)*df
        dz = (maxz-minz)*df
        self.ax.set_xlim3d(minx + dx, maxx - dx)
        self.ax.set_ylim3d(miny + dy, maxy - dy)
        self.ax.set_zlim3d(minz + dz, maxz - dz)
        self.ax.get_proj()
        self.update_annotation()
        #self.ax.figure.canvas.draw_idle()

    def on_move_view(self, event):
        x, y = event.xdata, event.ydata

        if x is None:
            return

        dx, dy = x - self.ax.sx, y - self.ax.sy
        w = self.ax._pseudo_w
        h = self.ax._pseudo_h
        self.ax.sx, self.ax.sy = x, y

        if dx == 0 and dy == 0:
            return

        self.ax.elev = art3d._norm_angle(self.ax.elev - (dy/h)*180)
        self.ax.azim = art3d._norm_angle(self.ax.azim - (dx/w)*180)
        self.ax.get_proj()

        self.update_annotation()

        self.change_lables_visible()

        #self.ax.stale = True
        self.ax.figure.canvas.draw_idle()

    def change_lables_visible(self):
        """
        当调整三维坐标轴视角时，改变重叠label的可视性
        """
        # 当调整视角与平面有2度的误差时，就隐藏lable和ticklabels
        if ((self.ax.elev <= 92 and self.ax.elev >= 88)
            or (self.ax.elev <= -88 and self.ax.elev >= -92)):
            show_label(self.ax, 'Both')
            hide_label(self.ax, 'Z')
            ticks_auto(self.ax, 'both')
            self.ax.get_zaxis().set_ticklabels([])
            self.hide_labels = True
        elif (((self.ax.elev >= -2 and self.ax.elev <= 2) or
             self.ax.elev >= 178 or self.ax.elev <= -178)
             and ((self.ax.azim <= -88 and self.ax.azim >= -92)
             or (self.ax.azim <= 92 and self.ax.azim >= 88))):
            show_label(self.ax, 'Both')
            hide_label(self.ax, 'Y')
            ticks_auto(self.ax, 'both')
            self.ax.get_yaxis().set_ticklabels([])
            self.hide_labels = True
        elif (((self.ax.elev <= 2 and self.ax.elev >= -2) or
             self.ax.elev >= 178 or self.ax.elev <= -178)
             and ((self.ax.azim >= -2 and self.ax.azim <= 2)
             or self.ax.azim >= 178 or self.ax.azim <= -178)):
            show_label(self.ax, 'Both')
            hide_label(self.ax, 'X')
            ticks_auto(self.ax, 'both')
            self.ax.get_xaxis().set_ticklabels([])
            self.hide_labels = True
        elif self.hide_labels:
            show_label(self.ax, 'Both')
            ticks_auto(self.ax, 'both')
            self.hide_labels = False

    def on_release(self, event):
        if self.zoom:
            self.fig.canvas.mpl_disconnect(self.move_zoom_id)
            self.zoom = False

        if self.view:
            self.view = False
            self.fig.canvas.mpl_disconnect(self.move_view_id)
            mw_get_cfig().current_mplcursor.checked_tool_num -= 1

    def update_annotation(self):
        return 
        if len(mw_get_cfig().current_mplcursor.selections) > 0:
            for _selection in mw_get_cfig().current_mplcursor.selections:
                selection = _selection['value']

                point = selection['point']
                if point.axes != self.ax:
                    continue

                x,y,z = point.get_data_3d()
                if isinstance(x, np.ndarray):
                    x,y,z = (x[0], y[0], z[0])
                x2,y2,_ = proj3d.proj_transform(x, y, z, self.ax.get_proj())

                ann = selection['ann']
                ann.xy = (x2, y2)

def apply_aspect(position=None):
    pass