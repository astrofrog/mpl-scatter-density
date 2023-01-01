import os

from packaging.version import Version

import matplotlib

MPL_VERSION = Version(matplotlib.__version__)

baseline_root = 'baseline'

if MPL_VERSION >= Version('3'):  # pragma: nocover
    baseline_subdir = '3.0.x'
else:  # pragma: nocover
    raise ValueError('Matplotlib {0} is not supported'.format(matplotlib.__version__))

baseline_dir = os.path.join(baseline_root, baseline_subdir)
