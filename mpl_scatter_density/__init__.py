from .scatter_density_artist import *  # noqa
from .scatter_density_axes import *  # noqa

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('mpl-scatter-density').version
except DistributionNotFound:
    __version__ = 'undefined'
