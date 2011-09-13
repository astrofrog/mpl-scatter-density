About
-----

The raster_axes file defines a RasterAxes class that inherits from
Axes, and adds a rasterized_scatter method that can plot millions of
points. This version is preliminary, and ideally this will in future
support all the options that scatter does, including symbols, alpha,
etc. Contributions via pull requests are welcome!

Example
-------

The file example.py contains a demonstration of the RasterAxes class.
To run, launch ipython:

    $ ipython -pylab

Then type:

    In [1]: execfile('example.py')

You can then pan and zoom as normal in the interactive Matplotlib
window.
