# TODO: this is not yet functional

import numpy as np

import matplotlib.pyplot as plt

# The following is needed to register the axes
import mpl_scatter_density  # noqa

ax = plt.subplot(1, 1, 1, projection='scatter_density')

n = 1000000
x = np.random.normal(0.5, 0.3, n)
y = np.random.normal(0.5, 0.3, n)

ax.scatter_density(x, y, color='red')

n = 1000000
x = np.random.normal(0.5, 0.2, n)
y = np.random.normal(0.5, 0.2, n)

ax.scatter_density(x, y, color='green')

plt.show()
