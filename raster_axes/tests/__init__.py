import os

from distutils.version import LooseVersion

import matplotlib

MPL_VERSION = LooseVersion(matplotlib.__version__)

baseline_root = 'baseline'

if MPL_VERSION >= LooseVersion('2'):
    baseline_subdir = '2.0.x'
elif MPL_VERSION >= LooseVersion('1.5'):
    baseline_subdir = '1.5.x'
else:
    raise ValueError('Matplotlib {0} is not supported'.format(matplotlib.__version__))

baseline_dir = os.path.join(baseline_root, baseline_subdir)
