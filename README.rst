About
-----

The raster\_axes file defines a RasterAxes class that inherits from
Axes, and adds a rasterized\_scatter method that can plot millions of
points. This version is preliminary, and ideally this will in future
support all the options that scatter does, including symbols, alpha,
etc. Contributions via pull requests are welcome!

Example
-------

The ``examples`` directory contains a few examples of usage, for
instance an example of 10 million points sampled from a Gaussian::

::

    python examples_density.py

or the `NYC taxi data <http://www.andresmh.com/nyctaxitrips/>`__:

::

    python convert_nyc.py
    python examples_taxi.py

Note that the ``convert_nyc.py`` script requires a CSV file to be
present with at least the ``dropoff_x``, ``dropoff_y``, and
``trip_distance`` columns. The demo works well for 10 million poins, and
hasn't been tested above.

You can then pan and zoom as normal in the interactive Matplotlib
window.

.. figure:: screenshot.png
   :alt: nyc\_taxi

   nyc\_taxi
