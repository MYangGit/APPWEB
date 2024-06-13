"""
名称：setting_figure
功能：图窗属性面板初始化
接口：图窗面板类
依赖：mw_setting_common、mw_interface
"""
from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.settings.mw_setting_common import *

def get_color(cfig):
    fig = cfig.fig
    face_color = fig.get_facecolor()
    if (len(face_color) == 4 and face_color[3] == 0) or len(face_color) == 0:
        face_color = 'none'

    return face_color

def set_color(cfig, color):
    fig = cfig.fig
    fig.set_facecolor(color)

def get_auto_adjust_view(cfig):
    return cfig.auto_adjust_view

def set_auto_adjust_view(cfig, auto):
    fig = cfig.fig
    cfig.auto_adjust_view = auto
    if auto:
        adjust_views(fig)

def get_data_tips_on(cfig):
    return cfig.data_tips_on

def set_data_tips_on(cfig, on):
    cfig.data_tips_on = on

def open_sampling(cfig, sampling):
    cfig.sampling = sampling
    if sampling:
        for cax in cfig.axs:
            cax.resample()
            if cax.__class__.__name__ == "CAxesYyaxis":
                cax.cax2.resample()
    else:
        for cax in cfig.axs:
            cax.unsample()
            if cax.__class__.__name__ == "CAxesYyaxis":
                cax.cax2.unsample()

def set_samplingnum(cfig,field_samplingnum):
    try:
        num = int(field_samplingnum)
    except ValueError:
        return
        
    if cfig.min_sampling_num == num:
        return

    if num <= 0:
        field_samplingnum.setText(str(cfig.min_sampling_num))
        return

    cfig.min_sampling_num = num
    if cfig.sampling:
        for cax in cfig.axs:
            cax.resample()
            if cax.__class__.__name__ == "CAxesYyaxis":
                cax.cax2.resample()

def change_sampling_algorithm(cfig,sampling_algorithm):
    cfig.sampling_algorithm = sampling_algorithm
    if cfig.sampling:
        for cax in cfig.axs:
            cax.resample()
            if cax.__class__.__name__ == "CAxesYyaxis":
                cax.cax2.resample()

def save_sampling_setting(cfig):
    cfig.write_sampling_setting(setting_widget)