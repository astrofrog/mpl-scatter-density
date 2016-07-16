import numpy as np

import matplotlib.pyplot as plt
from astropy.table import Table

from raster_axes import RasterAxes

from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

fig = plt.figure()
ax = RasterAxes(fig, [0.1, 0.1, 0.8, 0.8], aspect='equal')
fig.add_axes(ax)

xmin = -8240227.037
ymin = 4974203.152
xmax = -8231283.905
ymax = 4979238.441

arrays = np.load('taxi.npz')
x = arrays['x']
y = arrays['y']

ax.rasterized_scatter(x, y, colormap='plasma', norm=norm)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal')

plt.show()