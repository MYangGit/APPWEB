from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
from TyPlotOnline.objects.mw_axes_pareto import CAxesPareto
from matplotlib.offsetbox import AuxTransformBox
from matplotlib.offsetbox import HPacker, VPacker, TextArea, DrawingArea
from matplotlib.patches import Shadow
from matplotlib.backend_bases import MouseButton

from TyPlotOnline.objects.mw_interface import *

class CLegend(object):
    def __init__(self, legend):
        self.legend = legend
        # self.legend.set_animated(True)
        self.axes = self.legend.axes
        self.figure = self.legend.figure
        # self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)
        self.picked = False
        self.dir='va'
        self.handles,self.labels=self.axes.get_legend_handles_labels()
        self.press = False
        self.block = False
        self.self_picked = False


        if len(self.legend.texts) > 0:
            text_font_tuple = (self.legend.texts[0].get_fontname(), self.legend.texts[0].get_fontsize(),
                        True if self.legend.texts[0].get_fontstyle() == 'italic' else False,
                        True if self.legend.texts[0].get_fontweight() == 'bold' else False)
            self.text_fontdict = tuple_to_fontdict(text_font_tuple)
            self.text_color=self.legend.texts[0].get_color()
        else:
            self.text_fontdict = None
            self.text_color = None

        self.create_pick_state()

        self.legend.draw = self.draw

        self.connect()

    def create_pick_state(self):
        '''
        初始化选中状态边框
        '''
        self.box = AuxTransformBox(self.figure.get_transform())
        self.picker_point = [(0,0),(0,0),(0,0),(0,0)]
        picker_point_x, picker_point_y=[0,0,0,0],[0,0,0,0]
        self.pick_state = Line2D(picker_point_x, picker_point_y, marker = 's', clip_on = False, linestyle = 'none',
            markersize=6,markeredgecolor='#005a96',markerfacecolor='#7ce1f785')

        #self.set_pickbox_pos()

        self.pick_state.set_visible(False)
        # self.pick_state.set_animated(True)

        self.box.set_zorder(6)
        self.box.add_artist(self.pick_state)
        self.axes.figure.add_artist(self.box)

    def set_pickbox_pos(self,event=None):
        '''计算边框中四个点的位置'''
        bbox = self.legend.get_window_extent()

        picker_point_x = [bbox.x0,bbox.x0,bbox.x1,bbox.x1]
        picker_point_y = [bbox.y0,bbox.y1,bbox.y0,bbox.y1]

        self.pick_state.set_data(picker_point_x,picker_point_y)

    def pick_self(self, pick_only = False):
        """选中状态"""
        self.pick_state.set_visible(True)
        self.figure.canvas.draw_idle()
        self.picked = True
        if not pick_only:
            mw_get_cfig().current_objs.append(self)

    def dis_pick_self(self):
        """取消选中状态"""
        self.pick_state.set_visible(False)
        self.figure.canvas.draw_idle()
        self.picked = False

    def contains_self(self, event):
        contains, attrd = self.legend.contains(event)
        return contains

    # def on_press(self):
    #     if not mw_get_cfig().edit_mode:
    #         return

    #     if not self.picked:
    #         mw_clear_status()
    #         self.pick_self()

    #重新计算legend_box(横向)
    def _init_legend_box_ha(self,ncol,handles, labels, markerfirst=True):
        """
        重新计算legend_box(横向)
        源码为legend类中的_init_legend_box函数
        """
        self.legend._ncol=ncol
        fontsize = self.legend._fontsize

        text_list = []  # the list of text instances
        handle_list = []  # the list of text instances
        handles_and_labels = []

        label_prop = dict(verticalalignment='baseline',
                          horizontalalignment='left',
                          fontproperties=self.legend.prop,
                          )

        descent = 0.35 * fontsize * (self.legend.handleheight - 0.7)
        height = fontsize * self.legend.handleheight - descent
        legend_handler_map = self.legend.get_legend_handler_map()

        handles_ha=[]
        labels_ha=[]
        for i in range(ncol):
            j=i
            while True:
                handles_ha.append(handles[j])
                labels_ha.append(labels[j])
                j+=ncol
                if j >= len(handles):
                    break

        for orig_handle, lab in zip(handles_ha, labels_ha):
            handler = self.legend.get_legend_handler(legend_handler_map, orig_handle)
            if handler is None:
                cbook._warn_external(
                    "Legend does not support {!r} instances.\nA proxy artist "
                    "may be used instead.".format(orig_handle))
                handle_list.append(None)
            else:
                textbox = TextArea(lab, textprops=label_prop,
                                   multilinebaseline=True,
                                   minimumdescent=True)
                handlebox = DrawingArea(width=self.legend.handlelength * fontsize,
                                        height=height,
                                        xdescent=0., ydescent=descent)

                text_list.append(textbox._text)
                handle_list.append(handler.legend_artist(self.legend, orig_handle,
                                                         fontsize, handlebox))
                handles_and_labels.append((handlebox, textbox))

        if handles_and_labels:
            ncol = min(self.legend._ncol, len(handles_and_labels))
            nrows, num_largecol = divmod(len(handles_and_labels), ncol)
            num_smallcol = ncol - num_largecol
            rows_per_col = [nrows + 1] * num_largecol + [nrows] * num_smallcol
            start_idxs = np.concatenate([[0], np.cumsum(rows_per_col)[:-1]])
            cols = zip(start_idxs, rows_per_col)

        else:
            cols = []

        columnbox = []
        for i0, di in cols:
            itemBoxes = [HPacker(pad=0,
                                 sep=self.legend.handletextpad * fontsize,
                                 children=[h, t] if markerfirst else [t, h],
                                 align="baseline")
                         for h, t in handles_and_labels[i0:i0 + di]]
            if markerfirst:
                itemBoxes[-1].get_children()[1].set_minimumdescent(False)
            else:
                itemBoxes[-1].get_children()[0].set_minimumdescent(False)

            alignment = "baseline" if markerfirst else "right"
            columnbox.append(VPacker(pad=0,
                                     sep=self.legend.labelspacing * fontsize,
                                     align=alignment,
                                     children=itemBoxes))

        mode = "expand" if self.legend._mode == "expand" else "fixed"
        sep = self.legend.columnspacing * fontsize
        self.legend._legend_handle_box = HPacker(pad=0,
                                          sep=sep, align="baseline",
                                          mode=mode,
                                          children=columnbox)
        self.legend._legend_title_box = TextArea("")
        self.legend._legend_box = VPacker(pad=self.legend.borderpad * fontsize,
                                   sep=self.legend.labelspacing * fontsize,
                                   align="center",
                                   children=[self.legend._legend_title_box,
                                             self.legend._legend_handle_box])
        self.legend._legend_box.set_figure(self.legend.figure)
        self.legend.texts = text_list
        self.legend.legendHandles = handle_list
        self.legend.stale = True

    #重新计算legend_box(纵向)
    def _init_legend_box_va(self,ncol,handles, labels, markerfirst=True):
        """
        重新计算legend_box(纵向)
        源码为legend类中的_init_legend_box函数
        """
        self.legend._ncol=ncol
        fontsize = self.legend._fontsize


        text_list = []  # the list of text instances
        handle_list = []  # the list of text instances
        handles_and_labels = []

        label_prop = dict(verticalalignment='baseline',
                          horizontalalignment='left',
                          fontproperties=self.legend.prop,
                          )


        descent = 0.35 * fontsize * (self.legend.handleheight - 0.7)
        height = fontsize * self.legend.handleheight - descent
        legend_handler_map = self.legend.get_legend_handler_map()

        for orig_handle, lab in zip(handles, labels):
            handler = self.legend.get_legend_handler(legend_handler_map, orig_handle)
            if handler is None:
                cbook._warn_external(
                    "Legend does not support {!r} instances.\nA proxy artist "
                    "may be used instead.".format(orig_handle))
                handle_list.append(None)
            else:
                textbox = TextArea(lab, textprops=label_prop,
                                   multilinebaseline=True,
                                   minimumdescent=True)
                handlebox = DrawingArea(width=self.legend.handlelength * fontsize,
                                        height=height,
                                        xdescent=0., ydescent=descent)

                text_list.append(textbox._text)
                handle_list.append(handler.legend_artist(self.legend, orig_handle,
                                                         fontsize, handlebox))
                handles_and_labels.append((handlebox, textbox))

        if handles_and_labels:
            ncol = min(self.legend._ncol, len(handles_and_labels))
            nrows, num_largecol = divmod(len(handles_and_labels), ncol)
            num_smallcol = ncol - num_largecol
            rows_per_col = [nrows + 1] * num_largecol + [nrows] * num_smallcol
            start_idxs = np.concatenate([[0], np.cumsum(rows_per_col)[:-1]])
            cols = zip(start_idxs, rows_per_col)
        else:
            cols = []

        columnbox = []
        for i0, di in cols:
            itemBoxes = [HPacker(pad=0,
                                 sep=self.legend.handletextpad * fontsize,
                                 children=[h, t] if markerfirst else [t, h],
                                 align="baseline")
                         for h, t in handles_and_labels[i0:i0 + di]]
            if markerfirst:
                itemBoxes[-1].get_children()[1].set_minimumdescent(False)
            else:
                itemBoxes[-1].get_children()[0].set_minimumdescent(False)

            alignment = "baseline" if markerfirst else "right"
            columnbox.append(VPacker(pad=0,
                                     sep=self.legend.labelspacing * fontsize,
                                     align=alignment,
                                     children=itemBoxes))

        mode = "expand" if self.legend._mode == "expand" else "fixed"
        sep = self.legend.columnspacing * fontsize
        self.legend._legend_handle_box = HPacker(pad=0,
                                          sep=sep, align="baseline",
                                          mode=mode,
                                          children=columnbox)
        self.legend._legend_title_box = TextArea("")
        self.legend._legend_box = VPacker(pad=self.legend.borderpad * fontsize,
                                   sep=self.legend.labelspacing * fontsize,
                                   align="center",
                                   children=[self.legend._legend_title_box,
                                             self.legend._legend_handle_box])
        self.legend._legend_box.set_figure(self.legend.figure)
        self.legend.texts = text_list
        self.legend.legendHandles = handle_list
        self.legend.stale = True

    #重写draw
    def draw(self, renderer):
        '''
        加入选中框的位置刷新
        '''
        # docstring inherited
        if not self.legend.get_visible():
            return

        renderer.open_group('legend', gid=self.legend.get_gid())

        fontsize = renderer.points_to_pixels(self.legend._fontsize)

        # if mode == fill, set the width of the legend_box to the
        # width of the parent (minus pads)
        if self.legend._mode in ["expand"]:
            pad = 2 * (self.legend.borderaxespad + self.legend.borderpad) * fontsize
            self.legend._legend_box.set_width(self.legend.get_bbox_to_anchor().width - pad)

        # update the location and size of the legend. This needs to
        # be done in any case to clip the figure right.
        bbox = self.legend._legend_box.get_window_extent(renderer)
        self.legend.legendPatch.set_bounds(bbox.x0, bbox.y0, bbox.width, bbox.height)
        self.legend.legendPatch.set_mutation_scale(fontsize)

        if self.legend.shadow:
            Shadow(self.legend.legendPatch, 2, -2).draw(renderer)

        self.legend.legendPatch.draw(renderer)
        self.legend._legend_box.draw(renderer)
        self.set_pickbox_pos()

        renderer.close_group('legend')
        self.legend.stale = False

    #获取frame位置
    def get_frame_xy(self):
        return (self.legend.get_frame().get_x(),self.legend.get_frame().get_y())

    #设置frame位置
    def set_frame_xy(self,xy):
        self.legend._set_loc(xy)

    def context_menu(self):
        '''
        右键菜单
        '''
        # Online 暂不支持
        pass

    def action_edgewidth(self):
        '''边框宽度'''
        action = QAction()
        sender = action.sender()
        linewidth = float(sender.text())
        self.legend.legendPatch.set_linewidth(linewidth)
        self.legend.figure.canvas.draw()

    def action_ncol(self):
        '''列数'''
        action = QAction()
        sender = action.sender()
        ncol=int(sender.text())
        self.set_ncol(ncol,dir=self.dir)

    def action_loc(self):
        action = QAction()
        sender = action.sender()
        for i in range(5):
            if self.dic_loc[i]==sender.text():
                loc=i
        self.legend._set_loc(loc)

    def action_delete(self):
        # mw_clear_status()
        mw_legend(self.axes,display='off')
        # mw_get_cfig().pick_self()

    def action_edit_title(self):
        self.title_edit=DlgLegendTitle(self,self.legend.get_title())
        self.title_edit.show()

    def action_face_color(self):
        background_color='none'
        if not self.legend.legendPatch is None:
            tuple_background_color = self.legend.legendPatch.get_facecolor()
            background_color = color_to_qcolor(tuple_background_color)
            if tuple_background_color[3]==0.0:
                background_color='none'
        dlg_color = DlgColor(background_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            self.legend.legendPatch.update(dict(facecolor=select_color))

        self.legend.figure.canvas.draw()

    def action_edge_color(self):
        edge_color='none'
        if not self.legend.legendPatch is None:
            tuple_edge_color = self.legend.legendPatch.get_edgecolor()
            edge_color = color_to_qcolor(tuple_edge_color)
            if tuple_edge_color[3]==0.0:
                edge_color='none'
        dlg_color = DlgColor(edge_color)
        if dlg_color.exec_() == QDialog.Accepted:
            select_color = dlg_color.get_color().name()
            self.legend.legendPatch.update(dict(edgecolor=select_color))

        self.legend.figure.canvas.draw()

    def action_font(self):
        '''设置字体动作'''
        if len(self.legend.texts) == 0:
            return

        self.font=DlgLegendFont(self.legend,self.legend.texts[0])
        self.font.show()

    def action_prop(self):
        '''打开属性面板'''
        from TyPlotOnline.settings.mw_setting_base import CPropertySetting
        prop_dlg = CPropertySetting()
        prop_dlg.add_tabs([[self.figure], [self.axes], [self.legend]])
        prop_dlg.set_current_index(2)
        prop_dlg.connect()
        prop_dlg.exec_()

    def action_dir(self):
        action = QAction()
        sender = action.sender()
        dir = sender.text()
        if dir == '垂直':
            if self.legend._ncol == len(self.labels):
                self.legend._ncol = 1
            self.dir = 'va'
            self.set_ncol(self.legend._ncol,dir=self.dir)
        elif dir == '水平':
            if self.legend._ncol == 1:
                self.legend._ncol = len(self.labels)
            self.dir = 'ha'
            self.set_ncol(self.legend._ncol,dir=self.dir)

    #设置图例中元素的排列方向
    def set_dir(self,dir):
        '''
        设置排列方向
        '''
        if dir == 'ha' :
            if self.legend._ncol == 1:
                self.legend._ncol = len(self.labels)
            self.dir = 'ha'
            self.set_ncol(self.legend._ncol,dir=self.dir)
        if dir == 'va':
            if self.legend._ncol == len(self.labels):
                self.legend._ncol = 1
            self.dir = 'va'
            self.set_ncol(self.legend._ncol,dir=self.dir)

    #设置图例列数
    def set_ncol(self,ncol=None,dir=None):
        #TODO:图例中所有元素的label均为空时,调用该函数会报错
        '''
        设置列数
        '''
        if dir == None:
            dir=self.dir
        if ncol == None:
            ncol=self.legend._ncol

        if isinstance(mw_get_cax(self.axes), CAxesPareto):
            self.handles,self.labels = mw_get_cax(self.axes)._get_legend_handles_labels()
        elif isinstance(mw_get_cax(self.axes), CAxesYyaxis):
            self.handles,self.labels = mw_get_cax(self.axes)._get_legend_handles_labels()
        else:
            self.handles,self.labels=self.axes.get_legend_handles_labels()
        if len(self.handles) != 0:
            # 根据曲线的 zorder 属性对曲线图例进行排序
            sorted_legend_items = sorted(zip(self.handles, self.labels), key=lambda item: (item[0].zorder if hasattr(item[0], 'zorder') else item[0][0].zorder))
            # 解压排序后的曲线和标签
            self.handles, self.labels = zip(*sorted_legend_items)
            # 更新图例
            self.legend = self.axes.legend(self.handles, self.labels)
        if dir == 'va':
            self._init_legend_box_va(ncol,self.handles,self.labels)
        elif dir == 'ha':
            self._init_legend_box_ha(ncol,self.handles,self.labels)

        if len(self.legend.texts) > 0:
            text_font_tuple = (self.legend.texts[0].get_fontname(), self.legend.texts[0].get_fontsize(),
                        True if self.legend.texts[0].get_fontstyle() == 'italic' else False,
                        True if self.legend.texts[0].get_fontweight() == 'bold' else False)
            text_fontdict = tuple_to_fontdict(text_font_tuple)
            self.text_fontdict = text_fontdict
            text_color=self.legend.texts[0].get_color()
            self.text_color = text_color
        elif self.text_fontdict != None:
            text_fontdict = self.text_fontdict
            text_color = self.text_color
        else:
            # 此处考虑到图例内容一开始是下划线的情况，这种情况下图例是个小方框，不满足上述分支
            # 如果图例是先正常内容再转为下划线，这种情况由于self.text_fontdict不为None，
            # 因此不进当前分支
            text_fontdict = None
            text_color = None

        title=self.legend.get_title()
        title_color = title.get_color()
        title_font_tuple = (title.get_fontname(), title.get_fontsize(),
                    True if title.get_fontstyle() == 'italic' else False,
                    True if title.get_fontweight() == 'bold' else False)
        title_fontdict = tuple_to_fontdict(title_font_tuple)


        self.legend.set_title(title.get_text(),title_fontdict)
        self.legend.get_title().set_color(title_color)

        if text_fontdict is not None and text_color is not None:
            for text in self.legend.texts:
                text.update(text_fontdict)
                text.set_color(text_color)
        self.legend._set_loc(self.legend._loc_real)

        #解决在属性面板调用改函数后,拖动出现bug的问题 bug原因未知
        # self.set_draggable(False)
        # self.set_draggable(True)

    #刷新图例中的元素
    def update_handels_and_labels_by_axes(self):
        self.set_ncol(self.legend._ncol)

    def connect(self):
        # self.press_id = self.figure.canvas.mpl_connect(
        #     'button_press_event', self.on_press)
        self.move_id = self.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_move)
        self.release_id = self.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        # self.draw_id = self.figure.canvas.mpl_connect(
        #     'draw_event', self.on_draw)

    def on_release(self, event):
        if not self.press:
            return

        self.press = False
        self.block = False
        self.self_picked = False
        mw_get_cfig().current_mplcursor.checked_tool_num -= 1

    def on_move(self, event):
        if not self.press:
            return

        dx = event.x - self.pos_x
        dy = event.y - self.pos_y
        self.legend._set_loc(mw_display_to_axes(self.axes, (self.start_pos[0] + dx, self.start_pos[1] + dy)))
        self.figure.canvas.draw_idle()
        #self._update()

    def on_press(self, event = None):
        if not self.picked and mw_get_cfig().edit_mode:
            mw_clear_status()
            self.pick_self()

        self.self_picked = True

        if event is None:
            return

        if self.block:
            return

        if event.button is MouseButton.RIGHT:
            return

        if not self.contains_self(event):
            return

        mw_get_cfig().current_mplcursor.checked_tool_num += 1

        self.press = True
        self.block = True
        self.pos_x = event.x
        self.pos_y = event.y
        self.start_pos = (self.legend.get_frame().get_x(), self.legend.get_frame().get_y())

    # def on_draw(self,event):
    #     '''用于动画效果'''
    #     self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)

    #     if self.background != None:
    #         self.figure.canvas.restore_region(self.background)

    #     self.axes.draw_artist(self.legend)
    #     self.axes.draw_artist(self.pick_state)

    # def _update(self):
    #     '''用于动画效果'''
    #     if self.background is not None:
    #         self.figure.canvas.restore_region(self.background)

    #     self.axes.draw_artist(self.legend)
    #     self.figure.draw_artist(self.pick_state)
    #     self.figure.canvas.blit(self.figure.bbox)

    def draw_self(self):
        self.axes.draw_artist(self.legend)
        self.figure.draw_artist(self.pick_state)

    def delete_self(self):
        if self.pick:
            self.dis_pick_self()
            if self in mw_get_cfig().current_objs:
                mw_get_cfig().current_objs.remove(self)
            mw_get_cfig().pick_self()

        mw_get_cax(self.ax).legends.remove(self)
        self.legend.remove()

# #字体属性对话框
# class DlgLegendFont(DlgFont):
#     '''字体设置对话框'''
#     def __init__(self, legend, text,parent = None):
#          self.legend=legend
#          super(DlgLegendFont,self).__init__(text,parent)

#     def init_font_panel(self,text,font_tuple):
#         self.font_layout = DlgLegendFontPanel(self.legend, text, font_tuple)
# #字体属性Layout
# class DlgLegendFontPanel(DlgFontPanel):
#     def __init__(self,legend, text, font):
#         self.legend = legend
#         super().__init__(text, font)

#     def update_font(self):
#         '''更新标题字体设置'''
#         font = self.get_font()
#         style = 'italic' if font[2] else 'normal'
#         weight = 'bold' if font[3] else 'normal'
#         fontdict={'family':font[0],'size': font[1], 'weight' : weight, 'style' : style}
#         for text in self.legend.texts:
#             text.update(fontdict)

#         self.legend.get_title().update(fontdict)
#         self.legend.figure.canvas.draw()
# #标题属性对话框
# class DlgLegendTitle(DlgText):
#     '''标题文本设置对话框'''
#     def __init__(self, legend, text, parent = None):
#         self.legend = legend
#         self.text=text
#         super().__init__(text, parent=parent)

#     def init_text_layout(self):
#         self.text_layout = DlgLegendTitlePanel(self.legend, self.text)
# #标题属性Layout
# class DlgLegendTitlePanel(DlgTextPanel):
#     def __init__(self, clegend, text):
#         self.clegend=clegend
#         super().__init__(text)

#     def update_text(self):
#         '''更新标题文本设置'''
#         self.clegend.legend.set_title(self.preview.displayText())

