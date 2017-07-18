from __future__ import division, print_function

import uuid

import numpy as np

import matplotlib.pyplot as plt

from raster_axes.scatter_density import ScatterDensity

__all__ = ['ScatterDensityAxes']


class ScatterDensityAxes(plt.Axes):

    def __init__(self, *args, **kwargs):
        plt.Axes.__init__(self, *args, **kwargs)
        self._scatter_objects = {}

    def scatter_density(self, x, y, color='black', cmap=None, alpha=1.0, norm=None, **kwargs):
        """
        Make a density plot of the (x, y) scatter data.

        Parameters
        ----------
        x, y : iterable
            The data to plot
        color : str or tuple
            The color to use for the density map. This can be any valid
            Matplotlib color.
        cmap : `matplotlib.colors.Colormap`
            The colormap to use for the density map. If specified, this takes
            precedence over the color argument.
        alpha : float
            Transparency of the density map
        norm : `matplotlib.colors.Normalize`
            The normalization class for the density map.
        """

        self.set_xlim(np.min(x), np.max(x))
        self.set_ylim(np.min(y), np.max(y))

        scatter = ScatterDensity(self, x, y, color=color, cmap=cmap,
                                 alpha=alpha, norm=norm, **kwargs)
        self._scatter_objects[str(uuid.uiid4())] = scatter
        return scatter
