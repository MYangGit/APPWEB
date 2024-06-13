import datetime
import numpy as np
from matplotlib.backend_bases import MouseButton
from matplotlib.projections.polar import PolarAxes
from mpl_toolkits.mplot3d import art3d, proj3d
from mpl_toolkits.mplot3d.art3d import Line3D, Path3DCollection
from TyPlotOnline.objects.mw_plot3 import *
# from PyQt5.QtGui import QCursor
# from PyQt5.QtWidgets import QMenu


_default_annotation_kwargs = dict(
    bbox=dict(
        boxstyle="round,pad=0.5,rounding_size=0.2",
        fc="#fafaff",
        alpha=1,
        ec="#969698",
    ),
    linespacing = 1.6,
    # arrowprops=dict(
    #     arrowstyle="->",
    #     connectionstyle="arc3",
    #     shrinkB=0,
    #     ec="k",
    # ),
)

_default_annotation_positions = [
    dict(position=(-7, 7), anncoords="offset points",
         horizontalalignment="right", verticalalignment="bottom"),
    dict(position=(7, 7), anncoords="offset points",
         horizontalalignment="left", verticalalignment="bottom"),
    dict(position=(7, -7), anncoords="offset points",
         horizontalalignment="left", verticalalignment="top"),
    dict(position=(-7, -7), anncoords="offset points",
         horizontalalignment="right", verticalalignment="top"),
]

_location = {
    'northeast' : 1,
    'northwest' : 0,
    'southeast' : 2,
    'southwest' : 3,
}


class Cursor(object):
    def __init__(self, fig, ax):
        self.selections = []
        self.fig = fig
        self.ax = ax
        self.canvas = self.fig.canvas
        self.enabled = True
        self.connect()
        self.current_selection = None
        self.ann_pressed = False
        self.point_pressed = False
        self.hovered = False
        self.data_tips_on = True
        self.artist = None
        self.hover_annotate = None
        self.hover_point = None
        self.hover = {}
        self.cid_motion_ann_pos = None
        self.cid_motion_sel_pos = None
        self.selection_index = 0
        self.index = None
        self.background = None
        self.checked_tool_num = 0
        self.alt_open = False

        # 判断当前位置是否已生成data tips，用于release事件删除data tips的判断
        self.has_generate = False
        # 判断当前是否进行了拖拽data tips的操作，用于release事件删除data tips的判断
        self.has_move = False

        #self.init_hover_selection()

        self.default_annotation_positions = [
            dict(position=(-7, 7), anncoords="offset points",
                horizontalalignment="right", verticalalignment="bottom"),
            dict(position=(7, 7), anncoords="offset points",
                horizontalalignment="left", verticalalignment="bottom"),
            dict(position=(7, -7), anncoords="offset points",
                horizontalalignment="left", verticalalignment="top"),
            dict(position=(-7, -7), anncoords="offset points",
                horizontalalignment="right", verticalalignment="top"),
        ]
        
    def before_export(self):
        self.canvas = None
        self.background = None
        if self.cid_draw:
            self.fig.canvas.mpl_disconnect(self.cid_draw)

    def after_export(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()

    def after_import(self):
        self.canvas=self.fig.canvas
        self.background=self.canvas.copy_from_bbox(self.fig.bbox)
        self.connect()
        
    # 初始化悬浮的标签和点
    def init_hover_selection(self):
        xmin, xmax = plt.gca().get_xlim()
        ymin, ymax = plt.gca().get_ylim()
        pos = ((xmin + xmax)/2, (ymin + ymax)/2)

        self.hover_annotate = self.fig.gca().annotate("",
                                                xy=pos,
                                                xytext=(0,0),textcoords="offset points",
                                                horizontalalignment=("left"),
                                                verticalalignment=("baseline"),
                                                visible=True,
                                                zorder=1e10,
                                                **_default_annotation_kwargs)
        self.hover_annotate.set(**_default_annotation_positions[1])
        self.hover_point, = plt.gca().plot(pos[0], pos[1], "o", mfc = '#808080', mec = 'w', zorder=np.inf, visible = True)

    def connect(self):
        self.data_tips_on = True
        self.connect_move()
        self.connect_press()
        self.cid_release = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cid_key_press = self.fig.canvas.mpl_connect(
            'key_press_event', self.on_key_press)
        self.cid_draw = self.fig.canvas.mpl_connect(
            'draw_event', self.on_draw)
        self.cid_key_release = self.fig.canvas.mpl_connect(
            'key_release_event',self.on_key_release)

    def on_key_release(self,event):
        # 退出使用alt快捷键或者shift快捷键打多个marker点
        if event.key in ['alt','shift']:
            self.alt_open = False
            return

    def disconnect(self):
        self.disconnect_move()
        self.disconnect_press()
        self.fig.canvas.mpl_disconnect(self.cid_release)
        self.data_tips_on = False

    def connect_move(self):
        self.cid_motion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def connect_press(self):
        self.cid_press = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)

    def disconnect_move(self):
        self.fig.canvas.mpl_disconnect(self.cid_motion)

    def disconnect_press(self):
        self.fig.canvas.mpl_disconnect(self.cid_press)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)

        if self.background != None:
            self.canvas.restore_region(self.background)

        self.draw_self()

    def draw_self(self):
        if not isinstance(self.ax, Axes3D):
            if self.hover_point != None:
                self.ax.draw_artist(self.hover_point)
        if self.hover_annotate != None:
            self.ax.draw_artist(self.hover_annotate)
        for sel_dict in self.selections:  # LIFO.
            sel = sel_dict['value']
            ann = sel['ann']
            point = sel['point']
            self.ax.draw_artist(ann)
            if not isinstance(self.ax, Axes3D):
                self.ax.draw_artist(point)
        if self.current_selection != None:
            selection = self.current_selection['value']
            ann_cur = selection['ann']
            point_cur = selection['point']
            self.ax.draw_artist(ann_cur)
            if not isinstance(self.ax, Axes3D):
                self.ax.draw_artist(point_cur)

    def on_pick(self, event):
        pass
        # if isinstance(event.artist, Rectangle):
        #     if self.category == 'v':
        #         x = bar.get_x()
        #         y = bar.get_y()
        #         width = bar.get_width()
        #         height = bar.get_height()
        #         pos_top_x = (x*2 + width)/2
        #         pos_top_y = y + height
        #         pos = (pos_top_x,pos_top_y)
        #         text = 'X ' + label.get_text() +'\nY ' + str(pos_top_y)
        #     else:
        #         x = bar.get_x()
        #         y = bar.get_y()
        #         width = bar.get_width()
        #         height = bar.get_height()
        #         pos_right_x = x + width
        #         pos_right_y = y + height / 2
        #         pos = (pos_right_x,pos_right_y)
        #         text = 'X ' + str(pos_right_x) + '\nY ' + label.get_text()
        #     mw_get_cax(self.ax).current_mplcursor.create_selection(self.ax, text, pos, bar)

    def on_key_press(self, event):
        if self.checked_tool_num:
            return

        if event.key not in ['left', 'up', 'right', 'down','delete','alt','shift']:
            return

        if len(mw_get_cfig().axs) == 0:
            return

        if mw_get_cax(plt.gca()).cursor:
            return

        if event.key in ['left', 'down']:
            self.current_selection_pos_sub(event)
            return
        elif event.key in ['right', 'up']:
            self.current_selection_pos_add(event)
            return
        elif event.key == 'delete':
            self.delete_current()
            return
        # 使用alt快捷键或者shift快捷键打多个marker点
        elif event.key in ['alt','shift']:
            self.alt_open = True
            return

    def on_press(self, event):
        # self.ann_pressed = False
        # self.point_pressed = False
        # 先判断是否选中了标签或标签点
        if self.checked_tool_num:
            return

        if self.ax == None:
            return

        if mw_get_cax(event.inaxes) == None or mw_get_cax(event.inaxes).cursor or mw_get_cax(event.inaxes).dline != None:
            return
        
        # 遍历所有标线，判断当前点击是否在标线上
        for datum_line in mw_get_cax().lst_datum_lines:
            if datum_line.line.contains(event)[0]:
                return

        for sel_dict in self.selections:  # LIFO.
            sel = sel_dict['value']
            ann = sel['ann']
            point = sel['point']
            if event.canvas is not ann.figure.canvas:
                continue

            contained_ann, _ = ann.contains(event)
            contained_point, _ = point.contains(event)
            if contained_ann:
                # 选中
                self.on_select(sel_dict)
                if event.button is MouseButton.RIGHT:
                    # 右键菜单
                    self.context_menu()
                elif event.button is MouseButton.LEFT:
                    # event.canvas.setCursor(Qt.SizeAllCursor)
                    self.cid_motion_ann_pos = event.canvas.mpl_connect('motion_notify_event', self.on_motion_ann_postion)
                    self.disconnect_move()
                    self.ann_pressed = True
                return
            elif contained_point:
                if event.button is MouseButton.RIGHT:
                    self.on_select(sel_dict)
                    self.context_menu()
                    return
                elif event.button is MouseButton.LEFT:
                    self.has_generate = True
                    self.has_move = False
                    self.on_select(sel_dict)
                    self.cid_motion_sel_pos = event.canvas.mpl_connect('motion_notify_event', self.on_motion_selection_postion)
                    self.disconnect_move()
                    self.contained_point = True
                return

        if not event.inaxes or mw_get_cax(event.inaxes) is None:
            return
        # 再判断当前hover标签是否显示，若显示，则将该标签添加到图形上
        # if self.hover_annotate != None and self.index != None:
        #     index1 = self.index
        #     self.update_hover_selection()
        #     if isinstance(self.artist, Line3D):
        #         result = self.line_data_tips(self.artist, index1, event.inaxes, event)
        #         if len(result) == 4:
        #             text, pos_pnn, pos_point, index = result
        #             self.create_selection_3d(event.inaxes, text, pos_pnn, pos_point, self.artist, index)
        #     else:
        #         # text, pos, index = result
        #         # self.create_selection(event.inaxes, text, pos, self.artist, index)
        #         text = self.hover_annotate.get_text()
        #         pos = self.hover_annotate.xy
        #         self.update_hover_selection()
        #         self.create_selection(event.inaxes, text, pos, self.artist, index1)
        # elif mw_get_cfig().data_tips:
        self.create_new_selection(mw_get_cax(event.inaxes), event, False, True)

    def on_release(self, event):
        # if self.ann_pressed:
        #     self.ann_pressed = False
        # if self.point_pressed:
        #     self.point_pressed = False
        if self.checked_tool_num > 0:
            return

        if self.ax == None:
            return

        if mw_get_cax(plt.gca()).cursor:
            return

        # 删除data tips
        for sel_dict in self.selections:
            sel = sel_dict['value']
            ann = sel['ann']
            point = sel['point']
            contained_point, _ = point.contains(event)
            if contained_point:
                # 当左键点击、当前存在data tips且未经过拖拽操作，可以删除
                if event.button is MouseButton.LEFT and self.has_generate and not self.has_move:
                    self.selections.remove(sel_dict)
                    ann.remove()
                    point.remove()
                    self.current_selection = None
                    if len(self.selections) > 0:
                        self.on_select(self.selections[-1])
                    # 删除之后，self.has_generate置为False
                    self.has_generate = False
                    # 小部件重绘 使用这个方法可以避免标线移动过慢
                    self.ax.figure.canvas.draw_idle()

        self.update_hover_selection()
        event.canvas.mpl_disconnect(self.cid_motion_ann_pos)
        event.canvas.mpl_disconnect(self.cid_motion_sel_pos)
        self.connect_move()

        self.cid_motion_ann_pos = None
        self.cid_motion_sel_pos = None

    # 旋转标签
    def on_motion_ann_postion(self, event):
        self.fig.canvas.send_event("cursor", cursor="all-scroll")
        selection = self.current_selection['value']
        ann = selection['ann']
        ann_x, ann_y = ann.xy
        if isinstance(ann_x, datetime.date):
            ann_x = matplotlib.dates.date2num(ann_x)
        if isinstance(ann_y, datetime.date):
            ann_y = matplotlib.dates.date2num(ann_y)

        ax = ann.axes
        if isinstance(ax, PolarAxes):
            ann_x,ann_y = mw_data_to_display(ax, [ann_x,ann_y])
            xdata, ydata = event.x, event.y
        else:
            ax = ann.axes
            xdata, ydata = ax.transData.inverted().transform([event.x, event.y])

        # xdata = event.xdata
        # ydata = event.ydata

        fontsize = ann.get_fontsize()
        position_adjust = fontsize*0.5 + 1
        if xdata > ann_x and ydata > ann_y:
            ann.set(**self.default_annotation_positions[1])
            ann.set(position=(position_adjust,position_adjust))
        elif xdata < ann_x and ydata > ann_y:
            ann.set(**self.default_annotation_positions[0])
            ann.set(position=(-position_adjust,position_adjust))
        elif xdata < ann_x and ydata < ann_y:
            ann.set(**self.default_annotation_positions[3])
            ann.set(position=(-position_adjust,-position_adjust))
        elif xdata > ann_x and ydata < ann_y:
            ann.set(**self.default_annotation_positions[2])
            ann.set(position=(position_adjust,-position_adjust))

        self._update()

    # 移动标签
    def on_motion_selection_postion(self, event):
        self.fig.canvas.send_event("cursor", cursor="all-scroll")
        artist = self.current_selection['value']['artist']

        if not isinstance(artist, Line2D):
            return

        contains, attrd =  artist.contains(event)
        if isinstance(artist, Line3D):
            return
        elif isinstance(artist, Line2D):
            # result = self.line_data_tips(artist, attrd['ind'][0], event.inaxes, event)
            # if len(result) == 4:
            #     text, pos_pnn, pos_point, index = result
            #     self.update_current_selection_3d(event.inaxes, text, pos_pnn, pos_point)
            # else:
            if contains:
                text, pos, index = self.line_data_tips(artist, attrd['ind'][0], event.inaxes, event)
                self.update_current_selection(event.inaxes, text, pos, index)
            else:
                xdata, ydata = plt.gca().transData.inverted().transform([event.x, event.y])
                xdatas, ydatas = artist.get_data()
                if xdata in xdatas:
                    pass

                index_right = np.searchsorted(xdatas, [xdata])[0]
                if index_right >= len(xdatas):
                    ind = len(xdatas) - 1
                    text, pos, index = self.line_data_tips(artist, ind, event.inaxes, event)
                    self.update_current_selection(event.inaxes, text, pos, index)
                else:
                    x_right, y_right = plt.gca().transData.transform([xdatas[index_right], ydatas[index_right]])
                    x_left, y_left = plt.gca().transData.transform([xdatas[index_right-1], ydatas[index_right-1]])

                    ind = index_right if (((x_right - event.x)**2 + (y_right - event.y)**2) <
                        ((x_left - event.x)**2 + (y_left - event.y)**2)) else index_right - 1

                    text, pos, index = self.line_data_tips(artist, ind, event.inaxes, event)
                    self.update_current_selection(event.inaxes, text, pos, index)
        # 移动完成之后，设self.has_move为True
        self.has_move = True

    # 鼠标移动事件
    def on_motion(self, event):
        """
        鼠标移动事件
        """
        if self.checked_tool_num > 0:
            return

        if self.ax == None:
            return

        if mw_get_cax(event.inaxes) == None or mw_get_cax(event.inaxes).cursor:
            return

        # if not mw_get_cfig().data_tips:
        #     return

        # print(event)
        # 先判断是否在坐标轴内
        if not event.inaxes:
            self.update_hover_selection()
            return

        self.ax = event.inaxes
        self.hovered = False
        for sel_dict in self.selections:  # LIFO.
            sel = sel_dict['value']
            ann = sel['ann']
            if event.canvas is not ann.figure.canvas:
                continue

            contained, _ = ann.contains(event)
            if contained:
                # 鼠标移到标签上，则不触发添加标签的操作
                self.hovered = True
                #if mw_get_cfig().data_tips:
                # event.canvas.setCursor(Qt.SizeAllCursor)
                self.fig.canvas.send_event("cursor", cursor="all-scroll")
                self.update_hover_selection()
                return
            else:
                self.fig.canvas.send_event("cursor", cursor="default")

        ax = event.inaxes
        current_ax = mw_get_cax(ax)
        if current_ax == None:
            return

        #contains = False
        # cfig = mw_get_cfig()
        #self.update_hover_selection()
        if mw_get_cfig(self.fig).data_tips_on:
            contains = self.create_new_selection(current_ax, event, False)

            if not contains:
                # event.canvas.setCursor(Qt.ArrowCursor)
                self.update_hover_selection()
        else:
            return

    def create_new_selection(self, current_ax, event, contains, press = False):

        lst_bar_containers = []
        lst_lines = []
        lst_scatters = []
        lst_stems = []
        lst_errorbars = []
        lst_areas = []
        lst_hists = []
        lst_surfs = []
        lst_streamlines = []
        lst_feathers = []
        lst_quivers = []
        lst_quiver3s = []

        lst_bar_containers = current_ax.bar_containers
        lst_lines += current_ax.lines
        lst_scatters += current_ax.scatters
        lst_stems += current_ax.stems
        lst_errorbars = current_ax.errorbars
        lst_areas += current_ax.areas
        lst_hists += current_ax.histograms
        lst_surfs += current_ax.surfs
        lst_streamlines += current_ax.streamlines
        lst_feathers += current_ax.feathers
        lst_quivers += current_ax.quivers
        lst_quiver3s += current_ax.quiver3s

        from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
        if current_ax.__class__.__name__ == "CAxesYyaxis":
            cax_2 = current_ax.cax2

            lst_bar_containers += cax_2.bar_containers
            lst_lines += cax_2.lines
            lst_scatters += cax_2.scatters
            lst_stems += cax_2.stems
            lst_errorbars += cax_2.errorbars
            lst_areas += cax_2.areas
            lst_hists += cax_2.histograms
            lst_surfs += cax_2.surfs
            lst_streamlines += cax_2.streamlines
            lst_feathers += cax_2.feathers
            lst_quivers += cax_2.quivers
            lst_quiver3s += cax_2.quiver3s

        if len(lst_bar_containers) != 0:
            for c_bar in lst_bar_containers:
                contains = c_bar.contains_self(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos, text, bar = self.bar_data_tips(c_bar, event)
                        self.create_selection(c_bar.ax, text, pos, bar)
                    elif not mw_get_cfig().data_tips:
                        pos, text, bar = self.bar_data_tips(c_bar, event)
                        self.update_hover_selection(c_bar.ax, text, pos, bar)
                    return contains

        if len(lst_lines) != 0 :
            for c_line in lst_lines:
                contains, attrd = c_line.line.contains(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    #self.line_data_tips(c_line, attrd, ax, event, press)

                    if press:
                        result = self.line_data_tips(c_line.line, attrd['ind'][0], c_line.ax, event)
                        if len(result) == 4:
                            text, pos_pnn, pos_point, index = result
                            self.create_selection_3d(c_line.ax, text, pos_pnn, pos_point, c_line.line, index)
                        else:
                            text, pos, index = result
                            self.create_selection(c_line.ax, text, pos, c_line.line, index)
                    elif not mw_get_cfig().data_tips:
                        result = self.line_data_tips(c_line.line, attrd['ind'][0], c_line.ax, event)
                        if len(result) == 4:
                            text, pos_pnn, pos_point, index = result
                            self.update_hover_selection_3d(c_line.ax, text, pos_pnn, pos_point, c_line.line, index)
                        else:
                            text, pos, index = result
                            self.update_hover_selection(c_line.ax, text, pos, c_line.line, index)
                    return contains

        if len(lst_stems) != 0:
            for c_stem in lst_stems:
                contains, attrd = c_stem.markerline.contains(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos_2d,pos_3d,text = self.stem_data_tips(c_stem, attrd["ind"][0], c_stem.ax, event)
                        if pos_3d is not None:
                            self.create_selection_3d(c_stem.ax, text, pos_2d, pos_3d)
                        else:
                            self.create_selection(c_stem.ax, text, pos_2d)
                    elif not mw_get_cfig().data_tips:
                        pos_2d,pos_3d,text = self.stem_data_tips(c_stem, attrd["ind"][0], c_stem.ax, event)
                        if pos_3d is not None:
                            self.update_hover_selection_3d(c_stem.ax, text, pos_2d, pos_3d)
                        else:
                            self.update_hover_selection(c_stem.ax, text, pos_2d)
                    return contains

                contains, attrd = c_stem.stemlines.contains(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos_2d,pos_3d,text = self.stem_data_tips(c_stem, attrd["ind"][0], c_stem.ax, event)
                        if pos_3d is not None:
                            self.create_selection_3d(c_stem.ax, text, pos_2d, pos_3d)
                        else:
                            self.create_selection(c_stem.ax, text, pos_2d)
                    elif not mw_get_cfig().data_tips:
                        pos_2d,pos_3d,text = self.stem_data_tips(c_stem, attrd["ind"][0], c_stem.ax, event)
                        if pos_3d is not None:
                            self.update_hover_selection_3d(c_stem.ax, text, pos_2d, pos_3d)
                        else:
                            self.update_hover_selection(c_stem.ax, text, pos_2d)
                    return contains

        if len(lst_errorbars) != 0:
            for c_errorbars in lst_errorbars:
                contains, attrd = c_errorbars.contains_self(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos, text = self.errorbar_data_tips(c_errorbars, attrd["ind"][0], event)
                        self.create_selection(c_errorbars.ax, text, pos)
                    elif not mw_get_cfig().data_tips:
                        pos, text = self.errorbar_data_tips(c_errorbars, attrd["ind"][0], event)
                        self.update_hover_selection(c_errorbars.ax, text, pos)
                    return contains

        if len(lst_areas) != 0:
            for c_area in lst_areas:
                contains, attrd = c_area.contains_self(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos, text = self.area_data_tips(c_area, attrd, c_area.ax, event)
                        self.create_selection(c_area.ax, text, pos)
                    elif not mw_get_cfig().data_tips:
                        pos, text = self.area_data_tips(c_area, attrd, c_area.ax, event)
                        self.update_hover_selection(c_area.ax, text, pos)
                    return contains

        if len(lst_hists) != 0:
            for c_hist in lst_hists:
                contains, attrd, bar = c_hist.contains_self(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos, text = self.hist_data_tips(c_hist, bar, event)
                        self.create_selection(c_hist.ax, text, pos)
                    elif not mw_get_cfig().data_tips:
                        pos, text = self.hist_data_tips(c_hist, bar, event)
                        self.update_hover_selection(c_hist.ax, text, pos)
                    return contains

        if len(lst_surfs) != 0:
            pass
            # for c_surf in lst_surfs:
            #     contains, attrd = c_surf.contains_self(event)
            #     if contains:
            #         contains = True
            #         event.canvas.setCursor(Qt.CrossCursor)

            #         if press:
            #             self.surf_data_tips(c_surf, attrd, c_surf.ax, event, press)

            #         # if not mw_get_cfig().data_tips:
            #         #     self.surf_data_tips(c_surf, attrd, ax, event, press)
            #         #     #self.update_hover_selection(ax, text, pos)
            #         break

        if len(lst_streamlines) != 0:
            for c_streamline in lst_streamlines:
                contains, attrd = c_streamline.streamline.contains(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        result = self.line_data_tips(c_streamline.streamline, attrd['ind'][0], c_streamline.ax, event)
                        if len(result) == 4:
                            text, pos_pnn, pos_point, index = result
                            self.create_selection_3d(c_streamline.ax, text, pos_pnn, pos_point, c_streamline.streamline, index)
                        else:
                            text, pos, index = result
                            self.create_selection(c_streamline.ax, text, pos, c_streamline.streamline, index)
                    elif not mw_get_cfig().data_tips:
                        result = self.line_data_tips(c_streamline.streamline, attrd['ind'][0], c_streamline.ax, event)
                        if len(result) == 4:
                            text, pos_pnn, pos_point, index = result
                            self.update_hover_selection_3d(c_streamline.ax, text, pos_pnn, pos_point, c_streamline.streamline, index)
                        else:
                            text, pos, index = result
                            self.update_hover_selection(c_streamline.ax, text, pos, c_streamline.streamline, index)
                    return contains

        if len(lst_feathers) != 0:
            # print(len(current_ax.feather_baselines))
            for c_feather in lst_feathers:
                contains_feather, attrd_feather = c_feather.feather.feather.contains(event)
                contains_arrow, attrd_arrow = c_feather.feather.arrow.contains(event)
                if contains_feather or contains_arrow:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        if contains_feather:
                            text, pos, index = self.feather_data_tips(c_feather.feather, attrd_feather['ind'][0], c_feather.ax, 1,event)
                            self.create_selection(c_feather.ax, text, pos, c_feather.feather.arrow, index)
                        elif contains_arrow:
                            text, pos, index = self.feather_data_tips(c_feather.feather, attrd_arrow['ind'][0], c_feather.ax, 0, event)
                            self.create_selection(c_feather.ax, text, pos, c_feather.feather.arrow, index)
                    elif not mw_get_cfig().data_tips:
                        if contains_feather :
                            text, pos, index = self.feather_data_tips(c_feather.feather, attrd_feather['ind'][0], c_feather.ax, 1, event)
                            self.update_hover_selection(c_feather.ax, text, pos, c_feather.feather.feather, index)
                        elif contains_arrow:
                            text, pos, index = self.feather_data_tips(c_feather.feather, attrd_arrow['ind'][0], c_feather.ax, 0, event)
                            self.update_hover_selection(c_feather.ax, text, pos, c_feather.feather.arrow, index)
                    return contains
        if len(current_ax.feather_baselines)!=0:
            for c_line in current_ax.feather_baselines:
                contains, attrd = c_line.line.contains(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        result = self.line_data_tips(c_line.line, attrd['ind'][0], c_line.ax, event)
                        text, pos, index = result
                        self.create_selection(c_line.ax, text, pos, c_line.line, index)
                    elif not mw_get_cfig().data_tips:
                        result = self.line_data_tips(c_line.line, attrd['ind'][0], c_line.ax, event)
                        text, pos, index = result
                        self.update_hover_selection(c_line.ax, text, pos, c_line.line, index)
                    return contains


        if len(lst_quivers) != 0:
            for c_quiver in lst_quivers:
                contains = c_quiver.contains_self(event)
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)
                    if press:
                        pos, text, index = self.quiver_data_tips(c_quiver, c_quiver.ax,event)
                        self.create_selection(c_quiver.ax, text, pos)
                    elif not mw_get_cfig().data_tips:
                        pos, text, index= self.quiver_data_tips(c_quiver,c_quiver.ax,event)
                        self.update_hover_selection(c_quiver.ax, text, pos)
                    return contains
            return contains
        
        if len(lst_scatters) != 0:
            for c_catter in lst_scatters:
                contains, attrd = c_catter.path_collection.contains(event)
                if isinstance(c_catter.path_collection,Path3DCollection):
                    return False
                if contains:
                    contains = True
                    # event.canvas.setCursor(Qt.CrossCursor)

                    if press:
                        pos, text = self.scatter_data_tips(c_catter, attrd, event)
                        self.create_selection(c_catter.ax, text, pos)
                    elif not mw_get_cfig().data_tips:
                        pos, text = self.scatter_data_tips(c_catter, attrd, event)
                        self.update_hover_selection(c_catter.ax, text, pos)
                    return contains

    def bar_data_tips(self, c_bar, event):
        if len(c_bar.ticks) >= len(c_bar.bars):
            ticks = c_bar.ticks
        else:
            if c_bar.category == 'v':
                ticks = c_bar.ax.get_xticks()
            else:
                ticks = c_bar.ax.get_yticks()

        for bar, label in zip(c_bar.bars, ticks):
            contains, attrd = bar.contains(event)
            if contains:
                return self.bar_get_pos(c_bar, bar, label)
                # pos = []
                # if c_bar.category == 'v':
                #     x = bar.get_x()
                #     y = bar.get_y()
                #     width = bar.get_width()
                #     height = bar.get_height()
                #     pos_top_x = (x*2 + width)/2
                #     pos_top_y = y + height
                #     pos = (pos_top_x,pos_top_y)
                #     text = str_remove_zeros(str('X ' + str(label) +'\nY ' + str(('%1.6g' % pos_top_y))))
                # else:
                #     x = bar.get_x()
                #     y = bar.get_y()
                #     width = bar.get_width()
                #     height = bar.get_height()
                #     pos_right_x = x + width
                #     pos_right_y = y + height / 2
                #     pos = (pos_right_x,pos_right_y)
                #     text = str_remove_zeros(str('X ' + str(('%1.6g' % (pos_right_x))) + '\nY ' + str(label)))
                # return pos, text, bar

    def bar_get_pos(self, c_bar, bar, label = None):
        pos = []
        if c_bar.category == 'v':
            x = bar.get_x()
            y = bar.get_y()
            width = bar.get_width()
            height = bar.get_height()
            pos_top_x = (x*2 + width)/2
            pos_top_y = y + height
            pos = (pos_top_x,pos_top_y)
            if label == None:
                label = pos_top_x

            if isinstance(label, np.number):
                str_x = str_remove_zeros(str('%.6f' % (label)))
            else:
                str_x = str(label)

            if isinstance(pos_top_y, np.number):
                str_y = str_remove_zeros(str('%.6f' % (pos_top_y)))
            else:
                str_y = str(pos_top_y)
            text = 'X ' + str_x + '\nY ' + str_y
            # text = str_remove_zeros(str('X ' + str('%1.6g' % (label)) +'\nY ' + str('%1.6g' % pos_top_y)))
        else:
            x = bar.get_x()
            y = bar.get_y()
            width = bar.get_width()
            height = bar.get_height()
            pos_right_x = x + width
            pos_right_y = y + height / 2
            pos = (pos_right_x,pos_right_y)
            if label == None:
                label = pos_right_y

            if isinstance(pos_right_x, np.number):
                str_x = str_remove_zeros(str('%.6f' % (pos_right_x)))
            else:
                str_x = str(pos_right_x)

            if isinstance(label, np.number):
                str_y = str_remove_zeros(str('%.6f' % (label)))
            else:
                str_y = str(label)
            text = 'X ' + str_x + '\nY ' + str_y

            # text = str_remove_zeros(str('X ' + str('%1.6g' % (pos_right_x)) + '\nY ' + str('%1.6g' % (label))))
        return pos, text, bar

    def line_data_tips(self, line, index, ax, event):
        # index = ind if isinstance(ind, np.number) else ind["ind"][0]
        if isinstance(line, Line3D):
            xdata,ydata,zdata = line.get_data_3d()
            if index < 0:
                index = 0
            elif index > len(xdata) - 1:
                index = len(xdata) - 1
            x, y, z = xdata[index], ydata[index], zdata[index]
            pos = (x, y, z)
            text = str('X ' + str_remove_zeros(str(('%1.6g' % (x))))
                    + '\nY ' + str_remove_zeros(str(('%1.6g' % (y))))
                    + '\nZ ' + str_remove_zeros(str(('%1.6g' % (z)))))
            x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
            # if press:
            #     self.create_selection_3d(ax, text, (x2, y2), pos, line)
            # elif not mw_get_cfig().data_tips:
            #     self.update_hover_selection_3d(ax, text, (x2, y2), pos, line)
            return text, (x2, y2), pos, index
        else:
            x,y = line.get_data()
            if index < 0:
                index = 0
            elif index > len(x) - 1:
                index = len(x) - 1
            pos = (x[index], y[index])
            if mw_get_cax(ax).is_geomap:
                pos_original = pos
                pos = mw_get_cax(ax).geomap(x[index], y[index],inverse=True)

            if isinstance(pos[0], (np.number, float)):
                if isinstance(line.axes,PolarAxes):
                    str_x = str_remove_zeros(str(('%1.6g' % (np.rad2deg(pos[0])%360)))+"°")
                else:
                    str_x = str_remove_zeros(str(('%1.6g' % (pos[0]))))
            else:
                if isinstance(line.axes,PolarAxes):
                    str_x = str(np.rad2deg(pos[0]))+"°"
                else:
                    str_x = str(pos[0])
            if isinstance(pos[1], (np.number, float)):
                str_y = str_remove_zeros(str(('%1.6g' % (pos[1]))))
            else:
                str_y = str(pos[1])
            if mw_get_cax(ax).is_geomap:
                pos = pos_original
                text = 'Latitude ' + str_y + '\nLongitude ' + str_x
            else:
                text = 'X ' + str_x + '\nY ' + str_y
            # if press:
            #     self.create_selection(ax, text, pos, line)
            # elif not mw_get_cfig().data_tips:
            #     self.update_hover_selection(ax, text, pos, line)
            return text, pos, index

    def scatter_data_tips(self, c_scatter, ind, event):
        path_collection = c_scatter.path_collection
        pos = path_collection.get_offsets()[ind["ind"][0]]
        if mw_get_cax(c_scatter.ax).is_geomap:
            pos_original = pos
            pos = mw_get_cax(c_scatter.ax).geomap(pos[0], pos[1],inverse=True)
        # if isinstance(c_scatter.ax,PolarAxes):
        #     text = 'X ' + str_remove_zeros(str(('%1.6g' % (np.rad2deg(pos[0])%360))))+'°' + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
        # else:
        #     text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
        text = self.scatter_pos2text(c_scatter.ax, pos)
        if mw_get_cax(c_scatter.ax).is_geomap:
            pos = pos_original
        return pos, text

    def scatter_pos2text(self,ax,pos):
        if isinstance(ax,PolarAxes):
            text = 'X ' + str_remove_zeros(str(('%1.6g' % (np.rad2deg(pos[0])%360))))+'°' + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
        else:
            if mw_get_cax(ax).is_geomap:
                text = 'Latitude ' + str_remove_zeros(
                    str(('%1.6g' % (pos[1])))) + '\nLongitude ' + str_remove_zeros(str(('%1.6g' % (pos[0]))))
            else:
                text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))

        return text

    def stem_data_tips(self, c_stem, index, ax, event):
        markerline = c_stem.markerline
        if isinstance(markerline,Line3D):
            x_a,y_a,z_a = markerline.get_data_3d()
            (x_3d,y_3d,z_3d) = (x_a[index], y_a[index],z_a[index])
            x, y, _ = proj3d.proj_transform(x_3d,y_3d,z_3d, ax.get_proj())
            pos_2d = (x,y)
            pos_3d = (x_3d,y_3d,z_3d)
            text = str_remove_zeros(str('X ' + str(('%1.6g' % (x_3d))))
                    + '\nY ' + str_remove_zeros(str(('%1.6g' % (y_3d))))
                    + '\nZ ' + str_remove_zeros(str(('%1.6g' % (z_3d)))))
        else:
            x,y = markerline.get_data()
            pos_2d = (x[index], y[index])
            pos_3d = None

            if isinstance(ax.xaxis.converter, matplotlib.dates.DateConverter):
                str_x = str(matplotlib.dates.num2date(pos_2d[0]))
            else:
                str_x = str_remove_zeros(str(('%1.6g' % (pos_2d[0]))))

            if isinstance(ax.yaxis.converter, matplotlib.dates.DateConverter):
                str_y = str(matplotlib.dates.num2date(pos_2d[1]))
            else:
                str_y = str_remove_zeros(str(('%1.6g' % (pos_2d[1]))))

            text = 'X ' + str_x + '\nY ' + str_y

            # text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos_2d[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos_2d[1]))))

        return pos_2d, pos_3d, text

    def errorbar_data_tips(self, c_errorbar, index, event):
        error_container = c_errorbar.errorbar_container
        data_line = c_errorbar.data_line

        x,y = data_line.get_data()
        pos = (x[index], y[index])
        text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))

        if error_container.has_xerr:
            error_x = error_container[2][0].get_paths()[index]
            x_left, x_right = error_x.vertices
            delta_x = ('\nX Delta [' + str_remove_zeros(('%1.6g' % (x_left[0] - x[index])))
                    + ' ' + str_remove_zeros(('%1.6g' % (x_right[0] - x[index]))) + ']')
            text = text + delta_x
        if error_container.has_yerr:
            error_y = error_container[2][-1].get_paths()[index]
            y_left, y_right = error_y.vertices
            delta_y = ('\nY Delta [' + str_remove_zeros(('%1.6g' % (y_left[1] - y[index])))
                    + ' ' + str_remove_zeros(('%1.6g' % (y_right[1] - y[index]))) + ']')
            text = text + delta_y

        return pos, text

    def area_data_tips(self, c_area, ind, ax, event):
        poly_collection = c_area.poly_collection
        # A[:,setdiff([1:end;],(1,4,8))]
        #获取区域图的上半部分点的数据，拆分为x坐标数据，y坐标数据
        indexes = np.unique(poly_collection.get_paths()[0].vertices,axis=0)
        data = poly_collection.get_paths()[0].vertices

        # 去除无效数据
        data = np.delete(data, 0, 0)
        data = np.delete(data, -1, 0)
        middle = int(len(data)/2)
        data = np.delete(data, middle, 0)

        # 对数据进行处理分类
        indexes_buttom = data[0 : middle]
        indexes_top = data[middle : len(data)][::-1]
        # indexes_top = indexes[1::2]
        # indexes_buttom = indexes[0::2]
        x_data_top = indexes_top[:, 0]
        y_data_top = indexes_top[:, 1]
        x_data_buttom = indexes_buttom[:, 0]
        y_data_buttom = indexes_buttom[:, 1]

        #计算获取的数据点，离鼠标最近的一个点
        xdata, ydata = plt.gca().transData.inverted().transform([event.x, event.y])
        index_right = np.searchsorted(x_data_top, [xdata])[0]
        if index_right >= len(x_data_top):
            index = len(x_data_top) - 1
        else:
            x_right, y_right = ax.transData.transform([x_data_top[index_right], y_data_top[index_right]])
            x_left, y_left = ax.transData.transform([x_data_top[index_right-1], y_data_top[index_right-1]])

            index = index_right if (((x_right - event.x)**2 + (y_right - event.y)**2) <
                ((x_left - event.x)**2 + (y_left - event.y)**2)) else index_right - 1

        c_areas = mw_get_cax(ax).get_all_areas()
        if len(c_areas) > 1:
            pos = (x_data_top[index], y_data_top[index])
            text = ('X ' + str_remove_zeros(str(('%1.6g' % (pos[0]))))
                + '\nY(Stacked) ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
                + '\nY(Segment) ' + str_remove_zeros(str(('%1.6g' % (pos[1] - y_data_buttom[index])))))
        else:
            pos = (x_data_top[index], y_data_top[index])
            text = ('X ' + str_remove_zeros(str(('%1.6g' % (pos[0]))))
                + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1])))))

        return pos, text

    def hist_data_tips(self, c_hist, bar, event):
        if c_hist.category == 'v':
            edge_left = bar.get_x()
            edge_right = bar.get_x() + bar.get_width()
            x = bar.get_x()+bar.get_width()/2
            y = bar.get_y()+bar.get_height()
            pos = (x,y)
            if isinstance(c_hist.ax,PolarAxes):
                text = ('Value ' + str_remove_zeros(str(('%1.6g' % (pos[1])))) + '\nBinEdges ['
                    + str_remove_zeros(str(('%1.6g' % (edge_left))))+' '
                    + str_remove_zeros(str(('%1.6g' % (edge_right))))+']')
            else:
                text = ('Value ' + str_remove_zeros(str(('%1.6g' % (pos[1])))) + '\nBinEdges ['
                    + str_remove_zeros(str(('%1.6g' % (edge_left)))) + ' '
                    + str_remove_zeros(str(('%1.6g' % (edge_right)))) + ']')
                # text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
            return pos, text
        else:
            edge_bottom = bar.get_y()
            edge_top = bar.get_y() + bar.get_height()
            x = bar.get_x()+bar.get_width()
            y = bar.get_y()+bar.get_height()/2
            pos = (x,y)
            if isinstance(c_hist.ax,PolarAxes):
                text = ('Value ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nBinEdges ['
                    + str_remove_zeros(str(('%1.6g' % (edge_bottom)))) + ' '
                    + str_remove_zeros(str(('%1.6g' % (edge_top))))+']')
                # text = 'X ' + str_remove_zeros(str(('%1.6g' % (np.rad2deg(pos[0])%360))))+'°' + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
            else:
                text = ('Value ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nBinEdges ['
                    + str_remove_zeros(str(('%1.6g' % (edge_bottom)))) + ' '
                    + str_remove_zeros(str(('%1.6g' % (edge_top)))) + ']')
                # text = 'X ' + str_remove_zeros(str(('%1.6g' % (pos[0])))) + '\nY ' + str_remove_zeros(str(('%1.6g' % (pos[1]))))
            return pos, text

    def surf_data_tips(self, c_surf, ind, ax, event, press):
        poly_collection = c_surf.poly_collection
        xdata,ydata,zdata,ones = poly_collection._vec
        # print(xdata)
        # print(ydata)
        # print(zdata)
        # print(poly_collection._segment3d)
        # print(poly_collection.get_paths()[ind["ind"][0]])
        segments_3d, codes = art3d._paths_to_3d_segments_with_codes(poly_collection.get_paths())
        #print(segments_3d)
        # print(xdata)
        # print(ind)
        #xdata,ydata,zdata = proj3d._proj_transform_vec(poly_collection._vec, ax.get_proj())
        # x, y, z = xdata[ind["ind"][0]], ydata[ind["ind"][0]], zdata[ind["ind"][0]]
        # pos = (x, y, z)
        # text = str('X ' + str(('%1.6g' % (x)))
        #         + '\nY ' + str(('%1.6g' % (y)))
        #         + '\nZ ' + str(('%1.6g' % (z))))
        # x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
        # if press:
        #     self.create_selection_3d(ax, text, (x2, y2), pos, poly_collection)
        # elif not mw_get_cfig().data_tips:
        #     self.update_hover_selection_3d(ax, text, (x2, y2), pos, poly_collection)

        #text = 'X ' + str(('%1.6g' % (pos[0]))) + '\nY ' + str(('%1.6g' % (pos[1])))
        #return pos, text

    def feather_data_tips(self, feather, index, ax, flag, event):
        x=[]
        y=[]
        if flag == 1:
            x = feather.feather.get_xdata().tolist()
            y = feather.feather.get_ydata().tolist()
        else:
            x = feather.arrow.get_xdata().tolist()
            y = feather.arrow.get_ydata().tolist()

        if index < 0:
            index = 0
        elif index > len(x) - 1:
            index = len(x) - 1
        pos = (x[index], y[index])

        if isinstance(pos[0], (np.number, float)):
            str_x = str_remove_zeros(str(('%1.6g' % (pos[0]))))
        else:
            str_x = str(pos[0])

        if isinstance(pos[1], (np.number, float)):
            str_y = str_remove_zeros(str(('%1.6g' % (pos[1]))))
        else:
            str_y = str(pos[1])

        text = 'X ' + str_x + '\nY ' + str_y

        return text, pos, index

    def quiver_data_tips(self, quiver, ax, event):
        x,y = quiver.quiver.marker.get_data()
        u = quiver.quiver.u
        v =quiver.quiver.v

        #计算最近的一个点
        min = 9999999
        min_index = 0

        for i in range(0,len(x)):
            _x, _y = ax.transData.transform([x[i], y[i]])
            if ((_x - event.x)**2 + (_y - event.y)**2) <min:
                min = (_x - event.x)**2 + (_y - event.y)**2
                min_index = i

        pos_return = (x[min_index], y[min_index])
        pos = (x[min_index], y[min_index],u[min_index],v[min_index])

        if mw_get_cax(ax).is_geomap:
            pos_original = pos
            pos = mw_get_cax(ax).geomap(x[min_index], y[min_index],inverse=True)

        if isinstance(pos[0], (np.number, float)):
            str_x = str_remove_zeros(str(('%1.6g' % (pos[0]))))
        else:
            str_x = str(pos[0])
        if isinstance(pos[1], (np.number, float)):
            str_y = str_remove_zeros(str(('%1.6g' % (pos[1]))))
        else:
            str_y = str(pos[1])

        if isinstance(pos[2], (np.number, float)):
            str_u = str_remove_zeros(str(('%1.6g' % (pos[2]))))
        else:
            str_u = str(pos[2])

        if isinstance(pos[3], (np.number, float)):
            str_v = str_remove_zeros(str(('%1.6g' % (pos[3]))))
        else:
            str_v = str(pos[3])

        text = '[X,Y] [' + str_remove_zeros(str_x) + ' '+ str_y + ']\n' +  '[U,V] [' + str_u + ' '+ str_v + ']'

        return  pos_return,text, min_index

    def on_select(self, sel):
        if self.current_selection != None:
            selection = self.current_selection['value']
            selection['ann'].set_zorder(1e10)
            selection['point'].set_zorder(1e10)

        self.current_selection = sel
        selection = self.current_selection['value']
        selection['ann'].set_zorder(1e10 + 1)
        selection['point'].set_zorder(1e10 + 1)
        # print(selection['ann'].get_zorder())

        # for selection_dict in self.selections:
        #     selection = selection_dict['value']
        #     selection['ann'].set_animated(False)
        self._update()

    def create_selection(self, ax, text, pos, artist = None, index = None, **kwargs):
        if text == None:
            return

        if mw_get_cfig().data_tips and self.current_selection != None and self.current_selection['value']['ann'].axes == ax\
        and self.alt_open == False:
            self.update_current_selection(ax, text, pos, index, artist)
            return

        self.ax = ax
        location = kwargs.pop('location', '')
        if location == '':
            location = 1
        else:
            location = _location[location]

        fontsize = kwargs.pop('fontsize', '')
        if fontsize == '':
            fontsize = 12

        not_change_lst = change_autoscalex(self.ax, auto = False)
        ann = ax.annotate(
            text,
            xy=pos,
            xytext=(0,0),textcoords="offset points",
            horizontalalignment=("left"),
            verticalalignment=("baseline"),
            # visible=True,
            zorder=1e10,
            fontsize = fontsize,
            **_default_annotation_kwargs,
            **kwargs)
        ann.set(**_default_annotation_positions[location])
        fontsize = ann.get_fontsize()
        position_adjust = fontsize*0.5 + 1
        if location == 0:
            ann.set(position=(-position_adjust,position_adjust))
        elif location == 1:
            ann.set(position=(position_adjust,position_adjust))
        elif location == 2:
            ann.set(position=(position_adjust,-position_adjust))
        elif location == 3:
            ann.set(position=(-position_adjust,-position_adjust))
        ann.set_animated(True)
        ann.set_in_layout(False)

        point, = ax.plot([pos[0]], [pos[1]], "o", mfc = 'k', mec = 'w', zorder=1e10)
        point.set_animated(True)
        point.set_in_layout(False)

        selection = dict(index = self.selection_index, value = dict(point = point, ann = ann, artist = artist, index = index))
        self.selection_index = self.selection_index + 1
        self.selections.append(selection)
        if mw_get_cfig().data_tips and self.alt_open == False:
            self.delete_current()
        self.current_selection = selection

        self._update()

        change_autoscalex(self.ax, auto=False,not_change_lst = not_change_lst)
        # self.artist = artist

    def create_selection_3d(self, ax, text, pos_ann, pos_point, artist = None, index = None):
        if text == None:
            return

        if mw_get_cfig().data_tips and self.current_selection != None and self.current_selection['value']['ann'].axes == ax:
            self.update_current_selection_3d(ax, text, pos_ann, pos_point, index, artist)
            return

        self.ax = ax
        not_change_lst = change_autoscalex(self.ax, auto = False)
        ann = ax.annotate(
            text,
            xy=pos_ann,
            xytext=(0,0),textcoords="offset points",
            horizontalalignment=("left"),
            verticalalignment=("baseline"),
            # visible=True,
            zorder=1e10,
            **_default_annotation_kwargs)
        ann.set(**_default_annotation_positions[1])
        ann.set_animated(True)
        ann.set_in_layout(False)

        # point = plot3(ax, [pos_point[0]], [pos_point[1]], [pos_point[2]], "o", mfc = 'k', mec = 'w', zorder=np.inf)
        point, = ax.plot([pos_point[0]], [pos_point[1]], [pos_point[2]], "o", mfc = 'k', mec = 'w', zorder=np.inf)
        # point.set_animated(True)
        point.set_in_layout(False)

        selection = dict(index = self.selection_index, value = dict(point = point, ann = ann, artist = artist, index = index))
        self.selection_index = self.selection_index + 1
        self.selections.append(selection)
        if mw_get_cfig().data_tips:
            self.delete_current()
        self.current_selection = selection

        self._update()

        change_autoscalex(self.ax, not_change_lst = not_change_lst)

    def context_menu(self):
        """初始化右键菜单"""
        menu_list = []

        menu_list.append({"value": "del_datatip", "label": "删除当前数据提示", "children": [], "default_value":""})

        menu_list.append({"value": "delall_datatips", "label": "删除所有数据提示", "children": [], "default_value":""})

        self.fig.canvas.send_event("contextmenu", menu_list=menu_list)



        # self.fig.canvas.send_event("contextmenu", menu_list=menu_list)

        # context_menu = QMenu()

        # action_delete = context_menu.addAction('删除当前数据提示')
        # action_delete_all = context_menu.addAction('删除所有数据提示')

        # action_delete.triggered.connect(self.delete_current)
        # action_delete_all.triggered.connect(self.delete_all)

        # context_menu.exec_(QCursor().pos())

    def delete_current(self):
        print("delete_current")
        if self.current_selection == None:
            return

        if self.current_selection in self.selections:
            self.selections.remove(self.current_selection)

        selection = self.current_selection['value']
        selection['ann'].remove()
        selection['point'].remove()
        self.current_selection = None
        # if not CGlobalSetting.isOnline:
        self.fig.canvas.draw_idle()

    def delete_all(self):
        print("delete_all")
        for selection in self.selections:
            _selection = selection['value']
            _selection['ann'].remove()
            _selection['point'].remove()
        self.selections.clear()
        self.current_selection = None
        self.hover.clear()
        # if not CGlobalSetting.isOnline:
        self.fig.canvas.draw_idle()

    def set_current_selection(self):
        if self.current_selection == None and len(self.selections) > 0:
            self.current_selection = self.selections[0]

    # 更新标签的位置和文本
    def update_current_selection(self, ax, text, pos, index = None, artist = None):
        """
        拖拽或者方向键移动标签
        """
        selection = self.current_selection['value']
        selection_index = self.current_selection['index']
        ann = selection['ann']
        ann.xy = pos
        ann.set_text(text)
        point = selection['point']
        point.set_data(pos[0], pos[1])
        selection['index'] = index
        if artist != None:
            selection['artist'] = artist

        for _selection in self.selections:
            if _selection['index'] == selection_index:
                _selection = self.current_selection
                break

        self._update()

    def update_current_selection_3d(self, ax, text, pos_ann, pos_point, index = None, artist = None):
        selection = self.current_selection['value']
        selection_index = self.current_selection['index']
        ann = selection['ann']
        ann.xy = pos_ann
        ann.set_text(text)
        point = selection['point']
        point.set_data_3d(pos_point[0], pos_point[1], pos_point[2])
        selection['index'] = index
        if artist != None:
            selection['artist'] = artist

        for _selection in self.selections:
            if _selection['index'] == selection_index:
                _selection = self.current_selection
                break

        self._update()

    # 标签右移
    def current_selection_pos_add(self, event):
        """
        键盘右键或下键使标签右移
        """
        if mw_get_cfig() == None:
            return

        if self.current_selection == None:
            if len(self.selections) > 0:
                self.current_selection = self.selections[-1]
            else:
                return

        selection = self.current_selection['value']
        artist = selection['artist']

        if not isinstance(artist, Line2D):
            return

        index = selection['index']
        index = index + 1
        # self.current_selection['index'] = index

        if isinstance(artist, Line2D):
            result = self.line_data_tips(artist, index, plt.gca(), event)
            if len(result) == 4:
                text, pos_pnn, pos_point, index1 = result
                self.update_current_selection_3d(plt.gca(), text, pos_pnn, pos_point, index1)
            else:
                text, pos, index1 = result
                self.update_current_selection(plt.gca(), text, pos, index1)

        #     result = self.line_data_tips(c_line.line, attrd['ind'][0], ax, event)
        #     if len(result) == 4:
        #         text, pos_pnn, pos_point, index = result
        #         self.create_selection_3d(ax, text, pos_pnn, pos_point, c_line.line, index)
        # elif isinstance(artist, Line2D):
        #     text, pos, index1 = self.line_data_tips(artist, index, plt.gca(), event)
        #     self.update_current_selection(plt.gca(), text, pos, index1)
        # elif isinstance(artist, )

    # 标签左移
    def current_selection_pos_sub(self, event):
        """
        键盘左键或上键使标签左移
        """
        if mw_get_cfig() == None:
            return

        if self.current_selection == None:
            if len(self.selections) > 0:
                self.current_selection = self.selections[-1]
            else:
                return

        selection = self.current_selection['value']
        artist = selection['artist']

        if not isinstance(artist, Line2D):
            return

        index = selection['index']
        index = index - 1
        # self.current_selection['index'] = index

        if isinstance(artist, Line2D):
            result = self.line_data_tips(artist, index, plt.gca(), event)
            if len(result) == 4:
                text, pos_pnn, pos_point, index1 = result
                self.update_current_selection_3d(plt.gca(), text, pos_pnn, pos_point, index1)
            else:
                text, pos, index1 = result
                self.update_current_selection(plt.gca(), text, pos, index1)

        # if isinstance(artist, Line2D):
        #     text, pos, index1 = self.line_data_tips(artist, index, plt.gca(), None)
        #     self.update_current_selection(plt.gca(), text, pos, index1)

    def update_hover_selection(self, ax = None, text = None, pos = None, artist = None, index = None):
        if not mw_get_cfig(self.fig).data_tips_on:
            return

        if text == None:
            if self.hover_annotate != None:
                self.hover_annotate.set_visible(False)
            if self.hover_point != None:
                self.hover_point.set_visible(False)
            if self.background == None:
                self.background = self.canvas.copy_from_bbox(self.fig.bbox)
            self._update()
        else:
            if self.hover_annotate == None or not (ax in self.hover.keys()):
                not_change_lst = change_autoscalex(self.ax, auto = False)
                self.hover_annotate = ax.annotate(text,
                                                xy=pos,
                                                xytext=(0,0),textcoords="offset points",
                                                horizontalalignment=("left"),
                                                verticalalignment=("baseline"),
                                                visible=True,
                                                zorder=np.inf,
                                                **_default_annotation_kwargs)
                self.hover_annotate.set(**_default_annotation_positions[1])
                self.hover_annotate.set_animated(True)
                self.hover_annotate.set_in_layout(False)

                self.hover_point, = ax.plot(pos[0], pos[1], "o", mfc = '#808080', mec = 'w', zorder=np.inf)
                self.hover_point.set_animated(True)
                self.hover_point.set_in_layout(False)

                self.hover[ax] = [self.hover_annotate, self.hover_point]

                if self.background == None:
                    self.background = self.canvas.copy_from_bbox(self.fig.bbox)
                self._update()

                change_autoscalex(self.ax, not_change_lst = not_change_lst)
            else:
                if self.hover_annotate.axes == ax:
                    self.hover_annotate.set_visible(True)
                    self.hover_annotate.xy = pos
                    self.hover_annotate.set_text(text)

                    self.hover_point.set_data(pos[0], pos[1])
                    self.hover_point.set_visible(True)
                elif ax in self.hover.keys():
                    self.hover_annotate = self.hover[ax][0]
                    self.hover_annotate.set_visible(True)
                    self.hover_annotate.xy = pos
                    self.hover_annotate.set_text(text)

                    self.hover_point = self.hover[ax][1]
                    self.hover_point.set_visible(True)
                self._update()
            #self._update()

            self.artist = artist

        self.index = index
        #self.fig.canvas.draw_idle()

    def update_hover_selection_3d(self, ax = None, text = None, pos_ann = None, pos_point = None, artist = None, index = None):
        if not mw_get_cfig(self.fig).data_tips_on:
            return

        if text == None:
            if self.hover_annotate != None:
                self.hover_annotate.set_visible(False)
            if self.hover_point != None:
                self.hover_point.set_visible(False)
            if self.background == None:
                self.background = self.canvas.copy_from_bbox(self.fig.bbox)
            self._update()
        else:
            if self.hover_annotate == None or not (ax in self.hover.keys()):
                not_change_lst = change_autoscalex(self.ax, auto = False)
                self.hover_annotate = ax.annotate(text,
                                                xy=pos_ann,
                                                xytext=(0,0),textcoords="offset points",
                                                horizontalalignment=("left"),
                                                verticalalignment=("baseline"),
                                                visible=True,
                                                zorder=np.inf,
                                                **_default_annotation_kwargs)
                self.hover_annotate.set(**_default_annotation_positions[1])
                self.hover_annotate.set_animated(True)
                self.hover_annotate.set_in_layout(False)

                self.hover_point = plot3(ax, [pos_point[0]], [pos_point[1]], [pos_point[2]], "o", mfc = '#808080', mec = 'w', zorder=np.inf)
                # self.hover_point.set_animated(True)
                self.hover_annotate.set_in_layout(False)
                self.hover[ax] = [self.hover_annotate, self.hover_point]
                self._update()

                change_autoscalex(self.ax, not_change_lst = not_change_lst)
            else:
                if self.hover_annotate.axes == ax:
                    self.hover_annotate.set_visible(True)
                    self.hover_annotate.xy = pos_ann
                    self.hover_annotate.set_text(text)

                    self.hover_point.set_data_3d(pos_point[0], pos_point[1], pos_point[2])
                    self.hover_point.set_visible(True)
                elif ax in self.hover.keys():
                    self.hover_annotate = self.hover[ax][0]
                    self.hover_annotate.set_visible(True)
                    self.hover_annotate.xy = pos_ann
                    self.hover_annotate.set_text(text)

                    self.hover_point = self.hover[ax][1]
                    self.hover_point.set_data_3d(pos_point[0], pos_point[1], pos_point[2])
                    self.hover_point.set_visible(True)

                self._update()
            self.artist = artist

        self.index = index
        #self.fig.canvas.draw_idle()

    def _update(self):
        # update_all(self.fig)
        self.fig.canvas.draw_idle()

        # if self.background is not None:
        #     self.canvas.restore_region(self.background)

        # self.draw_self()

        # # 处理多轴情况下游标和数据提示都存在的情况
        # # 在刷新数据提示时，也需要刷新游标对象
        # for i in range(0, mw_get_cfig().cursor_lines.__len__())[::-1]:
        #     cursor_line = mw_get_cfig().cursor_lines[i]
        #     cursor_line.draw_self()

        # for i in range(0, mw_get_cfig().draw_lines.__len__())[::-1]:
        #     dline = mw_get_cfig().draw_lines[i]
        #     dline.draw_self()

        # self.canvas.blit(self.fig.bbox)


def mw_datatip_pos(target, x, y, z = None, **kwargs):
    kwargs_snaptodatavertex = kwargs.pop('dataindex', '')
    if kwargs_snaptodatavertex == '':
        kwargs_snaptodatavertex = 'on'
    snaptodatavertex = True if kwargs_snaptodatavertex == 'on' else False

    if isinstance(target,list):
        target = target[0]

    data_tip = mw_get_cfig().current_mplcursor
    if isinstance(target, PathCollection):
        datas = target.get_offsets()

        target_pos = None
        min_distance = np.inf
        for data_pos in datas:
            distance = (x - data_pos[0])**2 + (y - data_pos[1])**2
            if distance == 0:
                target_pos = data_pos
                break
            elif distance < min_distance:
                target_pos = data_pos
                min_distance = distance

        text = data_tip.scatter_pos2text(target.axes, target_pos)
        data_tip.create_selection(target.axes, text, target_pos, **kwargs)
    elif isinstance(target, Line2D):
        datas_x = target.get_xdata()
        if isinstance(target, Line3D):
            dataindex = get_line_dataindex(target, x, y, z)
        else:
            dataindex = get_line_dataindex(target, x, y)
        result = data_tip.line_data_tips(target, dataindex, target.axes, None)
        if len(result) == 4:
            text, pos_pnn, pos_point, index = result
            data_tip.create_selection_3d(target.axes, text, pos_pnn, pos_point, target, index, **kwargs)
        else:
            text, pos, index = result
            data_tip.create_selection(target.axes, text, pos, target, index, **kwargs)
    elif isinstance(target, tuple) and len(target) > 0:
        # 先判断类型
        obj = target[0]
        if mw_get_cbar(target) != None:
            # 条形图
            c_bar = mw_get_cbar(target)
            if len(c_bar.ticks) >= len(c_bar.bars):
                ticks = c_bar.ticks
            else:
                if c_bar.category == 'v':
                    ticks = c_bar.ax.get_xticks()
                else:
                    ticks = c_bar.ax.get_yticks()

            target_pos = None
            target_text = None
            target_bar = None
            min_distance = np.inf
            create = False
            for bar, tick in zip(c_bar.bars, ticks):
                pos, text, bar = data_tip.bar_get_pos(c_bar, bar, tick)

                if c_bar.category == 'v':
                    distance = x - pos[0]
                else:
                    distance = y - pos[1]

                if distance < 0:
                    create = True
                    if abs(distance) > min_distance:
                        data_tip.create_selection(c_bar.ax, target_text, target_pos, target_bar, **kwargs)
                    else:
                        data_tip.create_selection(c_bar.ax, text, pos, bar, **kwargs)
                    break
                else:
                    target_pos = pos
                    target_text = text
                    target_bar = bar
                    min_distance = distance

            if not create:
                data_tip.create_selection(c_bar.ax, target_text, target_pos, target_bar, **kwargs)
        elif mw_get_cstem(target) != None:
            # 针状图
            c_stem = mw_get_cstem(target)
            markerline = c_stem.markerline
            datas_x = markerline.get_xdata()

            if isinstance(c_stem.ax, Axes3D):
                dataindex = get_line_dataindex(markerline, x, y, z)
            else:
                dataindex = get_nearest_index(datas_x, x)
            pos_2d,pos_3d,text = data_tip.stem_data_tips(c_stem, dataindex, c_stem.ax, None)
            if pos_3d is not None:
                data_tip.create_selection_3d(c_stem.ax, text, pos_2d, pos_3d, **kwargs)
            else:
                data_tip.create_selection(c_stem.ax, text, pos_2d, **kwargs)
        elif mw_get_cerrorbar(target) != None:
            c_errorbar = mw_get_cerrorbar(target)
            data_line = c_errorbar.data_line
            dataindex = get_line_dataindex(data_line, x, y)
            pos, text = data_tip.errorbar_data_tips(c_errorbar, dataindex, None)
            data_tip.create_selection(c_errorbar.ax, text, pos, **kwargs)
        elif mw_get_chistogram(target) != None:
            c_hist = mw_get_chistogram(target)

            dataindex = 0
            create = False
            min_distance = np.inf
            for i in range(0, len(c_hist.bars)):
                bar = c_hist.bars[i]
                pos, text, bar = data_tip.bar_get_pos(c_hist, bar)

                if c_hist.category == 'v':
                    distance = x - pos[0]
                else:
                    distance = y - pos[1]

                if distance < 0:
                    create = True
                    if abs(distance) > min_distance:
                        pos, text = data_tip.hist_data_tips(c_hist, c_hist.bars[dataindex], None)
                        data_tip.create_selection(c_hist.ax, text, pos, **kwargs)
                    else:
                        pos, text = data_tip.hist_data_tips(c_hist, c_hist.bars[i], None)
                        data_tip.create_selection(c_hist.ax, text, pos, **kwargs)
                    break
                else:
                    dataindex = i
                    min_distance = distance

            if not create:
                pos, text = data_tip.hist_data_tips(c_hist, c_hist.bars[dataindex], None)
                data_tip.create_selection(c_hist.ax, text, pos, **kwargs)

def mw_datatip(target, **kwargs):
    dataindex = kwargs.pop('dataindex', '')
    if dataindex == '':
        dataindex = 0

    dataindex = dataindex - 1
    if dataindex < 0:
        return

    if isinstance(target,list):
        target = target[0]

    data_tip = mw_get_cfig().current_mplcursor
    if isinstance(target, PathCollection):
        datas = target.get_offsets()
        if dataindex > len(datas):
            dataindex = len(datas) - 1

        pos = datas[dataindex]

        text = data_tip.scatter_pos2text(target.axes, pos)
        data_tip.create_selection(target.axes, text, pos, **kwargs)
    elif isinstance(target, Line2D):
        datas_x = target.get_xdata()
        if dataindex > len(datas_x):
            dataindex = len(datas_x) - 1

        result = data_tip.line_data_tips(target, dataindex, target.axes, None)
        if len(result) == 4:
            text, pos_pnn, pos_point, index = result
            data_tip.create_selection_3d(target.axes, text, pos_pnn, pos_point, target, index, **kwargs)
        else:
            text, pos, index = result
            data_tip.create_selection(target.axes, text, pos, target, index, **kwargs)
    elif isinstance(target, tuple) and len(target) > 0:
        # 先判断类型
        if mw_get_cbar(target) != None:
            # 条形图
            c_bar = mw_get_cbar(target)
            if len(c_bar.ticks) >= len(c_bar.bars):
                ticks = c_bar.ticks
            else:
                if c_bar.category == 'v':
                    ticks = c_bar.ax.get_xticks()
                else:
                    ticks = c_bar.ax.get_yticks()

            if dataindex > len(c_bar.bars):
                dataindex = len(c_bar.bars) - 1

            tick = ticks[dataindex]
            bar = c_bar.bars[dataindex]
            pos, text, bar = data_tip.bar_get_pos(c_bar, bar, tick)
            data_tip.create_selection(c_bar.ax, text, pos, bar, **kwargs)
        elif mw_get_cstem(target) != None:
            # 针状图
            c_stem = mw_get_cstem(target)
            pos_2d,pos_3d,text = data_tip.stem_data_tips(c_stem, dataindex, c_stem.ax, None)
            if pos_3d is not None:
                data_tip.create_selection_3d(c_stem.ax, text, pos_2d, pos_3d, **kwargs)
            else:
                data_tip.create_selection(c_stem.ax, text, pos_2d, **kwargs)
        elif mw_get_cerrorbar(target) != None:
            # 误差图
            c_errorbar = mw_get_cerrorbar(target)
            pos, text = data_tip.errorbar_data_tips(c_errorbar, dataindex, None)
            data_tip.create_selection(c_errorbar.ax, text, pos, **kwargs)
        elif mw_get_chistogram(target) != None:
            c_hist = mw_get_chistogram(target)
            bar = c_hist.bars[dataindex]
            pos, text = data_tip.hist_data_tips(c_hist, bar, None)
            data_tip.create_selection(c_hist.ax, text, pos, **kwargs)

def get_line_dataindex(line, x, y, z = None):
    if isinstance(line, Line3D):
        datas_x, datas_y, datas_z = line.get_data_3d()
        # x_pixels,y_pixels = line.axes.transData.transform((x,y))
        # x_pixels,z_pixels = line.axes.transData.transform((x,z))
        # y = line.axes.transData.transform((y))
        # z = line.axes.transData.transform((z))
        # x,y,z = line.axes.transData.transform((x, y, z))

        dataindex = 0
        min_distance = np.inf
        for i in range(0, len(datas_x)):
            data_x = datas_x[i]
            data_y = datas_y[i]
            data_z = datas_z[i]
            # data_x, data_y = line.axes.transData.transform((datas_x[i], datas_y[i]))
            # data_x, data_z = line.axes.transData.transform((datas_x[i], datas_z[i]))
            # data_y = line.axes.transData.transform((datas_y[i]))
            # data_z = line.axes.transData.transform((datas_z[i]))
            distance = (x - data_x)**2 + (y - data_y)**2 + (z - data_z)**2
            if distance == 0:
                dataindex = i
                break
            elif distance < min_distance:
                dataindex = i
                min_distance = distance

        return dataindex
    else:
        datas_x, datas_y = line.get_data()

        dataindex = 0
        min_distance = np.inf
        for i in range(0, len(datas_x)):
            data_x = datas_x[i]
            data_y = datas_y[i]
            distance = (x - data_x)**2 + (y - data_y)**2
            if distance == 0:
                dataindex = i
                break
            elif distance < min_distance:
                dataindex = i
                min_distance = distance

        return dataindex

def get_nearest_index(datas, pos):
    min_distance = np.inf
    for i in range(0, len(datas)):
        data = datas[i]
        distance = pos - data
        if distance < 0:
            if abs(distance) > min_distance:
                return i - 1
            else:
                return i
        else:
            min_distance = distance

    return len(datas) - 1
