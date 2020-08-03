import numpy as np

from .color import make_cmap
from .base_image_artist import BaseImageArtist

__all__ = ['GenericDensityArtist']


class GenericDensityArtist(BaseImageArtist):
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

    def __init__(self, ax, dpi=72, color=None, vmin=None, vmax=None, norm=None,
                 histogram2d_func=None, update_while_panning=True, **kwargs):

        self._density_vmin = np.nanmin
        self._density_vmax = np.nanmax

        super(GenericDensityArtist, self).__init__(ax,
                                                   array_func=histogram2d_func,
                                                   dpi=dpi,
                                                   update_while_panning=update_while_panning,
                                                   **kwargs)

        if color is not None:
            self.set_color(color)

        if norm is not None:
            self.set_norm(norm)

        if vmin is not None or vmax is not None:
            self.set_clim(vmin, vmax)

    def set_color(self, color):
        if color is not None:
            self.set_cmap(make_cmap(color))

    def set_data(self, array):

        if callable(self._density_vmin):
            vmin = self._density_vmin(array)
        else:
            vmin = self._density_vmin

        if callable(self._density_vmax):
            vmax = self._density_vmax(array)
        else:
            vmax = self._density_vmax

        super(GenericDensityArtist, self).set_data(array)
        super(GenericDensityArtist, self).set_clim(vmin, vmax)

    def set_clim(self, vmin, vmax):
        self._density_vmin = vmin
        self._density_vmax = vmax

    def set_norm(self, norm):
        if norm is not None and norm.vmin is not None:
            self._density_vmin = norm.vmin
        if norm is not None and norm.vmax is not None:
            self._density_vmax = norm.vmax
        super(GenericDensityArtist, self).set_norm(norm)
