from __future__ import division, print_function

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.projections import register_projection

from .scatter_density_artist import ScatterDensityArtist

__all__ = ['ScatterDensityAxes']


class ScatterDensityAxes(plt.Axes):

    name = 'scatter_density'

    def __init__(self, *args, **kwargs):
        plt.Axes.__init__(self, *args, **kwargs)

    def scatter_density(self, x, y, dpi=72, downres_factor=4, color=None, cmap=None,
                        alpha=1.0, norm=None, **kwargs):
        """
        Make a density plot of the (x, y) scatter data.

        Parameters
        ----------
        x, y : iterable
            The data to plot
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
            Transparency of the density map
        norm : `matplotlib.colors.Normalize`
            The normalization class for the density map.
        """

        self.set_xlim(np.min(x), np.max(x))
        self.set_ylim(np.min(y), np.max(y))

        scatter = ScatterDensityArtist(self, x, y, dpi=dpi, downres_factor=downres_factor,
                                       color=color, cmap=cmap,
                                       alpha=alpha, norm=norm, **kwargs)
        self.add_artist(scatter)

        return scatter


register_projection(ScatterDensityAxes)
