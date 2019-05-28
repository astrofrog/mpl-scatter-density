import pytest

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

try:
    from matplotlib.backends.backend_qt5 import FigureCanvasQT
except ImportError:
    QT_INSTALLED = False
else:
    QT_INSTALLED = True

from ..base_image_artist import supports_resize


def test_supports_resize():

    canvas = FigureCanvasAgg(Figure())
    assert not supports_resize(canvas)

    class SubclassA(FigureCanvasAgg):
        pass
    canvas = SubclassA(Figure())
    assert not supports_resize(canvas)


@pytest.mark.skipif('not QT_INSTALLED')
def test_supports_resize_qt():

    canvas = FigureCanvasQT(Figure())
    assert supports_resize(canvas)

    class SubclassB(FigureCanvasQT):
        pass
    canvas = SubclassB(Figure())
    assert supports_resize(canvas)
