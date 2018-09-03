from __future__ import division, print_function

from .generic_density_artist import GenericDensityArtist
from .fixed_data_density_helper import FixedDataDensityHelper

__all__ = ['ScatterDensityArtist']


class ScatterDensityArtist(GenericDensityArtist):
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
    update_while_panning : bool, optional
        Whether to compute histograms on-the-fly while panning.
    kwargs
        Any additional keyword arguments are passed to AxesImage.
    """

    def __init__(self, ax, x, y, downres_factor=4, c=None, **kwargs):
        self.histogram2d_helper = FixedDataDensityHelper(ax, x, y, c=c, downres_factor=downres_factor)
        super(ScatterDensityArtist, self).__init__(ax, histogram2d_func=self.histogram2d_helper, **kwargs)

    def set_xy(self, x, y):
        self.histogram2d_helper.set_xy(x, y)

    def set_c(self, c):
        self.histogram2d_helper.set_c(c)

    def on_press(self, event=None, force=False):
        if not force:
            if self._update_while_panning and self.histogram2d_helper._downres_factor == 1:
                return
        self.histogram2d_helper.downres()
        return super(ScatterDensityArtist, self).on_press(force=force)

    def on_release(self, event=None):
        self.histogram2d_helper.upres()
        return super(ScatterDensityArtist, self).on_release()
