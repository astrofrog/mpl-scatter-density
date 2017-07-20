from __future__ import division, print_function

import numpy as np

from matplotlib.image import AxesImage
from matplotlib.transforms import Bbox

from fast_histogram import histogram2d

from .color import make_cmap

__all__ = ['ScatterDensityArtist']


class ScatterDensityArtist(AxesImage):
    """
    Matplotlib artist to make a density plot of (x, y) scatter data.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`
        The axes to plot the artist into.
    x, y : iterable
        The data to plot.
    dpi : int or `None`
        The number of dots per inch to include in the density map. To use
        the native resolution of the drawing device, set this to None.
    downres_factor : int
        For interactive devices, when panning, the density map will
        automatically be made at a lower resolution and including only a
        subset of the points. The new dpi of the figure when panning will
        then be dpi / downres_factor, and the number of elements in the
        arrays will be reduced by downres_factor**2.
    cmap : `matplotlib.colors.Colormap`
        The colormap to use for the density map.
    color : str or tuple
        The color to use for the density map. This can be any valid
        Matplotlib color. If specified, this takes precedence over the
        colormap.
    alpha : float
        Overall transparency of the density map.
    norm : `matplotlib.colors.Normalize`
        The normalization class for the density map.
    kwargs
        Any additional keyword arguments are passed to AxesImage.
    """

    def __init__(self, ax, x, y, dpi=72, downres_factor=4, color=None, **kwargs):

        super(ScatterDensityArtist, self).__init__(ax, **kwargs)

        self._ax = ax
        self._ax.figure.canvas.mpl_connect('button_press_event', self.downres)
        self._ax.figure.canvas.mpl_connect('button_release_event', self.upres)

        if downres_factor < 1:
            raise ValueError('downres_factor should be a strictly positive integer value')

        self._dpi = dpi
        self._downres_factor = downres_factor
        self._x = x
        self._y = y
        self._update_subset()

        self.upres()
        self.set_array([[np.nan]])

        if color is not None:
            self.set_color(color)

    def set_color(self, color):
        if color is not None:
            self.set_cmap(make_cmap(color))

    def _update_subset(self):
        step = self._downres_factor ** 2
        self._x_sub = self._x[::step]
        self._y_sub = self._y[::step]

    def downres(self, event=None):
        if self._downres_factor == 1:
            return
        try:
            mode = self._ax.figure.canvas.toolbar.mode
        except AttributeError:
            return
        if mode != 'pan/zoom':
            return
        self._downres = True
        self.stale = True

    def upres(self, event=None):
        if self._downres_factor == 1:
            return
        self._downres = False
        self.stale = True

    def get_extent(self):
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        return xmin, xmax, ymin, ymax

    def get_window_extent(self, renderer=None):
        x0, x1, y0, y1 = self.get_extent()
        bbox = Bbox.from_extents([x0, y0, x1, y1])
        return bbox.transformed(self.axes.transData)

    def make_image(self, *args, **kwargs):

        xmin, xmax, ymin, ymax = self.get_extent()

        if self._dpi is None:
            dpi = self.axes.figure.get_dpi()
        else:
            dpi = self._dpi

        width = (self._ax.get_position().width *
                 self._ax.figure.get_figwidth())
        height = (self._ax.get_position().height *
                  self._ax.figure.get_figheight())

        nx = int(round(width * dpi))
        ny = int(round(height * dpi))

        if self._downres:
            nx_sub = nx // self._downres_factor
            ny_sub = ny // self._downres_factor
            array = histogram2d(self._y_sub, self._x_sub,
                                bins=(ny_sub, nx_sub),
                                range=((ymin, ymax), (xmin, xmax)))
        else:
            array = histogram2d(self._y, self._x,
                                bins=(ny, nx),
                                range=((ymin, ymax), (xmin, xmax)))

        if self.origin == 'upper':
            array = np.flipud(array)

        self.set_clim(np.nanmin(array), np.nanmax(array))
        self.set_data(array)

        return super(ScatterDensityArtist, self).make_image(*args, **kwargs)
