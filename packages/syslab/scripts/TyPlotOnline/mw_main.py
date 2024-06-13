"""
名称：mw_main
功能：初始化信号槽，界面等 #界面初始化
实现：1.获取所有工具栏按钮，添加进工具栏内
      2.连接信号槽，包括事件、右键菜单等
接口：初始化函数
依赖：objs库、actions库
"""

import platform
import os
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

# from mw_actions import *
from TyPlotOnline.objects.mw_figure import CFigure, mw_update_caxe, mw_update_clines, mw_update_scatters
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting
from TyPlotOnline.common.mw_replace_function import replace_function
import matplotlib.font_manager as fm
# 设置工具栏使用工具栏管理器模式
plt.rcParams['toolbar'] = 'toolmanager'
plt.rcParams["agg.path.chunksize"] = 20000
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def find_fonts_path(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if 'python' in dirs and 'resources' in os.listdir(os.path.join(root, 'python')):
            resources_path = os.path.join(root, 'python', 'resources', 'fonts')
            if os.path.exists(resources_path):
                return resources_path
    print("字体设置错误，未找到字体文件。")

if "JULIA_BASE_DEPOT_PATH" in os.environ:
    julia_env_path = os.environ["JULIA_BASE_DEPOT_PATH"]
    julia_path = julia_env_path +  "/packages/TyPlot/"
    fonts_path = find_fonts_path(julia_path)

    # 将自定义字体文件路径添加到Matplotlib的字体搜索路径
    font_files = os.listdir(fonts_path)
    for font_file in font_files:
        font_path = os.path.join(fonts_path, font_file)
        fm.fontManager.addfont(font_path)
else:
    print("找不到 JULIA_BASE_DEPOT_PATH 环境变量。")

# 初始化函数
def init(figure, init=True, is_import=False, **kwargs):
    """
    初始化工具栏
    将actions库中实现的工具栏按钮添加至工具栏中

    Args:
        figure: 图窗对象

    Returns:
    Raises:
    """
    # if os.getenv('ISONLINE'):
    #     CGlobalSetting.isOnline = True
    # else:
    #     CGlobalSetting.isOnline = False
    CGlobalSetting.isOnline = True
    sys = platform.system()
    if sys == 'Windows':
        CGlobalSetting.CGlobalPlatformVersion = "Windows"
        # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial']
        CGlobalSetting.cGlobalFont = ('Microsoft YaHei', 10, False, False)
    elif sys == "Linux":
        CGlobalSetting.cGlobalFont = ('Microsoft YaHei', 10, False, False)
        if 'Ubuntu' in platform.version():
            CGlobalSetting.CGlobalPlatformVersion = "Ubuntu"
            # CGlobalSetting.cGlobalFont = ('AR PL UKai CN', 10, False, False)
        elif 'KYLINOS' in platform.version():
            CGlobalSetting.CGlobalPlatformVersion = "KYLINOS"
            # CGlobalSetting.cGlobalFont = ('CESI_KT_GB13000', 10, False, False)
        else:
            catout = os.popen('cat /etc/os-release').readlines()[0].strip()
            if "CentOS" in catout:
                CGlobalSetting.CGlobalPlatformVersion = "CentOS"
                # CGlobalSetting.cGlobalFont = ('AR PL UMing CN', 10, False,
                #                             False)
            elif "Ubuntu" in catout:
                CGlobalSetting.CGlobalPlatformVersion = "Ubuntu"
                # CGlobalSetting.cGlobalFont = ('AR PL UKai CN', 10, False,
                #                               False)
            elif CGlobalSetting.isOnline:
                CGlobalSetting.CGlobalPlatformVersion = "Online"
                # CGlobalSetting.cGlobalFont = ('AR PL UKai CN', 10, False,
                #                               False)
            else:
                CGlobalSetting.CGlobalPlatformVersion = "Ubuntu"
                # CGlobalSetting.cGlobalFont = ('AR PL UKai CN', 10, False,
                #                               False)
    elif sys == "Darwin":
        arch = platform.mac_ver()[2]
        if arch == 'x86_64':
            CGlobalSetting.CGlobalPlatformVersion = "macOS"
            # CGlobalSetting.cGlobalFont = ('PingFang SC', 10, False, False)
        else:
            raise SystemError(f"Unsupported MacOS arch: {arch}")
    else:
        raise SystemError(f"Unknown system: {sys}")
    replace_function()

    # if not CGlobalSetting.isOnline:
    #     init_toolbar(figure)

    # 设置对象可选中
    if init:
        ax = figure.gca()

    if not is_import:
        c_fig = CFigure(figure, **kwargs)

        # 将初始化后的图窗对象存储
        CGlobalSetting.c_fig_lst.append(c_fig)

        from matplotlib.lines import Line2D
        from matplotlib.collections import PathCollection

        for ax in figure.axes:
            mw_update_caxe(figure, ax)
            # mw_update_clines(figure, ax.get_lines())
            for child in ax._children:
                if isinstance(child, Line2D):
                    mw_update_clines(figure, [child])
                elif isinstance(child, PathCollection):
                    mw_update_scatters(figure, [child])

    # if init:
    #     mw_update_caxe(figure, ax)

    # 返回初始化后的figure对象
        return c_fig
    return None
