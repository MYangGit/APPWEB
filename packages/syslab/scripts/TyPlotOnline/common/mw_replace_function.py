import logging
from re import T
from typing import List
from matplotlib.collections import Collection, PathCollection, QuadMesh
from matplotlib import _api
from numbers import Integral
from matplotlib.blocking_input import BlockingInput
from matplotlib.legend_handler import HandlerPolyCollection
from matplotlib.axes import SubplotBase
from matplotlib.axes._subplots import SubplotBase
from matplotlib.gridspec import GridSpec, SubplotSpec
# from matplotlib.pyplot import gcf, delaxes
import matplotlib
import numpy as np
from matplotlib import cbook
from matplotlib import legend
from matplotlib.legend import _get_legend_handles
from matplotlib.artist import Artist

def replace_function():
    BlockingInput.__call__ = replace__call__
    SubplotBase.__init__ = SubplotBase_init
    SubplotBase.change_geometry = change_geometry
    matplotlib.pyplot.subplot = subplot
    HandlerPolyCollection._update_prop = _update_prop
    # args 为 0 时，不警告。重写函数，注释掉警告代码
    legend._parse_legend_args = _parse_legend_args
    # 处理图例名为空或者下划线开头情况
    matplotlib.legend._get_legend_handles_labels = _get_legend_handles_labels

# 源码有误，替换
def replace__call__(self, n=1, timeout=30):
    """Blocking call to retrieve *n* events."""
    _api.check_isinstance(Integral, n=n)
    self.n = n
    self.events = []

    if self.fig.canvas.manager:
        # Ensure that the figure is shown, if we are managing it.
        self.fig.show()
    # Connect the events to the on_event function call.
    self.callbacks = [self.fig.canvas.mpl_connect(name, self.on_event)
                        for name in self.eventslist]
    try:
        # Start event loop.
        self.fig.canvas.start_event_loop(timeout=timeout)
    finally:  # Run even on exception like ctrl-c.
        # Disconnect the callbacks.
        self.cleanup()
    # Return the events in this case.
    return self.events

def _update_prop(self, legend_handle, orig_handle):
    def first_color(colors):
        if len(colors) == 0:
            return (0, 0, 0, 0)
        return tuple(colors[0])

    def get_first(prop_array):
        if len(prop_array):
            return prop_array[0]
        else:
            return None

    # orig_handle is a PolyCollection and legend_handle is a Patch.
    # Directly set Patch color attributes (must be RGBA tuples).
    legend_handle._facecolor = first_color(orig_handle.get_facecolor())
    legend_handle._edgecolor = first_color(orig_handle.get_edgecolor())
    legend_handle._fill = orig_handle.get_fill()
    legend_handle._hatch = orig_handle.get_hatch()
    # Hatch color is anomalous in having no getters and setters.
    legend_handle._hatch_color = orig_handle._hatch_color
    # Setters are fine for the remaining attributes.
    legend_handle.set_linewidth(get_first(orig_handle.get_linewidths()))
    legend_handle.set_linestyle(get_first(orig_handle.get_linestyles()))
    legend_handle.set_transform(get_first(orig_handle.get_transforms()))
    legend_handle.set_figure(orig_handle.get_figure())
    # Alpha is already taken into account by the color attributes.

def SubplotBase_init(self, fig, *args, **kwargs):
    self.figure = fig
    self._subplotspec = SubplotSpec._from_subplot_args(fig, args)
    self._axes_class.__init__(self, fig, [0, 0, 1, 1], **kwargs)
    # This will also update the axes position.
    # self.set_subplotspec(SubplotSpec._from_subplot_args(fig, args))
    if 'position' not in kwargs:
        self._set_position(self._subplotspec.get_position(self.figure))

def change_geometry(self, numrows, numcols, num):
    self._subplotspec = GridSpec(numrows, numcols,
                                    figure=self.figure)[num - 1]
    self.update_params()
    self.set_position(self._subplotspec.get_position(self.figure))

# 3.5.0该函数有误，替换至3.3.4版本
def subplot(*args, **kwargs):
    # Here we will only normalize `polar=True` vs `projection='polar'` and let
    # downstream code deal with the rest.
    unset = object()
    projection = kwargs.get('projection', unset)
    polar = kwargs.pop('polar', unset)
    if polar is not unset and polar:
        # if we got mixed messages from the user, raise
        if projection is not unset and projection != 'polar':
            raise ValueError(
                f"polar={polar}, yet projection={projection!r}. "
                "Only one of these arguments should be supplied."
            )
        kwargs['projection'] = projection = 'polar'

    # if subplot called without arguments, create subplot(1, 1, 1)
    if len(args) == 0:
        args = (1, 1, 1)

    # This check was added because it is very easy to type subplot(1, 2, False)
    # when subplots(1, 2, False) was intended (sharex=False, that is). In most
    # cases, no error will ever occur, but mysterious behavior can result
    # because what was intended to be the sharex argument is instead treated as
    # a subplot index for subplot()
    if len(args) >= 3 and isinstance(args[2], bool):
        _api.warn_external("The subplot index argument to subplot() appears "
                           "to be a boolean. Did you intend to use "
                           "subplots()?")
    # Check for nrows and ncols, which are not valid subplot args:
    if 'nrows' in kwargs or 'ncols' in kwargs:
        raise TypeError("subplot() got an unexpected keyword argument 'ncols' "
                        "and/or 'nrows'.  Did you intend to call subplots()?")

    fig = gcf()

    ax = fig.add_subplot(*args, **kwargs)
    fig.sca(ax)
    bbox = ax.bbox
    axes_to_delete = []
    for other_ax in fig.axes:
        if other_ax == ax:
            continue
        if bbox.fully_overlaps(other_ax.bbox):
            axes_to_delete.append(other_ax)
    for ax_to_del in axes_to_delete:
        delaxes(ax_to_del)

    return ax

def _parse_legend_args(axs, *args, handles=None, labels=None, **kwargs):
    """
    Get the handles and labels from the calls to either ``figure.legend``
    or ``axes.legend``.

    The parser is a bit involved because we support::

        legend()
        legend(labels)
        legend(handles, labels)
        legend(labels=labels)
        legend(handles=handles)
        legend(handles=handles, labels=labels)

    The behavior for a mixture of positional and keyword handles and labels
    is undefined and issues a warning.

    Parameters
    ----------
    axs : list of `.Axes`
        If handles are not given explicitly, the artists in these Axes are
        used as handles.
    *args : tuple
        Positional parameters passed to ``legend()``.
    handles
        The value of the keyword argument ``legend(handles=...)``, or *None*
        if that keyword argument was not used.
    labels
        The value of the keyword argument ``legend(labels=...)``, or *None*
        if that keyword argument was not used.
    **kwargs
        All other keyword arguments passed to ``legend()``.

    Returns
    -------
    handles : list of `.Artist`
        The legend handles.
    labels : list of str
        The legend labels.
    extra_args : tuple
        *args* with positional handles and labels removed.
    kwargs : dict
        *kwargs* with keywords handles and labels removed.

    """
    log = logging.getLogger(__name__)

    handlers = kwargs.get('handler_map', {}) or {}
    extra_args = ()

    if (handles is not None or labels is not None) and args:
        _api.warn_external("You have mixed positional and keyword arguments, "
                           "some input may be discarded.")

    # if got both handles and labels as kwargs, make same length
    if handles and labels:
        handles, labels = zip(*zip(handles, labels))

    elif handles is not None and labels is None:
        labels = [handle.get_label() for handle in handles]

    elif labels is not None and handles is None:
        # Get as many handles as there are labels.
        handles = [handle for handle, label
                   in zip(_get_legend_handles(axs, handlers), labels)]

    # No arguments - automatically detect labels and handles.
    elif len(args) == 0:
        handles, labels = _get_legend_handles_labels(axs, handlers)
        # args 为 0 时，不警告。注释掉警告代码 --typlot
        
        # if not handles:
        #     log.warning(
        #         "No artists with labels found to put in legend.  Note that "
        #         "artists whose label start with an underscore are ignored "
        #         "when legend() is called with no argument.")

    # One argument. User defined labels - automatic handle detection.
    elif len(args) == 1:
        labels, = args
        if any(isinstance(l, Artist) for l in labels):
            raise TypeError("A single argument passed to legend() must be a "
                            "list of labels, but found an Artist in there.")

        # Get as many handles as there are labels.
        handles = [handle for handle, label
                   in zip(_get_legend_handles(axs, handlers), labels)]

    # Two arguments:
    #   * user defined handles and labels
    elif len(args) >= 2:
        handles, labels = args[:2]
        extra_args = args[2:]

    else:
        raise TypeError('Invalid arguments to legend.')

    return handles, labels, extra_args, kwargs

def _get_legend_handles_labels(axs, legend_handler_map=None):
    """
    Return handles and labels for legend, internal method.

    """
    handles = []
    labels = []

    for handle in _get_legend_handles(axs, legend_handler_map):
        label = handle.get_label()

        # 用于处理图例为空或者下划线开头情况
        # 图例为空情况处理规则与MATLAB对齐
        # if label and not label.startswith('_'):
        if not label.startswith('_'):
            handles.append(handle)
            labels.append(label)
    return handles, labels