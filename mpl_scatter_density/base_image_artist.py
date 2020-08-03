import inspect

import numpy as np

from matplotlib.image import AxesImage
from matplotlib.transforms import (IdentityTransform, TransformedBbox,
                                   BboxTransformFrom, Bbox)

__all__ = ['BaseImageArtist', 'supports_resize']

EMPTY_IMAGE = np.array([[np.nan]])
IDENTITY = IdentityTransform()

SUPPORTS_RESIZE = ('FigureCanvasTk', 'FigureCanvasQT')


def supports_resize(canvas):

    # We check whether the canvas supports resizing by using the name of the
    # class and its parents rather than checking with isinstance, since the
    # latter requires importing the relevant canvas classes which could then
    # trigger an import of e.g. Qt or Tk. We also check for specific method
    # names that exists on the expected canvases, in case names aren't
    # sufficient.

    parent_classes = [cls.__name__.split('.')[-1]
                      for cls in inspect.getmro(canvas.__class__)]

    return set(parent_classes) & set(SUPPORTS_RESIZE)


class BaseImageArtist(AxesImage):
    """
    Matplotlib artist that uses images generated on-the-fly.

    Parameters
    ----------
    ax : `matplotlib.axes.Axes`
        The axes to plot the artist into.
    dpi : int or `None`
        The number of dots per inch to include in the density map. To use
        the native resolution of the drawing device, set this to None.
    array_func : callable, optional
        The function (or callable instance) to use for computing the 2D
        histogram - this should take the arguments ``bins`` and ``range`` as
        defined by :func:`~numpy.histogram2d` as well as a ``pressed`` keyword
        argument that indicates whether the user is currently panning/zooming.
    kwargs
        Any additional keyword arguments are passed to AxesImage.
    """

    def __init__(self, ax, dpi=72, array_func=None, update_while_panning=True, **kwargs):

        super(BaseImageArtist, self).__init__(ax, **kwargs)

        self._array_func = array_func

        self._make_image_called = False
        self._pressed = False

        self._ax = ax
        self._ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self._ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

        self._update_while_panning = update_while_panning

        self.set_dpi(dpi)

        self.on_release()
        self.set_array(EMPTY_IMAGE)

        # Not all backends support timers properly, so we explicitly whitelist
        # backends for which they do. In these cases, we avoid recomputing the
        # density map during resizing.
        if supports_resize(self._ax.figure.canvas):
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
            return super(BaseImageArtist, self).make_image(*args, **kwargs)

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

        array = self._array_func(bins=bins, range=((ymin, ymax), (xmin, xmax)))

        if flip_x or flip_y:
            if flip_x and flip_y:
                array = array[::-1, ::-1]
            elif flip_x:
                array = array[:, ::-1]
            else:
                array = array[::-1, :]

        if self.origin == 'upper':
            array = np.flipud(array)

        self.set_data(array)

        self._make_image_called = True

        return super(BaseImageArtist, self).make_image(*args, **kwargs)

    def remove(self):
        if self._timer is not None:
            self._timer.stop()
            self._timer = None
        super(BaseImageArtist, self).remove()
        # We explicitly clean up the reference to the _array_func function since
        # this may in some cases cause circular references.
        self._array_func = None
