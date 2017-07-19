import numpy as np

import matplotlib.pyplot as plt

# The following is needed to register the axes
import mpl_scatter_density  # noqa

from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

ax = plt.subplot(1, 1, 1, projection='scatter_density')

n = 100000000
x = np.random.normal(0.5, 0.3, n)
y = np.random.normal(0.5, 0.3, n)

ax.scatter_density(x, y, cmap='viridis', norm=norm)

plt.show()
