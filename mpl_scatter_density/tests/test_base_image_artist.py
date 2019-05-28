from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTk
from matplotlib.backends.backend_qt5 import FigureCanvasQT

from ..base_image_artist import supports_resize


def test_supports_resize():

    canvas = FigureCanvasAgg(Figure())
    assert not supports_resize(canvas)

    canvas = FigureCanvasTk(Figure())
    assert supports_resize(canvas)

    canvas = FigureCanvasQT(Figure())
    assert supports_resize(canvas)

    class SubclassA(FigureCanvasAgg):
        pass
    canvas = SubclassA(Figure())
    assert not supports_resize(canvas)

    class SubclassB(FigureCanvasQT):
        pass
    canvas = SubclassB(Figure())
    assert supports_resize(canvas)
