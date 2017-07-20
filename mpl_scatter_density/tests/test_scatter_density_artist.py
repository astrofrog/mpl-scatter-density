from __future__ import division, print_function

import pytest
import numpy as np
import matplotlib.pyplot as plt

from ..scatter_density_artist import ScatterDensityArtist

from . import baseline_dir


class TestScatterDensity(object):

    def setup_class(self):
        np.random.seed(12345)
        self.x1 = np.random.normal(0, 1, 10000000)
        self.y1 = np.random.normal(0, 1, 10000000)
        self.x2 = np.random.normal(3, 1, 10000000)
        self.y2 = np.random.normal(0, 1, 10000000)

    def setup_method(self, method):
        self.fig = plt.figure(figsize=(3, 3))
        self.ax = self.fig.add_axes([0.13, 0.13, 0.8, 0.8])

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_default(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_remove(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        a.remove()
        return self.fig

    @pytest.mark.parametrize('origin', ['lower', 'upper'])
    @pytest.mark.mpl_image_compare(style={}, filename='test_origin.png', baseline_dir=baseline_dir)
    def test_origin(self, origin):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, origin=origin)
        self.ax.add_artist(a)
        self.ax.set_xlim(-2, 8)
        self.ax.set_ylim(-5, 10)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_image_settings(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', cmap=plt.cm.plasma)
        self.ax.add_artist(a)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_color(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', color='red')
        self.ax.add_artist(a)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_multi_scatter(self):

        a = ScatterDensityArtist(self.ax, self.x1, self.y1,
                                 interpolation='nearest', color='red')
        self.ax.add_artist(a)

        a = ScatterDensityArtist(self.ax, self.x2, self.y2,
                                 interpolation='nearest', color='blue')
        self.ax.add_artist(a)

        self.ax.set_xlim(-5, 8)
        self.ax.set_ylim(-6.5, 6.5)

        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_downres(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10)
        self.ax.add_artist(a)
        a.downres()
        return self.fig

    def test_no_dpi(self):
        # this is just to make sure things work, but can't do an image test
        # since dpi might be device-dependent
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, dpi=None)
        self.ax.add_artist(a)
        return self.fig
