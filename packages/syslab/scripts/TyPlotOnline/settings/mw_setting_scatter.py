from TyPlotOnline.objects.mw_interface import *
import numpy as np


dict_marker_prop = {'+' : ['+'],
            'o' : ['o'],
            '.' : ['.'],
            'x' : ['x'],
            'square' : ['s'],
            'diamond' : ['D', 'd'],
            'v' : ['v'],
            '^' : ['^'],
            '>' : ['>'],
            '<' : ['<'],
            'pentagram' : ['*'],
            '|' : ['|'],
            '_' : ['_'],
            'none' : ['None', ' ', '', 'none']}


dict_marker = {'+' : ['+'],
            'o' : ['o'],
            '.' : ['.'],
            'x' : ['x'],
            '四方形' : ['s'],
            '菱形' : ['D', 'd'],
            'v' : ['v'],
            '^' : ['^'],
            '>' : ['>'],
            '<' : ['<'],
            '五角形' : ['*'],
            '无' : ['None', ' ', '', 'none']}


# 标记
def get_marker(s):
    cs = mw_get_cscatter(s)
    return cs.marker

def get_linewidth(s):
    return float(s.get_linewidth()[0])

def get_markeredgecolor(s):
    cs = mw_get_cscatter(s)
    return cs.edgecolor

def get_markerfacecolor(s):
    cs = mw_get_cscatter(s)
    return cs.facecolor

def set_marker(s, marker):
    if marker in dict_marker:
        marker = dict_marker[marker][0]
    elif marker in dict_marker_prop:
        marker = dict_marker_prop[marker][0]

    cs = mw_get_cscatter(s)
    cs.set_marker(marker)

def set_linewidth(s, ls):
    try:
        ls = float(ls)
    except:
        return
    
    if s.__class__.__name__ == "Path3DCollection":
        s._linewidth3d=[ls]
    s.set_linewidth(ls)

def set_markeredgecolor(s, color):
    cs = mw_get_cscatter(s)
    cs.set_edgecolor(color)

def set_markerfacecolor(s, color):
    cs = mw_get_cscatter(s)
    cs.set_facecolor(color)

# 透明度
def get_markerfacealpha(s):
    cs = mw_get_cscatter(s)

    return cs.facealpha

def get_markeredgealpha(s):
    cs = mw_get_cscatter(s)

    return cs.edgealpha

def set_markerfacealpha(s, alpha):
    try:
        alpha = float(alpha)
    except:
        return
    
    cs = mw_get_cscatter(s)
    cs.set_facealpha(alpha)

def set_markeredgealpha(s, alpha):
    try:
        alpha = float(alpha)
    except:
        return

    cs = mw_get_cscatter(s)
    cs.set_edgealpha(alpha)

# 颜色和大小数据
def get_sizedata(s):
    if len(s.get_sizes())>1:
        marker_size='1*'+str(len(s.get_sizes()))+' double'
    else:
        marker_size=s.get_sizes()[0]
    
    return marker_size

def set_sizedata(s, markersize):
    try:
        markersize = float(markersize)
    except:
        return

    s._sizes3d =np.ma.ravel((markersize))
    s.set_sizes(np.ma.ravel((markersize)))
        
# 图例
def get_displayname(s):
    return s.get_label()

def set_displayname(s, name):
    s.set_label(name)