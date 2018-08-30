from __future__ import division, print_function

import pytest
import numpy as np
import matplotlib.pyplot as plt

from ..scatter_density_axes import ScatterDensityAxes

from . import baseline_dir


class TestScatterDensityAxes(object):

    def setup_class(self):
        np.random.seed(12345)
        self.x1 = np.random.normal(0, 1, 10000000)
        self.y1 = np.random.normal(0, 1, 10000000)
        self.x2 = np.random.normal(3, 1, 10000000)
        self.y2 = np.random.normal(0, 1, 10000000)

    def setup_method(self, method):
        self.fig = plt.figure(figsize=(3, 3))

    def teardown_method(self, method):
        plt.close(self.fig)

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_axes_basic(self):
        self.ax = ScatterDensityAxes(self.fig, [0.15, 0.15, 0.8, 0.8])
        self.fig.add_axes(self.ax)
        self.ax.scatter_density(self.x1, self.y1)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_axes_projection(self):
        self.ax = self.fig.add_subplot(1, 1, 1, projection='scatter_density')
        self.ax.scatter_density(self.x1, self.y1, color='red', alpha=0.7)
        return self.fig
