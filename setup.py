from setuptools import setup, find_packages

setup(name='mpl-scatter-density',
      version='0.7.dev0',
      description='Matplotlib helpers to make density scatter plots',
      long_description=open('README.rst').read(),
      install_requires=['numpy', 'matplotlib>=3.0', 'fast-histogram>=0.3'],
      python_requires='>=3.6',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      license='BSD',
      url='https://github.com/astrofrog/mpl-scatter-density',
      package_data={'mpl_scatter_density.tests': ['baseline/*/*.png']},
      packages=find_packages())
