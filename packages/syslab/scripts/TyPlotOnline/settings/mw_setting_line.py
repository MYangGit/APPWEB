from TyPlotOnline.objects.mw_interface import *

def set_color(line, color):
    line.set_color(color)

#  曲线样式
def set_linestyle(line, style): 
    line.set_linestyle(style)

# 曲线线宽
def set_linewidth(line, linewidth):
    line.set_linewidth(linewidth)
    line.set_markeredgewidth(linewidth)

# marker
def set_marker(line, marker):
    line.set_marker(marker)

# markersize
def set_markersize(line, markersize):
    line.set_markersize(markersize)
