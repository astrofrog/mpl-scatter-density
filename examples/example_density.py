import numpy as np

import matplotlib.pyplot as plt

from raster_axes import RasterAxes

from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

fig = plt.figure()
ax = RasterAxes(fig, [0.1, 0.1, 0.8, 0.8])
fig.add_axes(ax)

n = 10000000
x = np.random.normal(0.5, 0.3, n)
y = np.random.normal(0.5, 0.3, n)

ax.rasterized_scatter(x, y, colormap='viridis', norm=norm)

plt.show()