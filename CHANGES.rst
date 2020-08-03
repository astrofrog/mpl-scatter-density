0.7 (2020-08-03)
----------------

- Fix compatibility with Matplotlib 3.3. [#30]

- Drop support for Python 2.7 and require Matplotlib>=3. [#30]

- Update package infrastructure. [#31]

0.6 (2019-05-28)
----------------

- Avoid unecessary imports of Qt and Tk. [#27]

0.5 (2019-01-27)
----------------

- Internal code reorganization to faciliate re-use in other
  packages. [#26]

0.4 (2018-09-04)
----------------

- Added a keyword argment ``update_while_panning`` to set whether to
  compute the scatter denstiy map while panning and zooming. [#16]

- Downsample when resizing interactive window. [#14]

0.3 (2017-10-29)
----------------

- Added support for the ``c=`` argument, similar to the argument with
  the same name in Matplotlib's ``scatter`` function. [#11]

- Added support for log axes. [#11]

- Fixed support for flipped limits (e.g. xmax < xmin). [#11]

- Added support for setting vmin/vmax to functions to determine limits
  on-the-fly. [#11]

0.2 (2017-07-20)
----------------

- Fix compatibility with the Jupyter notebook. [#8]

0.1 (2017-07-19)
----------------

- Initial version.
