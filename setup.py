import os

import numpy as np
from setuptools import setup
from setuptools.extension import Extension


setup(name='raster-axes',
      version='0.1.dev0',
      install_requires=['numpy', 'matplotlib', 'fast-histogram'],
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='BSD',
      url='https://github.com/astrofrog/scatter-density',
      packages=['raster_axes']
)
