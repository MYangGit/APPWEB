"""
全局设置类，存储一些公共设置
"""

class CGlobalSetting(object):
    """
    全局设置类，存储一些公共设置变量

    Attributes:
        c_fig_lst : 初始化后的图窗对象
    """

    c_fig_lst = []
    cGlobalPlotPath = ""
    current_geo_path = ""
    icon_path = ""
    c_ax_pos_lst = [0.13, 0.11, 0.905, 0.925]
    precision = 6
    CGlobalPlatformVersion = 'Windows'
    cGlobalFont = ('Microsoft YaHei', 10, False, False)
    cGlobalMaxLineMarkersize = 1000
    cGlobalMaxLinewidth = 1000
    cGlobalMaxScatterMarkersize = 1e6
    cGlobalMaxFontsize = 1000
    isOnline = True
    line_copy_prop = []