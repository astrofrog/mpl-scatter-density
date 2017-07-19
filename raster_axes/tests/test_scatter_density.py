import numpy as np
import matplotlib.pyplot as plt

from ..scatter_density import ScatterDensityArtist


class TestScatterDensity(object):

    def setup_class(self):
        np.random.seed(12345)
        self.x1 = np.random.normal(0, 1, 10_000_000)
        self.y1 = np.random.normal(0, 1, 10_000_000)
        self.x2 = np.random.normal(3, 1, 10_000_000)
        self.y2 = np.random.normal(0, 1, 10_000_000)

    def setup_method(self, method):
        self.fig = plt.figure(figsize=(3, 3))
        self.ax = self.fig.add_axes([0.13, 0.13, 0.8, 0.8])

    def test_default(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        self.fig.savefig('test.png')

    def test_remove(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        a.remove()
        self.fig.savefig('test.png')

    def test_image_settings(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', cmap=plt.cm.plasma)
        self.ax.add_artist(a)
        self.fig.savefig('test.png')

    def test_color(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', color='red')
        self.ax.add_artist(a)
        self.fig.savefig('test.png')

    def test_multi_scatter(self):

        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', color='red')
        self.ax.add_artist(a)

        a = ScatterDensityArtist(self.ax, self.x2, self.y2,
                                 interpolation='nearest', color='blue', alpha=0.5)
        self.ax.add_artist(a)

        self.ax.set_xlim(-5, 8)
        self.ax.set_ylim(-6.5, 6.5)

        self.fig.savefig('test.png')

    def test_downres(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        print('downres')
        a.downres()
        self.fig.savefig('test.png')
