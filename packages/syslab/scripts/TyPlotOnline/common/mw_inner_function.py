"""
名称：mw_inner_function
功能：内部公共函数
"""
import numpy as np


# 来自matplotlib-3.3.4
def mw_check_in_list(_values, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* is in *_values*;
    if not, raise an appropriate ValueError.

    Examples
    --------
    >>> cbook._check_in_list(["foo", "bar"], arg=arg, other_arg=other_arg)
    """
    values = _values
    for k, v in kwargs.items():
        if v not in values:
            raise ValueError(
                "{!r} is not a valid value for {}; supported values are {}"
                .format(v, k, ', '.join(map(repr, values))))

# 来自matplotlib-3.3.4
def mw_process_unit_info(ax, xdata=None, ydata=None, kwargs=None):
    """Look for unit *kwargs* and update the axis instances as necessary"""

    def _process_single_axis(data, axis, unit_name, kwargs):
        # Return if there's no axis set
        if axis is None:
            return kwargs

        if data is not None:
            # We only need to update if there is nothing set yet.
            if not axis.have_units():
                axis.update_units(data)

        # Check for units in the kwargs, and if present update axis
        if kwargs is not None:
            units = kwargs.pop(unit_name, axis.units)
            if ax.name == 'polar':
                polar_units = {'xunits': 'thetaunits', 'yunits': 'runits'}
                units = kwargs.pop(polar_units[unit_name], units)

            if units != axis.units:
                axis.set_units(units)
                # If the units being set imply a different converter,
                # we need to update.
                if data is not None:
                    axis.update_units(data)
        return kwargs

    kwargs = _process_single_axis(xdata, ax.xaxis, 'xunits', kwargs)
    kwargs = _process_single_axis(ydata, ax.yaxis, 'yunits', kwargs)
    return kwargs

def get_index(arr):
    '''获取选中点下标序列'''
    if len(arr) <= 16:
        return np.arange(len(arr))
    elif len(arr) <= 24:
        return np.round(np.linspace(0, len(arr) - 1, 8)).astype(int)
    else:
        return np.round(np.linspace(0, len(arr) - 1, 16)).astype(int)
