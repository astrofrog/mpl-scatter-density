import numpy as np

from raster_axes.color import make_cmap
from fast_histogram import histogram2d

__all__ = ['ScatterDensity']


def warn_not_implemented(kwargs):
    for kwarg in kwargs:
        print("WARNING: keyword argument %s not implemented in raster scatter" % kwarg)


class ScatterDensity(object):

    def __init__(self, ax, x, y, color='black', alpha=1.0, cmap=None, norm=None, **kwargs):

        warn_not_implemented(kwargs)

        self._ax = ax
        self._ax.callbacks.connect('ylim_changed', self._update)
        self._ax.figure.canvas.mpl_connect('resize_event', self._update)
        self._ax.figure.canvas.mpl_connect('button_press_event', self._downres)
        self._ax.figure.canvas.mpl_connect('button_release_event', self._upres)

        self._x = x
        self._y = y
        self._update_subset()

        self._color = color
        self._alpha = alpha
        self._cmap = cmap
        self._norm = norm

        self._raster = None
        self._upres()

        self._update(None)

    def _update_subset(self):
        self._x_sub = self._x[::16]
        self._y_sub = self._y[::16]

    def set_visible(self, visible):
        self._raster.set_visible(visible)

    def set_offsets(self, coords):
        self._x, self._y = zip(*coords)
        self._update_subset()
        self._update(None)

    def _downres(self, event=None):
        try:
            mode = self._ax.figure.canvas.toolbar.mode
        except AttributeError:
            return
        if mode != 'pan/zoom':
            return
        self._downres = True
        self._update(None)

    def _upres(self, event=None):
        self._downres = False
        self._update(None)

    def set(self, color=None, alpha=None, norm=None, **kwargs):

        warn_not_implemented(kwargs)

        if color is not None:
            self._color = color
            self._raster.set_cmap(make_cmap(self._color))

        if alpha is not None:
            self._alpha = alpha
            self._raster.set_alpha(self._alpha)

        if norm is not None:
            self._norm = norm
            self._raster.set_norm(self._norm)

        if self._color == 'red':
            self._raster.set_zorder(20)

        self._ax.figure.canvas.draw()

    def set_zorder(self, zorder):
        self._raster.set_zorder(zorder)

    def _update(self, event):

        dpi = self._ax.figure.get_dpi()

        print('_update', dpi)

        autoscale = self._ax.get_autoscale_on()

        if autoscale:
            self._ax.set_autoscale_on(False)

        width = self._ax.get_position().width \
            * self._ax.figure.get_figwidth()
        height = self._ax.get_position().height \
            * self._ax.figure.get_figheight()

        nx = int(round(width * dpi))
        ny = int(round(height * dpi))

        xmin, xmax = self._ax.get_xlim()
        ymin, ymax = self._ax.get_ylim()

        print(xmin, xmax)
        print(ymin, ymax)
        print(nx, ny)

        # if self._downres:
        #     print("IN HERE")
        #     array = histogram2d(self._y_sub, self._x_sub,
        #                         bins=(ny // 4, nx // 4),
        #                         range=((ymin, ymax), (xmin, xmax)))
        # else:
        array = histogram2d(self._y, self._x,
                            bins=(ny, nx),
                            range=((ymin, ymax), (xmin, xmax)))

        print(array.sum())

        array[array == 0] = np.nan

        if self._raster is None:
            print('HERE1')
            cmap = self._cmap or make_cmap(self._color)
            self._raster = self._ax.imshow(array,
                                           extent=[xmin, xmax, ymin, ymax],
                                           aspect='auto',
                                           cmap=cmap,
                                           interpolation='nearest',
                                           alpha=self._alpha, origin='lower',
                                           norm=self._norm,
                                           zorder=10)
        else:
            print("HERE2")
            print(np.nansum(array))
            self._raster.set_data(array)
            print([xmin, xmax, ymin, ymax])
            self._raster.set_extent([xmin, xmax, ymin, ymax])

        if autoscale:
            self._ax.set_autoscale_on(True)

    def remove(self):
        if self._raster is not None:
            self._raster.remove()
            self._raster = None
