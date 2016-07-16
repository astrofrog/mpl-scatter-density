import os

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("histogram2d", ["histogram2d.pyx"],
        include_dirs = [np.get_include()])
]

setup(
    name = "histogram2d",
    ext_modules = cythonize(extensions),
    )