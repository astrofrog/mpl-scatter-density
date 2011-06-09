import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
import matplotlib.colors as colors


def make_colormap(color):

    r, g, b = colors.colorConverter.to_rgb(color)

    cdict = {'red': [(0.0, r, r),
                    (1.0, 1.0, 1.0)],

             'green': [(0.0, g, g),
                       (1.0, 1.0, 1.0)],

             'blue':  [(0.0, b, b),
                       (1.0, 1.0, 1.0)]}

    return colors.LinearSegmentedColormap('custom', cdict)


class RasterAxes(plt.Axes):

    def __init__(self, *args, **kwargs):
        plt.Axes.__init__(self, *args, **kwargs)
        self.callbacks.connect('ylim_changed', self._update_all_scatter)
        self._scatter_objects = []
        self._scatter_images = {}

    def scatter(self, x, y, c='red'):
        scatter = (x, y, c)
        self._scatter_objects.append(scatter)
        self._update_scatter(scatter)

    def _update_all_scatter(self, event):
        for scatter in self._scatter_objects:
            self._update_scatter(scatter)

    def _update_scatter(self, scatter):

        x, y, c = scatter

        dpi = self.figure.get_dpi()

        autoscale = self.get_autoscale_on()

        if autoscale:
            self.set_autoscale_on(False)

        width = self.get_position().width * self.figure.get_figwidth()
        height = self.get_position().height * self.figure.get_figheight()

        nx = int(round(width * dpi))
        ny = int(round(height * dpi))

        xmin, xmax = self.get_xlim()
        ymin, ymax = self.get_ylim()

        ix = ((x - xmin) / (xmax - xmin) * float(nx)).astype(int)
        iy = ((y - ymin) / (ymax - ymin) * float(ny)).astype(int)

        array = ma.zeros((nx, ny), dtype=int)

        keep = (ix >= 0) & (ix < nx) & (iy >= 0) & (iy < ny)

        array[ix[keep], iy[keep]] += 1

        array = array.transpose()

        array.mask = array == 0

        if id(x) in self._scatter_images:
            self._scatter_images[id(x)].set_data(array)
            self._scatter_images[id(x)].set_extent([xmin, xmax, ymin, ymax])
        else:
            self._scatter_images[id(x)] = self.imshow(array, extent=[xmin, xmax, ymin, ymax], aspect='auto', cmap=make_colormap(c), interpolation='nearest')

        if autoscale:
            self.set_autoscale_on(True)

if __name__ == "__main__":

    fig = plt.figure()
    ax = RasterAxes(fig, [0.1, 0.1, 0.8, 0.8])
    fig.add_axes(ax)

    n = 1000000
    x = np.random.random(n)
    y = np.random.random(n)

    ax.scatter(x, y, c='red')

    n = 1000000
    x = np.random.random(n)
    y = np.random.random(n)

    ax.scatter(x, y, c='green')

    fig.canvas.draw()
