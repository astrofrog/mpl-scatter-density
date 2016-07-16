import os

import numpy as np
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions=[
    Extension("histogram2d", [os.path.join('raster_scatter', 'histogram2d.pyx')],
              include_dirs=[np.get_include()])
]

setup(name='raster-scatter',
      version='0.1.dev0',
      install_requires=['numpy', 'Cython'],
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='BSD',
      url='https://github.com/astrofrog/rasterized_scatter',
      package='raster_scatter',
      ext_modules=cythonize(extensions),
)
