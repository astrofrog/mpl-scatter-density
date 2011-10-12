import numpy as np

import matplotlib.pyplot as plt

from raster_axes import RasterAxes

fig = plt.figure()
ax = RasterAxes(fig, [0.1, 0.1, 0.8, 0.8])
fig.add_axes(ax)

n = 1000000
x = np.random.normal(0.5, 0.3, n)
y = np.random.normal(0.5, 0.3, n)

ax.rasterized_scatter(x, y, colormap='jet')

fig.canvas.draw()
