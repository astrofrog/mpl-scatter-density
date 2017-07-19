import numpy as np

from raster_axes.color import make_cmap
from fast_histogram import histogram2d
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.image import AxesImage

__all__ = ['ScatterDensityArtist']


def warn_not_implemented(kwargs):
    for kwarg in kwargs:
        print("WARNING: keyword argument %s not implemented in raster scatter" % kwarg)


class ScatterDensityArtist(AxesImage):

    def __init__(self, ax, x, y, dpi=72, color=None, **kwargs):

        super(ScatterDensityArtist, self).__init__(ax, **kwargs)

        self._ax = ax
        # self._ax.callbacks.connect('ylim_changed', self._update)
        # self._ax.figure.canvas.mpl_connect('resize_event', self._update)
        self._ax.figure.canvas.mpl_connect('button_press_event', self.downres)
        self._ax.figure.canvas.mpl_connect('button_release_event', self.upres)

        self._dpi = dpi
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
        self._x_sub = self._x[::16]
        self._y_sub = self._y[::16]

    def downres(self, event=None):
        try:
            mode = self._ax.figure.canvas.toolbar.mode
        except AttributeError:
            return
        if mode != 'pan/zoom':
            return
        self._downres = True

    def upres(self, event=None):
        self._downres = False

    def get_extent(self):
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        return (xmin, xmax, ymin, ymax)

    def make_image(self, renderer, magnification=1.0, unsampled=False):

        trans = self.get_transform()

        xmin, xmax, ymin, ymax = self.get_extent()

        bbox = Bbox(np.array([[xmin, ymin], [xmax, ymax]]))
        transformed_bbox = TransformedBbox(bbox, trans)

        dpi = self._dpi

        width = (self._ax.get_position().width *
                 self._ax.figure.get_figwidth())
        height = (self._ax.get_position().height *
                  self._ax.figure.get_figheight())

        nx = int(round(width * dpi))
        ny = int(round(height * dpi))

        if self._downres:
            print('make image downres')
            array = histogram2d(self._y_sub, self._x_sub,
                                bins=(ny // 4, nx // 4),
                                range=((ymin, ymax), (xmin, xmax)))
        else:
            print('make image upres')
            array = histogram2d(self._y, self._x,
                                bins=(ny, nx),
                                range=((ymin, ymax), (xmin, xmax)))

        array[array == 0] = np.nan

        array = np.flipud(array)

        self.set_clim(np.nanmin(array), np.nanmax(array))
        self.set_array(array)

        return self._make_image(array, bbox, transformed_bbox,
                                self.axes.bbox, magnification,
                                unsampled=unsampled)
