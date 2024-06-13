from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
from TyPlotOnline.settings.mw_setting_common import *

from mpl_toolkits.mplot3d import Axes3D

# 坐标轴字体
def get_ax_font(ax):
    cax = mw_get_cax(ax)
    if cax:
        return cax.font
    else:
        return CGlobalSetting.cGlobalFont

def set_ax_fontfamily(ax, font_family):
    font_real = get_real_name(font_family)
    font = get_font(get_ax_font(ax), font_family = font_real)
    update_axes_font(ax, font)

def set_ax_fontsize(ax, font_size):
    font = get_font(get_ax_font(ax), font_size = font_size)
    update_axes_font(ax, font)

def set_ax_fontweight(ax, font_weight):
    font = get_font(get_ax_font(ax), font_weight = font_weight)
    update_axes_font(ax, font)

def set_ax_fontstyle(ax, font_style):
    font = get_font(get_ax_font(ax), font_italic = font_style)
    update_axes_font(ax, font)

def update_axes_font(ax, font):
    style = 'italic' if font[2] else 'normal'
    weight = 'bold' if font[3] else 'normal'
    fontdict={'family': font[0],'size': font[1], 'weight' : weight, 'style' : style}

    # 坐标轴标签文本
    ax.get_yaxis().get_label().update(fontdict)
    ax.get_xaxis().get_label().update(fontdict)

    # 坐标轴标题
    ax.title.update(fontdict)

    # 坐标轴刻度
    for tick_labels in ax.get_xaxis().get_majorticklabels():
        tick_labels.update(fontdict)
    for tick_labels in ax.get_yaxis().get_majorticklabels():
        tick_labels.update(fontdict)

    # 图例
    legend = ax.get_legend()
    if legend:
        for text in legend.texts:
            text.update(fontdict)
        legend.draw(ax.figure._cachedRenderer)

    # 3维坐标轴情况
    if isinstance(ax, Axes3D):
        ax.get_zaxis().get_label().update(fontdict)
        for tick_labels in ax.get_zaxis().get_majorticklabels():
            tick_labels.update(fontdict)

    ax.figure.canvas.draw()
    cax = mw_get_cax(ax)
    if cax:
        cax.font = font
    CGlobalSetting.cGlobalFont = font

# 坐标轴刻度
def get_ticks(ax, axis: str):
    axis = axis.lower()

    if axis == "x":
        return list(ax.get_xticks())
    elif axis == "theta":
        ticks = ax.get_xticks()
        return list(np.rad2deg(ticks))
    elif axis in ["y", "r"]:
        return list(ax.get_yticks())
    elif axis == "z":
        return list(ax.get_zticks())
    else:
        pass

def get_ticklabels(ax, axis: str):
    axis = axis.lower()

    if axis in ["x", "theta"]:
        return [l.get_text() for l in ax.get_xticklabels()]
    elif axis in ["y", "r"]:
        return [l.get_text() for l in ax.get_yticklabels()]
    elif axis == "z":
        return [l.get_text() for l in ax.get_zticklabels()]
    else:
        pass

def get_tickmode(ax, axis: str):
    cax = mw_get_cax(ax)
    axis = "Y" if axis == "R" else axis
    axis = "X" if axis == "Theta" else axis
    if cax and axis in cax.tick_auto:
        return cax.tick_auto[axis]
        
def get_xminortickmode(ax):
    cax = mw_get_cax(ax)
    if cax:
        return cax.minor_tick['X']

def get_yminortickmode(ax):
    cax = mw_get_cax(ax)
    if cax:
        return cax.minor_tick['Y']

def set_ax_ticks_ticklabels(ax, axis, tick_ticklabels):
    try:
        ticks, ticklabels = tick_ticklabels[0], tick_ticklabels[1]
        ticks = [ float(tick) for tick in ticks ]
    except:
        return

    if axis == 'X':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_xlim()
        ax.set_xticks(ticks)
        ax.set_xlim(xmin = min, xmax = max)
        ax.set_xticklabels(ticklabels)
        cax = mw_get_cax(ax)

        from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
        if isinstance(cax, CAxesYyaxis):
            if cax.ax == ax:
                cax.ax2.set_xticklabels(ticklabels)
            else:
                cax.ax.set_xticklabels(ticklabels)

        mw_get_cax(ax).tick_auto['X'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Y':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_ylim()
        ax.set_yticks(ticks)
        ax.set_ylim(ymin = min, ymax = max)
        ax.set_yticklabels(ticklabels)
        mw_get_cax(ax).tick_auto['Y'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Z':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_zlim()
        ax.set_zticks(ticks)
        ax.set_zlim(zmin = min, zmax = max)
        ax.set_zticklabels(ticklabels)
        mw_get_cax(ax).tick_auto['Z'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'R':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_ylim()
        ax.set_yticks(ticks)
        ax.set_ylim(ymin = min, ymax = max)
        ax.set_yticklabels(ticklabels)
        mw_get_cax(ax).tick_auto['Y'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Theta':
        _ticks = np.deg2rad(ticks)
        ax.set_xticks(_ticks)
        ax.set_xticklabels(ticklabels)
        mw_get_cax(ax).tick_auto['X'] = False

    update_view()

def set_ax_ticks(ax, axis, ticks):
    try:
        ticks = [ float(tick) for tick in ticks ]
    except:
        return
    
    if axis == 'X':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_xlim()
        ax.set_xticks(ticks)
        ax.set_xlim(xmin = min, xmax = max)
        cax = mw_get_cax(ax)

        mw_get_cax(ax).tick_auto['X'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Y':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_ylim()
        ax.set_yticks(ticks)
        ax.set_ylim(ymin = min, ymax = max)
        mw_get_cax(ax).tick_auto['Y'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Z':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_zlim()
        ax.set_zticks(ticks)
        ax.set_zlim(zmin = min, zmax = max)
        mw_get_cax(ax).tick_auto['Z'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'R':
        autoscalex_on = ax.get_autoscalex_on()
        min, max = ax.get_ylim()
        ax.set_yticks(ticks)
        ax.set_ylim(ymin = min, ymax = max)
        mw_get_cax(ax).tick_auto['Y'] = False
        ax.set_autoscalex_on(autoscalex_on)
    elif axis == 'Theta':
        _ticks = np.deg2rad(ticks)
        ax.set_xticks(_ticks)
        mw_get_cax(ax).tick_auto['X'] = False

    update_view()

def set_ax_ticklabels(ax, axis, ticklabels):
    if axis == 'X':
        ax.set_xticklabels(ticklabels)

        from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
        if isinstance(cax, CAxesYyaxis):
            if cax.ax == ax:
                cax.ax2.set_xticklabels(ticklabels)
            else:
                cax.ax.set_xticklabels(ticklabels)
    elif axis == 'Y':
        ax.set_yticklabels(ticklabels)
    elif axis == 'Z':
        ax.set_zticklabels(ticklabels)
    elif axis == 'R':
        ax.set_yticklabels(ticklabels)
    elif axis == 'Theta':
        ax.set_xticklabels(ticklabels)

    update_view()
    
def reset_ticks(ax, axis, auto):
    """
    将坐标轴刻度恢复至默认
    """
    # 当取消RTickMode或者ThetaTickMode勾选的情况处理
    if auto == False:
        if axis == 'R':
            mw_get_cax(ax).tick_auto['Y'] = False
        elif axis == 'Theta':
            mw_get_cax(ax).tick_auto['X'] = False
        elif axis == '':
            mw_get_ccolorbar(colorbar).tick_auto = False
        else:
            mw_get_cax(ax).tick_auto[axis] = False
        return
    
    cax = mw_get_cax(ax)
    if cax:
        font = cax.font
    else:
        font = CGlobalSetting.cGlobalFont
        
    style = 'italic' if font[2] else 'normal'
    weight = 'bold' if font[3] else 'normal'
    fontdict={'family':font[0],'size': font[1], 'weight' : weight, 'style' : style}

    if axis == 'X':
        ax.get_xaxis()._set_scale(ax.get_xscale())
        # ax.get_xaxis().reset_ticks()
        if not isinstance(ax, Axes3D):
            ax.minorticks_on()

        for tick_labels in ax.get_xaxis().get_majorticklabels():
            tick_labels.update(fontdict)
        
        min, max = ax.get_xlim()
        ax.get_xaxis().stale = True
        ax.autoscale(axis = 'x', enable = True)
        ax.set_xlim(xmin = min, xmax = max)
        mw_get_cax(ax).tick_auto['X'] = True
    elif axis == 'Y' or axis == 'R':
        ax.get_yaxis()._set_scale(ax.get_xscale())
        #ax.get_yaxis().reset_ticks()
        if not isinstance(ax, Axes3D):
            ax.minorticks_on()

        for tick_labels in ax.get_yaxis().get_majorticklabels():
            tick_labels.update(fontdict)

        min, max = ax.get_ylim()
        ax.get_yaxis().stale = True
        ax.autoscale(axis = 'y', enable = True)
        mw_get_cax(ax).tick_auto['Y'] = True
        ax.set_ylim(ymin = min, ymax = max)
    elif axis == 'Z':
        ax.get_zaxis()._set_scale(ax.get_xscale())
        #ax.get_zaxis().reset_ticks()
        # ax.minorticks_on()

        for tick_labels in ax.get_zaxis().get_majorticklabels():
            tick_labels.update(fontdict)

        min, max = ax.get_zlim()
        ax.get_zaxis().stale = True
        ax.autoscale(axis = 'z', enable = True)
        mw_get_cax(ax).tick_auto['Z'] = True
        ax.set_zlim(zmin = min, zmax = max)
    elif axis == '':
        colorbar._reset_locator_formatter_scale()
        colorbar.draw_all()
        mw_get_ccolorbar(colorbar).tick_auto = True
    elif axis == 'Theta':
        min, max = ax.get_xlim()
        ax.set_xticks(np.deg2rad(np.arange(0.0, 360.0, 30.0)))
        ax.xaxis.set_major_formatter(matplotlib.projections.polar.ThetaFormatter())
        for tick_labels in ax.get_xaxis().get_majorticklabels():
            tick_labels.update(fontdict)
        ax.set_xlim(xmin = min, xmax = max)
        mw_get_cax(ax).tick_auto['X'] = True

    update_view()

def set_ax_minorticks(ax, axis, display):
    if axis == 'X':
        xticks = ax.xaxis.get_minor_ticks()
        if display:
            line_width = ax.spines['left'].get_linewidth()
            ax.tick_params(which = 'minor', axis = 'x', length = 2.0 + line_width/2 - 0.4,
                width = line_width, grid_linewidth = line_width)
        else:
            ax.tick_params(which = 'minor', axis = 'x', length = 0)
        mw_get_cax(ax).minor_tick['X'] = display
    elif axis == "Y":
        yticks = ax.yaxis.get_minor_ticks()
        if display:
            line_width = ax.spines['left'].get_linewidth()
            ax.tick_params(which = 'minor', axis = 'y', length = 2.0 + line_width/2 - 0.4,
                width = line_width, grid_linewidth = line_width)
        else:
            ax.tick_params(which = 'minor', axis = 'y', length = 0)
        mw_get_cax(ax).minor_tick['Y'] = display

    update_view()

def update_minorticks(self,axis, state):
        pass

# 坐标轴标尺
def get_lim_name(axis: str):
    return axis + "Lim"

def get_lim(ax, axis: str):
    min, max = (0, 1)
    if axis == 'X':
        min, max = ax.get_xlim()
    elif axis == 'Y':
        min, max = ax.get_ylim()
    elif axis == 'Z':
        min, max = ax.get_zlim()
    elif axis == 'R':
        min, max = ax.get_ylim()
    elif axis == 'Theta':
        min, max = mw_get_cax(ax).theta_lim

    min = float(str_remove_zeros('%.4f' % min))
    max = float(str_remove_zeros('%.4f' % max))

    return min, max

def get_limmode_name(axis: str):
    return axis + "LimMode"

def get_limmode(ax, axis: str):
    if axis == 'X':
        return ax.get_autoscalex_on()
    elif axis == 'Y':
        return ax.get_autoscaley_on()
    elif axis == 'Z':
        return ax.get_autoscalez_on()
    elif axis == '':
        pass
    elif axis == 'R':
        return mw_get_cax(ax).lim_auto['R']
    elif axis == 'Theta':
        return mw_get_cax(ax).lim_auto['Theta']

def get_xcolor(ax):
    xcolor = ax.spines['bottom'].get_edgecolor()
    if isinstance(ax, Axes3D):
        xcolor = ax.w_xaxis.line.get_color()

    return xcolor

def get_ycolor(ax):
    ycolor = ax.spines['right'].get_edgecolor()
    if isinstance(ax, Axes3D):
        ycolor = ax.w_yaxis.line.get_color()

    return ycolor

def get_xscale(ax):
    return ax.get_xscale()

def get_yscale(ax):
    return ax.get_yscale()

def set_lim(ax, axis: str, value):
    update_lim(ax, axis, value[0], value[1])

def set_limemode(ax, axis: str, value):
    if axis == 'X':
        ax.autoscale(axis = 'x', enable = value)
    elif axis == 'Y':
        ax.autoscale(axis = 'y', enable = value)
    elif axis == 'Z':
        ax.autoscale(axis = 'z', enable = value)
    elif axis == '':
        pass
        # colorbar.norm.autoscale()
    elif axis == 'R':
        if value:
            ax.autoscale(axis = 'y', enable = value)
            mw_get_cax(ax).lim_auto['R'] = True
        else:
            # 取消RLimMode勾选状态的处理
            mw_get_cax(ax).lim_auto['R'] = False
    elif axis == 'Theta':
        if value:
            set_theta_lim(ax,0,360)
            mw_get_cax(ax).lim_auto['Theta'] = True
        else:
            # 取消ThetaLimMode勾选状态的处理
            mw_get_cax(ax).lim_auto['Theta'] = False

    ax.figure.canvas.draw()

def set_xcolor(ax, color):
    if isinstance(ax, Axes3D):
        ax.w_xaxis.line.set_color(color)
        ax.tick_params(which='both', axis='x', colors=color)
        ax.xaxis.label.set_color(color)
    else:
        ax.spines['bottom'].set_color(color)
        ax.spines['top'].set_color(color)
        ax.xaxis.label.set_color(color)
        ax.tick_params(which='both', axis='x', colors=color)
    
def set_ycolor(ax, color):
    if isinstance(ax, Axes3D):
        ax.w_yaxis.line.set_color(color)
        ax.tick_params(which='both', axis='y', colors=color)
        ax.yaxis.label.set_color(color)
    else:
        ax.spines['left'].set_color(color)
        ax.spines['right'].set_color(color)
        ax.yaxis.label.set_color(color)
        ax.tick_params(which='both', axis='y', colors=color)

def set_rcolor(ax,color):
    ax.spines['start'].set_color(color)
    ax.spines['end'].set_color(color)
    ax.spines['inner'].set_color(color)
    ax.tick_params(which='both', axis='y', colors=color)

def set_thetacolor(ax,color):
    ax.spines['polar'].set_color(color)
    ax.tick_params(which='both', axis='x', colors=color)

def set_xscale(ax, scale):
    set_ax_scale(ax, "X", scale)

def set_yscale(ax, scale):
    set_ax_scale(ax, "Y", scale)

def update_lim(ax, axis, min, max):
    """
    更新坐标轴标尺范围，需要考虑对数情况下坐标轴需要>=0
    """
    try:
        min = float(min)
        max = float(max)
    except:
        return

    if axis == 'X':
        if ax.get_xscale() == 'log':
            if min > 0:
                ax.set_xlim(xmin = min)
            if max > 0:
                ax.set_xlim(xmax = max)
        else:
            ax.set_xlim(xmin = min, xmax = max)
    elif axis == 'Y':
        if ax.get_yscale() == 'log':
            if min > 0:
                ax.set_ylim(ymin = min)
            if max > 0:
                ax.set_ylim(ymax = max)
        else:
            ax.set_ylim(ymin = min, ymax = max)
    elif axis == 'Z':
        if ax.get_zscale() == 'log':
            if min > 0:
                ax.set_zlim(zmin = min)
            if max > 0:
                ax.set_zlim(zmax = max)
        else:
            ax.set_zlim(zmin = min, zmax = max)
    elif axis == '':
        pass
        # colorbar.set_clim(min, max)
    elif axis == 'R':
        ax.set_ylim(ymin = min, ymax = max)
        mw_get_cax(ax).lim_auto['R'] = False
    elif axis == 'Theta':
        min_to_set = min
        max_to_set = max
        if max - min > 360:
            max_to_set = min_to_set + 360

        set_theta_lim(ax, min_to_set, max_to_set)
        mw_get_cax(ax).theta_lim = (min, max)
        mw_get_cax(ax).lim_auto['Theta'] = False

    update_view()

def set_theta_lim(ax, min, max):
    _min = np.deg2rad(min)
    _max = np.deg2rad(max)
    ax.set_xlim(_min, _max)
    ax.xaxis.set_major_locator(plt.MultipleLocator(np.deg2rad(30)))
    if (max-min) == 360:
        ax.set_xticks(np.deg2rad(np.arange(min, max, 30.0)))

def set_ax_scale(ax, axis, scale):
    """
    修改坐标轴比例尺，需要同步刻度
    """
    if scale not in ['linear', 'log']:
        return

    if axis == 'X':
        min, max = ax.get_xlim()

        # 刻度不是自动模式的情况下需要保留原刻度
        if mw_get_cax(ax).tick_auto['X'] == False:
            ticks = ax.get_xticks()
            tick_labels = [l.get_text() for l in ax.get_xticklabels()]

        if ax.get_autoscalex_on():
            ax.set_xscale(scale)
            set_limemode(ax, axis, True)
        elif min <= 0 and scale == 'log':
            ax.set_xscale(scale)
            set_limemode(ax, axis, True)
            ax.set_autoscalex_on(False)
            ax.set_xlim(xmax = max)
        else:
            ax.set_xscale(scale)
            update_lim(ax, axis, min, max)

        # 将原刻度设置到坐标轴
        if mw_get_cax(ax).tick_auto['X'] == False:
            autoscalex_on = ax.get_autoscalex_on()
            xmin, xmax = ax.get_xlim()
            ax.set_xticks(ticks)
            ax.set_xlim(xmin = xmin, xmax = xmax)
            ax.set_xticklabels(tick_labels)
            ax.set_autoscalex_on(autoscalex_on)

        ax.minorticks_on()
        # 需要同步修改属性面板刻度显示
    elif axis == 'Y':
        min, max = ax.get_ylim()

        # 刻度不是自动模式的情况下需要保留原刻度
        if mw_get_cax(ax).tick_auto['Y'] == False:
            ticks = ax.get_yticks()
            tick_labels = [l.get_text() for l in ax.get_yticklabels()]

        if ax.get_autoscaley_on():
            ax.set_yscale(scale)
            set_limemode(ax, axis, True)
        elif min <= 0 and scale == 'log':
            ax.set_yscale(scale)
            set_limemode(ax, axis, True)
            ax.set_autoscaley_on(False)
            ax.set_ylim(ymax = max)
        else:
            ax.set_yscale(scale)
            update_lim(ax, axis, min, max)

        # 将原刻度设置到坐标轴
        if mw_get_cax(ax).tick_auto['Y'] == False:
            autoscaley_on = ax.get_autoscaley_on()
            ymin, ymax = ax.get_ylim()
            ax.set_yticks(ticks)
            ax.set_ylim(ymin = ymin, ymax = ymax)
            ax.set_yticklabels(tick_labels)
            ax.set_autoscaley_on(autoscaley_on)

        ax.minorticks_on()
        # 需要同步修改属性面板刻度显示
    elif axis == 'Z':
        min, max = ax.get_zlim()

        # 刻度不是自动模式的情况下需要保留原刻度
        if mw_get_cax(ax).tick_auto['Z'] == False:
            ticks = ax.get_zticks()
            tick_labels = [l.get_text() for l in ax.get_zticklabels()]

        if ax.get_autoscalez_on():
            ax.set_zscale(scale)
            set_limemode(ax, axis, True)
        elif min <= 0 and scale == 'log':
            ax.set_zscale(scale)
            set_limemode(ax, axis, True)
            ax.set_autoscalez_on(False)
            ax.set_zlim(zmax = max)
        else:
            ax.set_zscale(scale)
            update_lim(ax, axis, min, max)

        # 将原刻度设置到坐标轴
        if mw_get_cax(ax).tick_auto['Z'] == False:
            autoscalez_on = ax.get_autoscalez_on()
            zmin, zmax = ax.get_zlim()
            ax.set_zticks(ticks)
            ax.set_zlim(zmin = zmin, zmax = zmax)
            ax.set_zticklabels(tick_labels)
            ax.set_autoscalez_on(autoscalez_on)
        ax.minorticks_on()
        # 需要同步修改属性面板刻度显示

    update_view()

# 获取legend是否存在及当前legends
def get_legend_status(ax):
    from TyPlotOnline.objects.mw_legend import CLegend
    legend = ax.get_legend()
    c_legend = None
    if legend != None:
        c_legend = CLegend(legend)
    return c_legend

# 坐标轴网格
# major
def get_xmajorgrid_status(ax):
    """
    获取x轴主网格线的状态
    """
    major_xticks = ax.xaxis.majorTicks

    bx_major = False
    if len(major_xticks) == 0:
        bx_major = False
    else:
        if all(tick.gridline.get_visible() for tick in major_xticks):
            bx_major = True
        elif not any(tick.gridline.get_visible() for tick in major_xticks):
            bx_major = False
        else:
            bx_major = None

    if isinstance(ax, Axes3D):
        bx_major = ax.xaxis.gridlines.get_visible()

    return bx_major

def get_ymajorgrid_status(ax):
    """
    获取y轴主网格线的状态
    """
    major_yticks = ax.yaxis.majorTicks

    by_major = False
    if len(major_yticks) == 0:
        by_major = False
    else:
        if all(tick.gridline.get_visible() for tick in major_yticks):
            by_major  = True
        elif not any(tick.gridline.get_visible() for tick in major_yticks):
            by_major  = False
        else:
            by_major  = None
    
    if isinstance(ax, Axes3D):
        by_major = ax.yaxis.gridlines.get_visible()

    return by_major

def get_zmajorgrid_status(ax):
    """
    获取y轴主网格线的状态
    """
    if isinstance(ax, Axes3D):
        return ax.zaxis.gridlines.get_visible()
    else:
        return None

def get_major_linestyle(ax):
    if isinstance(ax, Axes3D):
        if ax.xaxis._axinfo["grid"]['linestyle']:
            return ax.xaxis._axinfo["grid"]['linestyle']
        else:
            return '-'
    else:
        if 'grid_linestyle' in ax.get_xaxis()._minor_tick_kw:
            return ax.get_xaxis()._major_tick_kw['grid_linestyle']
        else:
            return '-'

def get_major_gridcolor(ax):
    if isinstance(ax, Axes3D):
        return ax.xaxis._axinfo["grid"]['color']
    elif 'grid_color' in ax.get_xaxis()._major_tick_kw:
        return ax.get_xaxis()._major_tick_kw['grid_color']
    else:
        return '#000000ff'

def get_major_gridalpha(ax):
    if isinstance(ax, Axes3D):
        color = ax.xaxis._axinfo["grid"]["color"]
        rgba_color = mcolors.to_rgba(color)
        return rgba_color[3]
    else:
        if 'grid_alpha' in ax.get_xaxis()._major_tick_kw:
            return ax.get_xaxis()._major_tick_kw['grid_alpha']
        else:
            return 0.15

def set_xmajorgrid_status(ax, status):
    update_grid_status(ax, which = "major", axis = "x", status = status)

def set_ymajorgrid_status(ax, status):
    update_grid_status(ax, which = "major", axis = "y", status = status)

def set_zmajorgrid_status(ax, status):
    update_grid_status(ax, which = "major", axis = "z", status = status)

def set_major_linestyle(ax, linestyle):
    update_grid_linestyle(ax, which = "major", linestyle = linestyle)

def set_major_gridcolor(ax, color):
    update_grid_color(ax, which = "major", color = color)

def set_major_gridalpha(ax, alpha):
    update_grid_alpha(ax, which = "major", alpha = alpha)

# minor
def get_xminorgrid_status(ax):
    """
    获取x轴次网格线的状态
    """
    minor_xticks = ax.xaxis.minorTicks

    bx_minor = False
    if len(minor_xticks) == 0:
        bx_minor = False
    else:
        if all(tick.gridline.get_visible() for tick in minor_xticks):
            bx_minor = True
        elif not any(tick.gridline.get_visible() for tick in minor_xticks):
            bx_minor = False
        else:
            bx_minor = None

    return bx_minor

def get_yminorgrid_status(ax):
    """
    获取y轴次网格线的状态
    """
    minor_yticks = ax.yaxis.minorTicks

    by_minor = False
    if len(minor_yticks) == 0:
        minor_yticks = False
    else:
        if all(tick.gridline.get_visible() for tick in minor_yticks):
            by_minor = True
        elif not any(tick.gridline.get_visible() for tick in minor_yticks):
            by_minor = False
        else:
            by_minor = None

    return by_minor

def get_minor_linestyle(ax):
    if 'grid_linestyle' in ax.get_xaxis()._minor_tick_kw:
        return ax.get_xaxis()._minor_tick_kw['grid_linestyle']
    else:
        return ':'

def get_minor_gridcolor(ax):
    if 'grid_color' in ax.get_xaxis()._minor_tick_kw:
        return ax.get_xaxis()._minor_tick_kw['grid_color']
    else:
        return '#000000ff'

def get_minor_gridalpha(ax):
    if 'grid_alpha' in ax.get_xaxis()._minor_tick_kw:
        return ax.get_xaxis()._minor_tick_kw['grid_alpha']
    else:
        return 0.25

def set_xminorgrid_status(ax, status):
    update_grid_status(ax, which = "minor", axis = "x", status = status)

def set_yminorgrid_status(ax, status):
    update_grid_status(ax, which = "minor", axis = "y", status = status)

def set_zminorgrid_status(ax, status):
    update_grid_status(ax, which = "minor", axis = "z", status = status)

def set_minor_linestyle(ax, linestyle):
    update_grid_linestyle(ax, which = "minor", linestyle = linestyle)

def set_minor_gridcolor(ax, color):
    update_grid_color(ax, which = "minor", color = color)

def set_minor_gridalpha(ax, alpha):
    update_grid_alpha(ax, which = "minor", alpha = alpha)


def update_grid_status(ax, which = 'major', axis = 'x', status = True, **kwargs):
    """
    修改坐标轴网格线的样式
    """
    cax = mw_get_cax(ax)
    if cax == None:
        return
    
    if isinstance(ax, Axes3D):
        if axis == 'x':
            ax.xaxis.gridlines.set_visible(status)
        elif axis == 'y':
            ax.yaxis.gridlines.set_visible(status)
        elif axis == 'z':
            ax.zaxis.gridlines.set_visible(status)

        if (ax.xaxis.gridlines.get_visible()
                and ax.yaxis.gridlines.get_visible()
                and ax.zaxis.gridlines.get_visible()):
                cax.grid = True
                cax.update_action_state()
        else:
            cax.grid = False
            cax.update_action_state()
    else:
        ax.grid(b = status, which = which, axis = axis, **kwargs)

        bx_major, by_major, bx_minor, by_minor = mw_get_grid_status(ax)
        if bx_major and by_major:
            cax.grid = True
            cax.update_action_state()
        else:
            cax.grid = False
            cax.update_action_state()

    update_view()

def update_grid_alpha(ax, which, alpha):
    if alpha < 0 or alpha > 1:
        return

    if isinstance(ax, Axes3D):
        new_color = mcolors.to_rgba(ax.xaxis._axinfo["grid"]['color'], alpha)
        ax.xaxis._axinfo["grid"]['color'] = new_color
        ax.yaxis._axinfo["grid"]['color'] = new_color
        ax.zaxis._axinfo["grid"]['color'] = new_color
        ax.xaxis.stale = True
        ax.yaxis.stale = True
        ax.zaxis.stale = True
    else:
        ax.get_xaxis().set_tick_params(which = which, grid_alpha = alpha)
        ax.get_yaxis().set_tick_params(which = which, grid_alpha = alpha)
        ax.get_xaxis().stale = True
        ax.get_yaxis().stale = True

    update_view()

def update_grid_linestyle(ax, which, linestyle):
    if isinstance(ax, Axes3D):
        ax.xaxis._axinfo["grid"]['linestyle'] = linestyle
        ax.yaxis._axinfo["grid"]['linestyle'] = linestyle
        ax.zaxis._axinfo["grid"]['linestyle'] = linestyle
        ax.xaxis.stale = True
        ax.yaxis.stale = True
        ax.zaxis.stale = True
    else:
        ax.get_xaxis().set_tick_params(which = which, grid_linestyle = linestyle)
        ax.get_yaxis().set_tick_params(which = which, grid_linestyle = linestyle)
        ax.get_xaxis().stale = True
        ax.get_yaxis().stale = True

    update_view()

def update_grid_color(ax, which, color):
    if isinstance(ax, Axes3D):
        old_color = ax.xaxis._axinfo["grid"]['color']
        rgba_color = mcolors.to_rgba(old_color)
        alpha = rgba_color[3]
        new_color = mcolors.to_rgba(color, alpha)
        ax.xaxis._axinfo["grid"]['color'] = new_color
        ax.yaxis._axinfo["grid"]['color'] = new_color
        ax.zaxis._axinfo["grid"]['color'] = new_color
        ax.xaxis.stale = True
        ax.yaxis.stale = True
        ax.zaxis.stale = True
    else:
        ax.get_xaxis().set_tick_params(which=which, grid_color=color)
        ax.get_yaxis().set_tick_params(which=which, grid_color=color)
        ax.get_xaxis().stale = True
        ax.get_yaxis().stale = True

    update_view()

# 框样式
def get_ax_color(ax):
    return ax.get_facecolor()

def get_ax_linewidth(ax):
    if isinstance(ax,PolarAxes):
        return ax.spines['polar'].get_linewidth()
    elif isinstance(ax,Axes3D):
        return ax.yaxis.line.get_linewidth()
    elif isinstance(ax,Axes):
        return ax.spines['left'].get_linewidth()

def set_ax_color(ax, color):
    if isinstance(ax, Axes3D):
        if color == 'none':
            current_color = ax.w_xaxis.pane.get_facecolor()
            new_color = mcolors.to_rgba(current_color, 0)
        else:
            new_color = mcolors.to_rgba(color, 1)

        ax.w_xaxis.set_pane_color(new_color)
        ax.w_yaxis.set_pane_color(new_color)
        ax.w_zaxis.set_pane_color(new_color)
    else:
        ax.set_facecolor(color)

    update_view()

def set_ax_linewidth(ax, linewidth):
    try:
        linewidth = float(linewidth)
    except:
        return
    
    if isinstance(ax, Axes3D):
        ax.xaxis.line.set_linewidth(linewidth)
        ax.xaxis._axinfo["tick"]['linewidth'][True] = linewidth
        ax.xaxis._axinfo["grid"]['linewidth'] = linewidth
        ax.xaxis._axinfo["tick"]['intword_factor'] = 3.5 + linewidth/2 - 0.4

        ax.yaxis.line.set_linewidth(linewidth)
        ax.yaxis._axinfo["tick"]['linewidth'][True] = linewidth
        ax.yaxis._axinfo["grid"]['linewidth'] = linewidth
        ax.yaxis._axinfo["tick"]['intword_factor'] = 3.5 + linewidth/2 - 0.4

        ax.zaxis.line.set_linewidth(linewidth)
        ax.zaxis._axinfo["tick"]['linewidth'][True] = linewidth
        ax.zaxis._axinfo["grid"]['linewidth'] = linewidth
        ax.zaxis._axinfo["tick"]['intword_factor'] = 3.5 + linewidth/2 - 0.4

        ax.xaxis.stale = True
        ax.yaxis.stale = True
        ax.zaxis.stale = True
    elif isinstance(ax,PolarAxes):
        ax.spines['polar'].set_linewidth(linewidth)
        ax.spines['inner'].set_linewidth(linewidth)
        ax.spines['start'].set_linewidth(linewidth)
        ax.spines['end'].set_linewidth(linewidth)
        ax.tick_params(which = 'both', width = linewidth, grid_linewidth = linewidth)
    else:
        ax.spines['right'].set_linewidth(linewidth)
        ax.spines['bottom'].set_linewidth(linewidth)
        ax.spines['left'].set_linewidth(linewidth)
        ax.spines['top'].set_linewidth(linewidth)

        # major_tick_length = ax.xaxis.majorTicks[0].tick1line.get_markersize()
        # minor_tick_length = ax.xaxis.minorTicks[0].tick1line.get_markersize()

        ax.tick_params(which = 'major', length = 3.5 + linewidth/2 - 0.4,
            width = linewidth, grid_linewidth = linewidth)
        if mw_get_cax(ax).minor_tick['X']:
            ax.tick_params(which = 'minor', axis = 'x', length = 2.0 + linewidth/2 - 0.4,
                width = linewidth, grid_linewidth = linewidth)
        else:
            ax.tick_params(which = 'minor', axis = 'x', grid_linewidth = linewidth)

        if mw_get_cax(ax).minor_tick['Y']:
            ax.tick_params(which = 'minor', axis = 'y', length = 2.0 + linewidth/2 - 0.4,
                width = linewidth, grid_linewidth = linewidth)
        else:
            ax.tick_params(which = 'minor', axis = 'y', grid_linewidth = linewidth)

    update_view()

# 位置
def get_position(ax):        
    pos = [ax.get_position().x0, ax.get_position().y0, ax.get_position().width, ax.get_position().height]

    return pos

def set_position(ax, pos):
    try:
        f_pos = (float(pos[0]),float(pos[1]),float(pos[2]),float(pos[3]))
    except:
        return
    
    ax.set_position(f_pos)
    update_view()