from .scatter_density_artist import *  # noqa
from .scatter_density_axes import *  # noqa

import sys
if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version

__version__ = version("mpl-scatter-density")
del version, sys
