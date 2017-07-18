import numpy as np
import matplotlib.pyplot as plt

from ..scatter_density import ScatterDensity


class TestScatterDensity(object):

    def setup_method(self, method):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        np.random.seed(12345)
        self.x = np.random.normal(0, 1, 100000)
        self.y = np.random.normal(0, 1, 100000)

    def test_default(self):
        d = ScatterDensity(self.ax, self.x, self.y)
        self.fig.savefig('test.pdf', dpi=10)
