0.6 (unreleased)
----------------

- Avoid unecessary imports of Qt and Tk. [#27]
No changes yet.

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
