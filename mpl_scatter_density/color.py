from __future__ import division, print_function

import matplotlib.colors as colors

__all__ = ['make_cmap']


def make_cmap(color):

    r, g, b = colors.colorConverter.to_rgb(color)

    cdict = {'red': [(0.0, r, r),
                     (1.0, r, r)],

             'green': [(0.0, g, g),
                       (1.0, g, g)],

             'blue': [(0.0, b, b),
                      (1.0, b, b)],

             'alpha': [(0.0, 0.0, 0.0),
                       (1.0, 1.0, 1.0)]}

    return colors.LinearSegmentedColormap('custom', cdict)
