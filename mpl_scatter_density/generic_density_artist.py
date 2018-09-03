from __future__ import division, print_function

import numpy as np

from matplotlib.image import AxesImage
from matplotlib.transforms import (IdentityTransform, TransformedBbox,
                                   BboxTransformFrom, Bbox)

from .color import make_cmap

__all__ = ['GenericDensityArtist']

EMPTY_IMAGE = np.array([[np.nan]])
IDENTITY = IdentityTransform()

SUPPORTS_RESIZE = []

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTk
except ImportError:
    pass
else:
    SUPPORTS_RESIZE.append(FigureCanvasTk)

try:
    from matplotlib.backends.backend_qt5 import FigureCanvasQT
except ImportError:
    pass
else:
    SUPPORTS_RESIZE.append(FigureCanvasQT)

SUPPORTS_RESIZE = tuple(SUPPORTS_RESIZE)


class GenericDensityArtist(AxesImage):
    """
    Matplotlib artist to make a density plot given a helper histogram function.

    This is a more generic form of ``ScatterDensityArtist``. Here, we can
    initialize the class with a histogram function that just takes bins and the
    range of values, and returns a density array. This is useful for cases where
    the data might be changing dynamically over time.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`
        The axes to plot the artist into.
    dpi : int or `None`
        The number of dots per inch to include in the density map. To use
        the native resolution of the drawing device, set this to None.
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
    histogram2d_func : callable, optional
        The function (or callable instance) to use for computing the 2D
        histogram - this should take the arguments ``bins`` and ``range`` as
        defined by :func:`~numpy.histogram2d` as well as a ``pressed`` keyword
        argument that indicates whether the user is currently panning/zooming.
    kwargs
        Any additional keyword arguments are passed to AxesImage.
    """

    def __init__(self, ax, dpi=72, color=None, vmin=None, vmax=None, norm=None, histogram2d_func=None, update_while_panning=True, **kwargs):

        super(GenericDensityArtist, self).__init__(ax, **kwargs)

        self._histogram2d_func = histogram2d_func

        self._make_image_called = False
        self._pressed = False
        self._density_vmin = np.nanmin
        self._density_vmax = np.nanmax

        self._ax = ax
        self._ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self._ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

        self._update_while_panning = update_while_panning

        self.set_dpi(dpi)

        self.on_release()
        self.set_array(EMPTY_IMAGE)

        if color is not None:
            self.set_color(color)

        if norm is not None:
            self.set_norm(norm)

        if vmin is not None or vmax is not None:
            self.set_clim(vmin, vmax)

        # Not all backends support timers properly, so we explicitly whitelist
        # backends for which they do. In these cases, we avoid recomputing the
        # density map during resizing.
        if isinstance(self._ax.figure.canvas, SUPPORTS_RESIZE):
            self._ax.figure.canvas.mpl_connect('resize_event', self._resize_start)
            self._timer = self._ax.figure.canvas.new_timer(interval=500)
            self._timer.single_shot = True
            self._timer.add_callback(self._resize_end)
        else:
            self._timer = None

    def _resize_start(self, event=None):
        if not self._make_image_called:
            # Only handle resizing once the map has been shown at least once
            # to avoid 'blinking' at the start.
            return
        self.on_press(force=True)
        self._timer.start()

    def _resize_end(self, event=None):
        self.on_release()
        self.stale = True
        self._ax.figure.canvas.draw()

    def set_color(self, color):
        if color is not None:
            self.set_cmap(make_cmap(color))

    def set_dpi(self, dpi):
        self._dpi = dpi

    def on_press(self, event=None, force=False):
        if not force:
            try:
                mode = self._ax.figure.canvas.toolbar.mode
            except AttributeError:  # pragma: nocover
                return
            if mode != 'pan/zoom':
                return
        self._pressed = True
        self.stale = True

    def on_release(self, event=None):
        self._pressed = False
        self.stale = True

    def get_extent(self):

        if not self._update_while_panning and self._pressed:
            return self._extent

        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()

        self._extent = xmin, xmax, ymin, ymax

        return self._extent

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

        if not self._update_while_panning and self._pressed:
            return super(GenericDensityArtist, self).make_image(*args, **kwargs)

        xmin, xmax = self._ax.get_xlim()
        ymin, ymax = self._ax.get_ylim()

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

        bins = (ny, nx)

        array = self._histogram2d_func(bins=bins, range=((ymin, ymax), (xmin, xmax)))

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
        super(GenericDensityArtist, self).set_clim(vmin, vmax)

        self._make_image_called = True

        return super(GenericDensityArtist, self).make_image(*args, **kwargs)

    def set_clim(self, vmin, vmax):
        self._density_vmin = vmin
        self._density_vmax = vmax

    def set_norm(self, norm):
        if norm.vmin is not None:
            self._density_vmin = norm.vmin
        if norm.vmax is not None:
            self._density_vmax = norm.vmax
        super(GenericDensityArtist, self).set_norm(norm)

    def remove(self):
        if self._timer is not None:
            self._timer.stop()
            self._timer = None
        super(GenericDensityArtist, self).remove()
        # We explicitly clean up the reference to the histogram2d function since
        # this may in some cases cause circular references.
        self._histogram2d_func = None
