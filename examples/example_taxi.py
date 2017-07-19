import os
import sys

import numpy as np

import matplotlib.pyplot as plt

# The following is needed to register the axes
import mpl_scatter_density  # noqa

from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

ax = plt.subplot(1, 1, 1, aspect='equal', projection='scatter_density')

xmin = -8240227.037
ymin = 4974203.152
xmax = -8231283.905
ymax = 4979238.441

if not os.path.exists('taxi.npz'):
    print("You need to run the convert_nyc.py script first")
    sys.exit(1)

arrays = np.load('taxi.npz')
x = arrays['x']
y = arrays['y']

ax.rasterized_scatter(x, y, colormap='plasma', norm=norm)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')

plt.show()
