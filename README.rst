About
-----

Plotting millions of points with Matplotlib can be slow. Real slow. Matplotlib
is extremely versatile, but the cost is performance, and sometim



The **mpl-scatter-density** mini-package provides functionality to make it easy
to make your own scatter density maps, both for interactive and non-interactive
use. Fast. The following animation shows real-time interactive use with 10
million points, but interactive performance is still good even with 100 million
points (and more if you have enough RAM).

.. figure:: https://github.com/astrofrog/mpl-scatter-density/raw/readme/demo_taxi.gif
   :alt: Demo of mpl-scatter-density with NY taxi data

When panning, the density map is shown at a lower resolution to keep things
responsive (though this is customizable).

Usage
-----

There are two main ways to use **mpl-scatter-density**, both of which are
explained below.

scatter_density method
~~~~~~~~~~~~~~~~~~~~~~

The easiest way to use this package is to simply import ``mpl_scatter_density``,
then create Matplotlib axes as usual but adding a
``projection='scatter_density'`` option (if your reaction is 'wait, what?', see
the Q&A below). This will return a ``ScatterDensityAxes`` instance that has a
``scatter_density`` method in addition to all the usual methods (``scatter``,
``plot``, etc.).

```python
import numpy as np
import mpl_scatter_density
import matplotlib.pyplot as plt

# Generate fake data

N = 10000000
x = np.random.normal(4, 2, N)
y = np.random.normal(3, 1, N)

# Make the plot - note that for the projection option to work, the
# mpl_scatter_density module has to be imported above.

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
ax.scatter_density(x, y)
ax.set_xlim(-5, 10)
ax.set_ylim(-5, 10)
fig.savefig('gaussian.png')
```

The ``scatter_density`` method takes the same options as ``imshow`` (for example
``cmap``, ``alpha``, ``norm``, etc.), but also takes the following optional
arguments:

* ``dpi``: this is an integer that is used to determine the resolution of the
  density map. By default, this is 72, but you can change it as needed, or set
  it to ``None`` to use the default for the Matplotlib backend you are using.

* ``downres_factor``: this is an integer that is used to determine how much to
  downsample the density map when panning in interactive mode. Set this to 1
  if you don't want any downsampling.

* ``color``: this can be set to any valid matplotlib color, and will be used
  to automatically make a monochromatic colormap based on this color. The
  colormap will fade to transparent, which means that this mode is ideal when
  showing multiple density maps together.

ScatterDensityArtist
~~~~~~~~~~~~~~~~~~~~

If you are a more experienced Matplotlib user, you might want to use the
``ScatterDensityArtist`` directly (this is used behind the scenes in the
above example). To use this, initialize the ``ScatterDensityArtist`` with
the axes as first argument, followed by any arguments you would have passed
to ``scatter_density`` above (you can also take a look at the docstring for
``ScatterDensityArtist``). You should then add the artist to the axes:

```python
from mpl_scatter_density import ScatterDensityArtist
a = ScatterDensityArtist(ax, x, y)
ax.add_artist(a)
```
