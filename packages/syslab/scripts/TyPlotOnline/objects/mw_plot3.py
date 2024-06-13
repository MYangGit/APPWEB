"""
名称：plot3
功能：初始化三维线条图
接口：三维线条图类
依赖：
"""

import mpl_toolkits as mpltool
from TyPlotOnline.objects.mw_interface import *


import numpy as np


def plot3(ax, xs, ys, zs, fmt = "-", **kwargs):

    had_data = ax.has_data()

    z = np.broadcast_to(zs, np.shape(xs))
    line = ax.plot(xs, ys, fmt, **kwargs)[0]
    mpltool.mplot3d.art3d.line_2d_to_3d(line, zs=z, zdir='z')
    xs, ys, z = mpltool.mplot3d.art3d.juggle_axes(xs, ys, z, 'z')
    ax.auto_scale_xyz(xs, ys, z, had_data)

    return line


def mw_plot3(ax, *args, zdir='z', **kwargs):
        """
        Plot 2D or 3D data.

        Parameters
        ----------
        xs : 1D array-like
            x coordinates of vertices.
        ys : 1D array-like
            y coordinates of vertices.
        zs : float or 1D array-like
            z coordinates of vertices; either one for all points or one for
            each point.
        zdir : {'x', 'y', 'z'}, default: 'z'
            When plotting 2D data, the direction to use as z ('x', 'y' or 'z').
        **kwargs
            Other arguments are forwarded to `matplotlib.axes.Axes.plot`.
        """
        # `zs` can be passed positionally or as keyword; checking whether
        # args[0] is a string matches the behavior of 2D `plot` (via
        # `_process_plot_var_args`).
        kwargs = mw_normalize_kwargs('line', **kwargs)
        linewidth_kwargs = kwargs.pop('linewidth','')
        linewidth = 1 if linewidth_kwargs == '' else linewidth_kwargs
        if linewidth <= 0:
            return None
        kwargs['linewidth'] = linewidth

        markerfacecolor_kwargs = kwargs.pop('markerfacecolor','')
        markerfacecolor = 'none' if markerfacecolor_kwargs == '' else markerfacecolor_kwargs
        kwargs['markerfacecolor'] = markerfacecolor

        lines = []
        while args and not isinstance(args[0], str):
            xs, ys, zs, *args = args
            if 'xs' in kwargs or 'yz' in kwargs or'zs' in kwargs:
                raise TypeError("plot() for multiple values for argument 'z'")

            fmt = "-"
            if args and isinstance(args[0], str):
                fmt, *args = args

            dim = np.shape(xs)
            dim1 = np.shape(ys)
            dim2 = np.shape(zs)
            if dim != dim1:
                print("X和Y维度必须一致")

            # 存在XY与Z维度不同的情况
            if len(dim) == 0 and len(dim1) == 0:
                line = plot3(ax, xs, ys, zs, fmt, **kwargs)
                lines.append(line)
                return lines

            if(len(dim) != 1 and dim[0] != 1 and dim[1] != 1):
                if len(dim2) != len(dim1):
                    for i in range(0,dim[1]):
                        x = xs[:,i]
                        y = ys[:,i]
                        line = plot3(ax, x, y, zs, fmt, **kwargs)
                        lines.append(line)
                    return lines
                else:
                    for i in range(0,dim[1]):
                        x = xs[:,i]
                        y = ys[:,i]
                        z = zs[:,i]
                        line = plot3(ax, x, y, z, fmt, **kwargs)
                        lines.append(line)
                    return lines

            line = plot3(ax, xs, ys, zs, fmt, **kwargs)
            lines.append(line)

        return lines

def IsAxes3d(ax):
    if isinstance(ax, Axes3D):
        return True

    return False