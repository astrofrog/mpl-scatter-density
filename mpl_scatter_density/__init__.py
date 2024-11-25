from .scatter_density_artist import *  # noqa
from .scatter_density_axes import *  # noqa

try:
    from .version import version as __version__
except ImportError:
    __version__ = 'undefined'
