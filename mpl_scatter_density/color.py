import matplotlib.colors as colors

__all__ = ['make_cmap']


def make_cmap(color):

    r, g, b = colors.colorConverter.to_rgb(color)

    cdict = {'red': [(0.0, 1.0, 1.0),
                     (1.0, r, r)],

             'green': [(0.0, 1.0, 1.0),
                       (1.0, g, g)],

             'blue':  [(0.0, 1.0, 1.0),
                       (1.0, b, b)]}

    return colors.LinearSegmentedColormap('custom', cdict)
