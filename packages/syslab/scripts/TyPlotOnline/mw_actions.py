from TyPlotOnline.objects.mw_interface import *
from matplotlib.backend_bases import _Mode
from TyPlotOnline.objects.mw_cursor_line import mw_cursor
from TyPlotOnline.data_tips.data_tips import Cursor
from TyPlotOnline.mw_draw_graphics import *

def exit_pan_zoom(figure):
    canvas = figure.canvas
    toolbar = canvas.manager.toolbar

    modename = toolbar.mode.name
    if modename != "NONE":
        mw_get_cfig(figure).current_mplcursor.checked_tool_num -= 1

    toolbar.mode = _Mode.NONE
    canvas.widgetlock.release(toolbar)
    toolbar.set_message(toolbar.mode)
    canvas.send_event('navigate_mode', mode=toolbar.mode.name)

# grid
def action_grid():
    cax = mw_get_cax()
    if cax.grid:
        action_grid_disable(cax)
    else:
        action_grid_enable(cax)

    cax.fig.canvas.send_event("property_update", key="Axes", child_key = "Grids", value = cax.get_prop_grids())

def action_grid_enable(cax):
    set_grid(cax.fig, cax.ax, True)
    cax.fig.canvas.send_event("toolbar_update", action="Grid", active=True, disabled=False)
    cax.grid = True

def action_grid_disable(cax):
    set_grid(cax.fig, cax.ax, False)
    cax.fig.canvas.send_event("toolbar_update", action="Grid", active=False, disabled=False)
    cax.grid = False

def set_grid(fig, ax, state):
    mw_grid(ax, 'on' if state else 'off')
    fig.canvas.draw_idle()


# legend
def action_legend():
    cax = mw_get_cax()
    if cax.legend:
        action_legend_disable(cax)
    else:
        action_legend_enable(cax)

def action_legend_enable(cax):
    cax.fig.canvas.send_event("toolbar_update", action="Legend", active=True, disabled=False)
    mw_legend(cax.ax, 'on')
    cax.fig.canvas.draw()

def action_legend_disable(cax):
    mw_legend(cax.ax, display = 'off')
    cax.fig.canvas.send_event("toolbar_update", action="Legend", active=False, disabled=False)
    cax.fig.canvas.draw()


# editmode
def action_editmode():
    figure = plt.gcf()

    cfig = mw_get_cfig(figure)

    if cfig.edit_mode:
        editmode_disable(figure)
    else:
        editmode_enable(figure)

def editmode_enable(figure):
    cfig = mw_get_cfig()
    if cfig.edit_mode:
        return
    
    exit_pan_zoom(figure)
    datatips_disable(figure)
    
    # 清除所有游标线
    for cax in cfig.axs:
        clear_ax_cursor(cax)
    figure.canvas.send_event("toolbar_update", action="Cursor", active=False, disabled=False)
    
    cfig.edit_mode = True
    figure.canvas.send_event("toolbar_update", action="EditMode", active=True, disabled=False)
    
    for cax in cfig.axs:
        clear_ax_cursor(cax)

    c_objs = cfig.current_objs

    if len(c_objs) > 0:
        for obj in c_objs:
            obj.pick_self(True)
    elif len(cfig.axs) == 0:
        cfig.pick_self()
    else:
        mw_get_cax(figure.gca()).pick_self()
    
    if cfig.current_mplcursor != None:
        cfig.current_mplcursor.checked_tool_num += 1
    else:
        cfig.pick_self()

    figure.canvas.draw()

def editmode_disable(figure):
    if mw_get_cfig().edit_mode == False:
        return
    
    mw_get_cfig().edit_mode = False
    figure.canvas.send_event("toolbar_update", action="EditMode", active=False, disabled=False)
    mw_clear_status(False)

    if mw_get_cfig().current_mplcursor is not None:
        mw_get_cfig().current_mplcursor.checked_tool_num -= 1

    
# cursor
def action_cursor():
    figure = plt.gcf()

    if len(mw_get_cax().get_all_lines()) == 0:
        return

    if mw_get_cax().cursor:
        curser_disable(figure)
    else:
        curser_enable(figure)

def curser_enable(figure):
    editmode_disable(figure)
    exit_pan_zoom(figure)
    datatips_disable(figure)

    cursor_line = mw_cursor(figure.gca())
    figure.canvas.draw_idle()
    mw_get_cax().cursor_line.append(cursor_line)
    mw_get_cfig().cursor_lines.append(cursor_line)

    mw_get_cax().cursor = True
    figure.canvas.send_event("toolbar_update", action="Cursor", active=True, disabled=False)

def curser_disable(figure):
    if len(figure.axes) == 0:
        return
    
    clear_ax_cursor(mw_get_cax())
    figure.canvas.draw_idle()
    figure.canvas.send_event("toolbar_update", action="Cursor", active=False, disabled=False)

def clear_ax_cursor(cax):
    # cax = mw_get_cax(ax)
    for cursor_line in cax.cursor_line:
        cursor_line.line.remove()
        if hasattr(cursor_line, "hline"):
            cursor_line.hline.remove()
        cursor_line.annotation.remove()
        for points in cursor_line.points:
            for point in points:
                point.remove()
        cursor_line.points.clear()
        mw_get_cfig().cursor_lines.remove(cursor_line)

    cax.cursor_line.clear()
    cax.cursor = False


# pan
def action_pan():
    figure = plt.gcf()
    if mw_get_cfig().current_mplcursor is None:
        return
    
    canvas = figure.canvas
    toolbar = canvas.manager.toolbar
    
    mode = toolbar.mode.name

    if mode == "NONE":
        mw_get_cfig().current_mplcursor.checked_tool_num += 1
        figure.canvas.send_event("toolbar_update", action="Pan", active=True, disabled=False)
    elif mode == "PAN":
        mw_get_cfig().current_mplcursor.checked_tool_num -= 1
        figure.canvas.send_event("toolbar_update", action="Pan", active=False, disabled=False)
    else:
        figure.canvas.send_event("toolbar_update", action="Pan", active=True, disabled=False)



    editmode_disable(figure)
    curser_disable(figure)

    toolbar.pan()


# zoom
def action_zoom():
    figure = plt.gcf()
    if mw_get_cfig().current_mplcursor is None:
        return
    
    canvas = figure.canvas
    toolbar = canvas.manager.toolbar

    mode = toolbar.mode.name

    if mode == "NONE":
        mw_get_cfig().current_mplcursor.checked_tool_num += 1
        figure.canvas.send_event("toolbar_update", action="Zoom", active=True, disabled=False)
    elif mode == "ZOOM":
        mw_get_cfig().current_mplcursor.checked_tool_num -= 1
        figure.canvas.send_event("toolbar_update", action="Zoom", active=False, disabled=False)
    else:
        figure.canvas.send_event("toolbar_update", action="Zoom", active=True, disabled=False)


    editmode_disable(figure)
    curser_disable(figure)

    toolbar.zoom()

def action_home():
    figure = plt.gcf()
    if len(figure.axes) == 0:
        return
    ax = plt.gca()
    canvas = figure.canvas
    toolbar = canvas.manager.toolbar
    toolbar._nav_stack.home()
    toolbar.set_history_buttons()
    toolbar._update_view()
    # 视图重置时，使坐标轴可以自动缩放
    ax._autoscaleXon = True
    ax._autoscaleYon = True
    ax.autoscale_view()

# datatips
def action_datatips():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.data_tips:
        datatips_disable(figure)
    else:
        datatips_enable(figure)

def datatips_enable(figure):
    cfig = mw_get_cfig(figure)
    if cfig.data_tips:
        return
    
    if cfig.current_mplcursor is None:
        return
        
    exit_pan_zoom(figure)
    editmode_disable(figure)

    # 清除所有游标线
    for cax in cfig.axs:
        clear_ax_cursor(cax)
    figure.canvas.draw_idle()
    figure.canvas.send_event("toolbar_update", action="Cursor", active=False)
    
    if cfig.current_mplcursor == None:
        cursor = Cursor(self.figure)
        cfig.current_mplcursor = cursor

    cfig.current_mplcursor.set_current_selection()
    cfig.data_tips = True
    figure.canvas.send_event("toolbar_update", action="DataTips", active=True)

def datatips_disable(figure):
    cfig = mw_get_cfig(figure)
    if cfig.data_tips == False:
        return

    if cfig.current_mplcursor is None:
        return
        
    cfig.data_tips = False
    figure.canvas.send_event("toolbar_update", action="DataTips", active=False)


# 绘制文本框
def action_darw_text():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawRect" and cfig.draw_graphics.graphics_type == "textbox":
        text_disable(figure)
    else:
        text_enable(figure)

def text_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # 不需要发送哪些按钮不被选中
    # update_draw_button_status(figure, 'DrawText')

    mw_clear_status()

    line = DrawRect(figure, 'textbox')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def text_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})

# 绘制矩形
def action_draw_rect():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawRect" and cfig.draw_graphics.graphics_type == "rectangle":
        rect_disable(figure)
    else:
        rect_enable(figure)

def rect_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawRect')

    mw_clear_status()

    line = DrawRect(figure, 'rectangle')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def rect_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})

# 绘制椭圆
def action_draw_ellipse():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawEllipse":
        ellipse_disable(figure)
    else:
        ellipse_enable(figure)

def ellipse_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawEllipse')

    mw_clear_status()

    line = DrawEllipse(figure, 'ellipse')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def ellipse_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})

# 绘制直线
def action_draw_line():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawLines" and cfig.draw_graphics.line_type == "line":
        line_disable(figure)
    else:
        line_enable(figure)

def line_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawLine')

    mw_clear_status()

    line = DrawLines(figure)
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def line_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})

# 绘制箭头
def action_draw_arrow():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawLines" and cfig.draw_graphics.line_type == "arrow":
        arrow_disable(figure)
    else:
        arrow_enable(figure)

def arrow_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawArrow')

    mw_clear_status()

    line = DrawLines(figure, 'arrow')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def arrow_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})


# 绘制文本箭头
def action_draw_textarrow():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)

    if cfig.draw_graphics.__class__.__name__ == "DrawLines" and cfig.draw_graphics.line_type == "textarrow":
        textarrow_disable(figure)
    else:
        textarrow_enable(figure)

def textarrow_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawTextArrow')

    mw_clear_status()

    line = DrawLines(figure, 'textarrow')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def textarrow_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})


# 绘制双箭头
def action_draw_doublearrow():
    figure = plt.gcf()
    cfig = mw_get_cfig(figure)
    if cfig.draw_graphics.__class__.__name__ == "DrawLines" and cfig.draw_graphics.line_type == "doublearrow":
        doublearrow_disable(figure)
    else:
        doublearrow_enable(figure)

def doublearrow_enable(figure):
    editmode_enable(figure)

    figure.canvas.send_event("toolbar_update", action="Draw", active=True)
    # update_draw_button_status(figure, 'DrawDoubleArrow')

    mw_clear_status()

    line = DrawLines(figure, 'doublearrow')
    line.connect_draw()
    cfig = mw_get_cfig(figure)
    cfig.draw_graphics = line
    cfig.drawing = True

def doublearrow_disable(figure):
    figure.canvas.send_event("toolbar_update", action="Draw", active=False)

    cfig = mw_get_cfig(figure)
    cfig.drawing = False
    cfig.draw_graphics = None
    figure.canvas.send_event({"cursor":"default"})