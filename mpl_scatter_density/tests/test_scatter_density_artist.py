from __future__ import division, print_function

import time
from mock import MagicMock
import pytest
import numpy as np
import matplotlib.pyplot as plt

try:
    import astropy  # noqa
except ImportError:  # pragma: nocover
    ASTROPY_INSTALLED = False
else:
    ASTROPY_INSTALLED = True

from ..scatter_density_artist import ScatterDensityArtist

from . import baseline_dir


class TestScatterDensity(object):

    def setup_class(self):
        np.random.seed(12345)
        self.x1 = np.random.normal(0, 1, 10000000)
        self.y1 = np.random.normal(0, 1, 10000000)
        self.x2 = np.random.normal(3, 1, 10000000)
        self.y2 = np.random.normal(0, 1, 10000000)
        self.c = self.x1 * self.y1

    def setup_method(self, method):
        self.fig = plt.figure(figsize=(3, 3))
        self.ax = self.fig.add_axes([0.13, 0.13, 0.8, 0.8])

    def teardown_method(self, method):
        plt.close(self.fig)

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
    @pytest.mark.parametrize('log', [True, False])
    def test_downres(self, log):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10)
        self.ax.add_artist(a)
        self.ax.figure.canvas.toolbar = MagicMock()
        self.ax.figure.canvas.toolbar.mode = 'pan/zoom'
        a.on_press()
        self.ax.set_xlim(0.1, 3.)
        self.ax.set_ylim(0.1, 3.)
        if log:
            self.ax.set_xscale('log')
            self.ax.set_yscale('log')
        return self.fig

    def test_no_dpi(self):
        # this is just to make sure things work, but can't do an image test
        # since dpi might be device-dependent
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, dpi=None)
        self.ax.add_artist(a)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    @pytest.mark.parametrize(('xscale', 'yscale'), [('linear', 'linear'), ('linear', 'log'),
                                                    ('log', 'linear'), ('log', 'log')])
    def test_scales(self, xscale, yscale):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10)
        self.ax.add_artist(a)
        self.ax.set_xlim(0.1, 10)
        self.ax.set_ylim(0.05, 8)
        self.ax.set_xscale(xscale)
        self.ax.set_yscale(yscale)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_colorcode(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10, c=self.c)
        self.ax.add_artist(a)
        self.ax.set_xlim(-5, 8)
        self.ax.set_ylim(-6.5, 6.5)
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_colorcode_downres(self):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10)
        a.set_c(self.c)  # do it this way to test setting c after the fact
        self.ax.add_artist(a)
        self.ax.set_xlim(-5, 8)
        self.ax.set_ylim(-6.5, 6.5)
        self.ax.figure.canvas.toolbar = MagicMock()
        self.ax.figure.canvas.toolbar.mode = 'pan/zoom'
        a.on_press()
        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    @pytest.mark.parametrize(('flipx', 'flipy'), [(False, False), (False, True),
                                                  (True, False), (True, True)])
    def test_flipping(self, flipx, flipy):
        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        if flipx:
            self.ax.set_xlim(5, -3)
        else:
            self.ax.set_xlim(-3, 5)
        if flipy:
            self.ax.set_ylim(6, -2)
        else:
            self.ax.set_ylim(-2, 6)
        return self.fig

    @pytest.mark.skipif('not ASTROPY_INSTALLED')
    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_norm(self):

        from astropy.visualization import LogStretch
        from astropy.visualization.mpl_normalize import ImageNormalize

        norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

        a = ScatterDensityArtist(self.ax, self.x1, self.y1, norm=norm)
        self.ax.add_artist(a)
        self.ax.set_xlim(-3, 5)
        self.ax.set_ylim(-2, 4)

        return self.fig

    @pytest.mark.mpl_image_compare(style={}, baseline_dir=baseline_dir)
    def test_manual_limits(self):

        a = ScatterDensityArtist(self.ax, self.x1, self.y1, vmin=-100, vmax=300)
        self.ax.add_artist(a)
        self.ax.set_xlim(-3, 5)
        self.ax.set_ylim(-2, 4)

        return self.fig

    @pytest.mark.parametrize('value', [-3, 0, 3.2])
    def test_invalid_downsample(self, value):

        with pytest.raises(ValueError) as exc:
            ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=value)
        assert exc.value.args[0] == 'downres_factor should be a strictly positive integer value'

    def test_downres_ignore_unity(self, tmpdir):

        # Make sure that when using a downres_factor of 1, we
        # are efficient and don't mark image as stale (which
        # would force a re-computation/draw)

        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=10)
        self.ax.add_artist(a)
        self.ax.figure.canvas.toolbar = MagicMock()
        self.ax.figure.canvas.toolbar.mode = 'pan/zoom'
        # We can't just draw, we need to save, as not all backends actually
        # draw when calling figure.canvas.draw()
        self.ax.figure.savefig(tmpdir.join('test1.png').strpath)
        assert not a.stale
        a.on_press()
        assert a.stale

        a = ScatterDensityArtist(self.ax, self.x1, self.y1, downres_factor=1)
        self.ax.add_artist(a)
        self.ax.figure.canvas.toolbar = MagicMock()
        self.ax.figure.canvas.toolbar.mode = 'pan/zoom'
        # We can't just draw, we need to save, as not all backends actually
        # draw when calling figure.canvas.draw()
        self.ax.figure.savefig(tmpdir.join('test2.png').strpath)
        assert not a.stale
        a.on_press()
        assert not a.stale

    def test_default_dpi(self, tmpdir):

        self.fig.set_dpi(90)
        a = ScatterDensityArtist(self.ax, self.x1, self.y1, dpi=None)
        self.ax.add_artist(a)
        # We can't just draw, we need to save, as not all backends actually
        # draw when calling figure.canvas.draw()
        self.ax.figure.savefig(tmpdir.join('test.png').strpath)
        assert a.get_size() == (216, 216)

    def test_downres_ignore_other_tools(self, tmpdir):

        # Make sure we ignore the downres if a tool other than pan/zoom is
        # selected (since the user may then be clicking on the canvas for
        # another reason)

        a = ScatterDensityArtist(self.ax, self.x1, self.y1)
        self.ax.add_artist(a)
        self.ax.figure.canvas.toolbar = MagicMock()
        self.ax.figure.canvas.toolbar.mode = 'apple picking'
        # We can't just draw, we need to save, as not all backends actually
        # draw when calling figure.canvas.draw()
        self.ax.figure.savefig(tmpdir.join('test.png').strpath)
        assert not a.stale
        a.on_press()
        assert not a.stale


def test_resize_qt():

    # This test just ensures that the code runs, but doesn't check for now
    # that the behavior is correct.

    from PyQt5.QtWidgets import QMainWindow

    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5 import FigureManagerQT
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    canvas.manager = FigureManagerQT(canvas, 0)  # noqa
    ax = fig.add_subplot(1, 1, 1)

    from matplotlib.backends.backend_qt5 import qApp

    window = QMainWindow()
    window.setCentralWidget(canvas)
    window.show()

    x1 = np.random.normal(0, 1, 10000000)
    y1 = np.random.normal(0, 1, 10000000)

    a = ScatterDensityArtist(ax, x1, y1)
    ax.add_artist(a)

    canvas.draw()
    assert not a.stale

    window.resize(300, 300)
    assert a.stale

    qApp.processEvents()
    assert not a.stale

    start = time.time()
    while time.time() - start < 1:
        qApp.processEvents()

    a.remove()
    qApp.processEvents()
