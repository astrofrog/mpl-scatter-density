|Azure Status| |Coverage Status|

About
-----

Plotting millions of points can be slow. Real slow... :sleeping:

So why not use density maps? :zap:

The **mpl-scatter-density** mini-package provides functionality to make it easy
to make your own scatter density maps, both for interactive and non-interactive
use. Fast. The following animation shows real-time interactive use with 10
million points, but interactive performance is still good even with 100 million
points (and more if you have enough RAM).

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/main/images/demo_taxi.gif
   :alt: Demo of mpl-scatter-density with NY taxi data
   :align: center

When panning, the density map is shown at a lower resolution to keep things
responsive (though this is customizable).

To install, simply do::

    pip install mpl-scatter-density

This package requires `Numpy <http://www.numpy.org>`_, `Matplotlib
<http://www.matplotlib.org>`_, and `fast-histogram
<https://github.com/astrofrog/fast-histogram>`_ - these will be installed
by pip if they are missing. Both Python 2.7 and Python 3.x are supported,
and the package should work correctly on Linux, MacOS X, and Windows.

Usage
-----

There are two main ways to use **mpl-scatter-density**, both of which are
explained below.

scatter_density method
~~~~~~~~~~~~~~~~~~~~~~

The easiest way to use this package is to simply import ``mpl_scatter_density``,
then create Matplotlib axes as usual but adding a
``projection='scatter_density'`` option (if your reaction is 'wait, what?', see
`here <https://github.com/astrofrog/mpl-scatter-density/blob/master/README.rst#why-on-earth-have-you-defined-scatter_density-as-a-projection>`_).
This will return a ``ScatterDensityAxes`` instance that has a
``scatter_density`` method in addition to all the usual methods (``scatter``,
``plot``, etc.).

.. code:: python

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

Which gives:

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/master/images/gaussian.png
   :alt: Result from the example script
   :align: center

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

Here is an example of using the ``color`` option:

.. code:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import mpl_scatter_density  # noqa

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')

    n = 10000000

    x = np.random.normal(0.5, 0.3, n)
    y = np.random.normal(0.5, 0.3, n)

    ax.scatter_density(x, y, color='red')

    x = np.random.normal(1.0, 0.2, n)
    y = np.random.normal(0.6, 0.2, n)

    ax.scatter_density(x, y, color='blue')

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)

    fig.savefig('double.png')

Which produces the following output:

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/master/images/double.png
   :alt: Result from the example script
   :align: center

ScatterDensityArtist
~~~~~~~~~~~~~~~~~~~~

If you are a more experienced Matplotlib user, you might want to use the
``ScatterDensityArtist`` directly (this is used behind the scenes in the
above example). To use this, initialize the ``ScatterDensityArtist`` with
the axes as first argument, followed by any arguments you would have passed
to ``scatter_density`` above (you can also take a look at the docstring for
``ScatterDensityArtist``). You should then add the artist to the axes:

.. code:: python

    from mpl_scatter_density import ScatterDensityArtist
    a = ScatterDensityArtist(ax, x, y)
    ax.add_artist(a)

Advanced
--------

Non-linear stretches for high dynamic range plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, your density map might have a high dynamic range, and you might
therefore want to show the log of the counts rather than the counts. You can do
this by passing a ``matplotlib.colors.Normalize`` object to the ``norm`` argument
in the same wasy as for ``imshow``. For example, the `astropy
<http://www.astropy.org>`_ package includes a `nice framework
<http://docs.astropy.org/en/stable/api/astropy.visualization.LogStretch.html#astropy.visualization.LogStretch>`_
for making such a ``Normalize`` object for different functions. The following
example shows how to show the density map on a log scale:

.. code:: python

    import numpy as np
    import mpl_scatter_density
    import matplotlib.pyplot as plt

    # Make the norm object to define the image stretch
    from astropy.visualization import LogStretch
    from astropy.visualization.mpl_normalize import ImageNormalize
    norm = ImageNormalize(vmin=0., vmax=1000, stretch=LogStretch())

    N = 10000000
    x = np.random.normal(4, 2, N)
    y = np.random.normal(3, 1, N)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    ax.scatter_density(x, y, norm=norm)
    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    fig.savefig('gaussian_log.png')

Which produces the following output:

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/master/images/gaussian_log.png
   :alt: Result from the example script
   :align: center

Adding a colorbar
~~~~~~~~~~~~~~~~~

You can show a colorbar in the same way as you would for an image - the
following example shows how to do it:

.. code:: python

    import numpy as np
    import mpl_scatter_density
    import matplotlib.pyplot as plt

    N = 10000000
    x = np.random.normal(4, 2, N)
    y = np.random.normal(3, 1, N)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y)
    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    fig.colorbar(density, label='Number of points per pixel')
    fig.savefig('gaussian_colorbar.png')

Which produces the following output:

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/master/images/gaussian_colorbar.png
   :alt: Result from the example script
   :align: center

Color-coding 'markers' with individual values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the same way that a 1-D array of values can be passed to Matplotlib's
``scatter`` function/method, a 1-D array of values can be passed to
``scatter_density`` using the ``c=`` argument:

.. code:: python

    import numpy as np
    import mpl_scatter_density
    import matplotlib.pyplot as plt

    N = 10000000
    x = np.random.normal(4, 2, N)
    y = np.random.normal(3, 1, N)
    c = x - y + np.random.normal(0, 5, N)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    ax.scatter_density(x, y, c=c, vmin=-10, vmax=+10, cmap=plt.cm.RdYlBu)
    ax.set_xlim(-5, 13)
    ax.set_ylim(-5, 11)
    fig.savefig('gaussian_color_coded.png')

Which produces the following output:

.. image:: https://github.com/astrofrog/mpl-scatter-density/raw/master/images/gaussian_color_coded.png
   :alt: Result from the example script
   :align: center

Note that to keep performance as good as possible, the values from the ``c``
attribute are averaged inside each pixel of the density map, then the colormap
is applied. This is a little different to what ``scatter`` would converge to in
the limit of many points (since in that case it would apply the color to all the
markers than average the colors).

Q&A
---

Isn't this basically the same as datashader?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This follows the same ideas as
`datashader <https://github.com/bokeh/datashader>`_, but the aim of
mpl-scatter-density is specifically to bring datashader-like functionality to
Matplotlib users. Furthermore, mpl-scatter-density is intended to be very easy
to install - for example it can be installed with pip. But if you have
datashader installed and regularly use bokeh, mpl-scatter-density won't do much
for you. Note that if you are interested in datashader and Matplotlib together,
there is a work in progress (`pull request
<https://github.com/bokeh/datashader/pull/200>`_) by **@tacaswell** to create a
Matplotlib artist similar to that in this package but powered by datashader.

What about vaex?
~~~~~~~~~~~~~~~~

`Vaex <http://vaex.astro.rug.nl>`_ is a powerful package to
visualize large datasets on N-dimensional grids, and therefore has some
functionality that overlaps with what is here. However, the aim of
mpl-scatter-density is just to provide a lightweight solution to make
it easy for users already using Matplotlib
to add scatter density maps to their plots rather than provide a complete
environment for data visualization. I highly recommend that you take a look
at Vaex and determine which approach is right for you!

Why on earth have you defined scatter_density as a projection?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are a Matplotlib developer: I truly am sorry for distorting the intended
purpose of ``projection`` :blush:. But you have to admit that it's a pretty
convenient way to have users get a custom Axes sub-class even if it has nothing
to do with actual projection!

Where do you see this going?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of things we could add to this package, for example a way to
plot density maps as contours, or a way to color code each point by a third
quantity and have that reflected in the density map. If you have ideas, please
open issues, and even better contribute a pull request! :smile:

Can I contribute?
~~~~~~~~~~~~~~~~~

I'm glad you asked - of course you are very welcome to contribute! If you have
some ideas, you can open issues or create a pull request directly. Even if you
don't have time to contribute actual code changes, I would love to hear from you
if you are having issues using this package.

[![Build Status](https://dev.azure.com/thomasrobitaille/mpl-scatter-density/_apis/build/status/astrofrog.mpl-scatter-density?branchName=master)](https://dev.azure.com/thomasrobitaille/mpl-scatter-density/_build/latest?definitionId=17&branchName=master)

.. |Azure Status| image:: https://dev.azure.com/thomasrobitaille/mpl-scatter-density/_apis/build/status/astrofrog.mpl-scatter-density?branchName=master
   :target: https://dev.azure.com/thomasrobitaille/mpl-scatter-density/_build/latest?definitionId=17&branchName=master

.. |Coverage Status| image:: https://codecov.io/gh/astrofrog/mpl-scatter-density/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/astrofrog/mpl-scatter-density
  
Running tests
-------------

To run the tests, you will need `pytest <https://docs.pytest.org/en/latest/>`_
and the `pytest-mpl <https://pypi.python.org/pypi/pytest-mpl>`_ plugin. You can
then run the tests with::

    pytest mpl_scatter_density --mpl
