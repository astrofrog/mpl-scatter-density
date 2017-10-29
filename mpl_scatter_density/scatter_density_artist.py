from __future__ import division, print_function

from math import log10

import numpy as np

from matplotlib.image import AxesImage
from matplotlib.transforms import (IdentityTransform, TransformedBbox,
                                   BboxTransformFrom, Bbox)

from fast_histogram import histogram2d

from .color import make_cmap

__all__ = ['ScatterDensityArtist']

EMPTY_IMAGE = np.array([[np.nan]])
IDENTITY = IdentityTransform()


class ScatterDensityArtist(AxesImage):
    """
    Matplotlib artist to make a density plot of (x, y) scatter data.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`
        The axes to plot the artist into.
    x, y : iterable
        The data to plot.
    c : iterable
        Values to use for color-encoding. This is meant to be the same as
        the argument with the same name in :meth:`~matplotlib.axes.Axes.scatter`
        although for now only 1D iterables of values are accepted. Note that
        values are averaged inside each pixel of the density map *before*
        applying the colormap, which in some cases will be different from what
        the average color of markers would have been inside each pixel.
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
    vmin, vmax : float or func
        The lower and upper levels used for scaling the density map. These can
        optionally be functions that take the density array and returns a single
        value (e.g. a function that returns the 5% percentile, or the minimum).
        This is useful since when zooming in/out, the optimal limits change.
    kwargs
        Any additional keyword arguments are passed to AxesImage.
    """

    def __init__(self, ax, x, y, dpi=72, downres_factor=4, color=None, c=None,
                 vmin=None, vmax=None, **kwargs):

        super(ScatterDensityArtist, self).__init__(ax, **kwargs)

        self._c = None
        self._density_vmin = np.nanmin
        self._density_vmax = np.nanmax

        self._ax = ax
        self._ax.figure.canvas.mpl_connect('button_press_event', self.downres)
        self._ax.figure.canvas.mpl_connect('button_release_event', self.upres)

        if downres_factor < 1:
            raise ValueError('downres_factor should be a strictly positive integer value')

        self._downres_factor = downres_factor
        self.set_dpi(dpi)
        self.set_xy(x, y)
        self.set_c(c)

        self.upres()
        self.set_array(EMPTY_IMAGE)

        if color is not None:
            self.set_color(color)

        if vmin is not None or vmax is not None:
            self.set_clim(vmin, vmax)

    def set_color(self, color):
        if color is not None:
            self.set_cmap(make_cmap(color))

    def set_xy(self, x, y):
        self._x = x
        self._y = y
        self._x_log = None
        self._y_log = None
        self._x_log_sub = None
        self._y_log_sub = None
        step = self._downres_factor ** 2
        self._x_sub = self._x[::step]
        self._y_sub = self._y[::step]

    def set_c(self, c):
        self._c = c
        step = self._downres_factor ** 2
        if self._c is None:
            self._c_sub = None
        else:
            self._c_sub = self._c[::step]

    def set_dpi(self, dpi):
        self._dpi = dpi

    def _update_x_log(self):
        step = self._downres_factor ** 2
        self._x_log = np.log10(self._x)
        self._x_log_sub = self._x_log[::step]

    def _update_y_log(self):
        step = self._downres_factor ** 2
        self._y_log = np.log10(self._y)
        self._y_log_sub = self._y_log[::step]

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

    def get_transform(self):

        # If we don't override this, the transform includes LogTransforms
        # and the final image gets warped to be 'correct' in data space
        # since Matplotlib 2.x:
        #
        #   https://matplotlib.org/users/prev_whats_new/whats_new_2.0.0.html#non-linear-scales-on-image-plots
        #
        # However, we want pixels to always visually be the same size, so we
        # override the transform to not include the LogTransform components.

        xmin, xmax = self._ax.get_xlim()
        ymin, ymax = self._ax.get_ylim()

        bbox = BboxTransformFrom(TransformedBbox(Bbox([[xmin, ymin], [xmax, ymax]]),
                                                 IDENTITY))

        return bbox + self._ax.transAxes

    def make_image(self, *args, **kwargs):

        xmin, xmax = self._ax.get_xlim()
        ymin, ymax = self._ax.get_ylim()

        xscale = self._ax.get_xscale()
        yscale = self._ax.get_yscale()

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

        flip_x = xmin > xmax
        flip_y = ymin > ymax

        if flip_x:
            xmin, xmax = xmax, xmin

        if flip_y:
            ymin, ymax = ymax, ymin

        if xscale == 'log':
            xmin, xmax = log10(xmin), log10(xmax)
            if self._x_log is None:
                # We do this here insead of in set_xy to save time since in
                # set_xy we don't know yet if the axes will be log or not.
                self._update_x_log()
            if self._downres:
                x = self._x_log_sub
            else:
                x = self._x_log
        elif xscale == 'linear':
            if self._downres:
                x = self._x_sub
            else:
                x = self._x
        else:
            raise ValueError('Unexpected xscale: {0}'.format(xscale))

        if yscale == 'log':
            ymin, ymax = log10(ymin), log10(ymax)
            if self._y_log is None:
                # We do this here insead of in set_xy to save time since in
                # set_xy we don't know yet if the axes will be log or not.
                self._update_y_log()
            if self._downres:
                y = self._y_log_sub
            else:
                y = self._y_log
        elif yscale == 'linear':
            if self._downres:
                y = self._y_sub
            else:
                y = self._y
        else:
            raise ValueError('Unexpected xscale: {0}'.format(xscale))

        if self._downres:
            nx_sub = nx // self._downres_factor
            ny_sub = ny // self._downres_factor
            bins = (ny_sub, nx_sub)
            weights = self._c_sub
        else:
            bins = (ny, nx)
            weights = self._c

        if weights is None:
            array = histogram2d(y, x, bins=bins, weights=weights,
                                range=((ymin, ymax), (xmin, xmax)))
        else:
            array = histogram2d(y, x, bins=bins, weights=weights,
                                range=((ymin, ymax), (xmin, xmax)))
            count = histogram2d(y, x, bins=bins,
                                range=((ymin, ymax), (xmin, xmax)))

            with np.errstate(invalid='ignore'):
                array /= count

        if flip_x or flip_y:
            if flip_x and flip_y:
                array = array[::-1, ::-1]
            elif flip_x:
                array = array[:, ::-1]
            else:
                array = array[::-1, :]

        if self.origin == 'upper':
            array = np.flipud(array)

        if callable(self._density_vmin):
            vmin = self._density_vmin(array)
        else:
            vmin = self._density_vmin

        if callable(self._density_vmax):
            vmax = self._density_vmax(array)
        else:
            vmax = self._density_vmax

        self.set_data(array)
        super(ScatterDensityArtist, self).set_clim(vmin, vmax)

        return super(ScatterDensityArtist, self).make_image(*args, **kwargs)

    def set_clim(self, vmin, vmax):
        self._density_vmin = vmin
        self._density_vmax = vmax

    def set_norm(self, norm):
        if norm.vmin is not None:
            self._density_vmin = norm.vmin
        if norm.vmax is not None:
            self._density_vmax = norm.vmax
        super(ScatterDensityArtist, self).set_norm(norm)
