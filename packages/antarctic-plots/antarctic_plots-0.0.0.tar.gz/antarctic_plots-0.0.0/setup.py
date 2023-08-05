# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antarctic_plots', 'antarctic_plots.tests']

package_data = \
{'': ['*']}

install_requires = \
['netCDF4>=1.6.0,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pooch>=1.6.0,<2.0.0',
 'pygmt>=0.7.0,<0.8.0',
 'pyproj>=3.3.1,<4.0.0',
 'rioxarray>=0.11.1,<0.12.0',
 'verde>=1.7.0,<2.0.0',
 'xarray>=2022.3.0,<2023.0.0']

setup_kwargs = {
    'name': 'antarctic-plots',
    'version': '0.0.0',
    'description': 'Functions to automate Antarctic data visualization',
    'long_description': "# Antarctic-plots\nFunctions to automate Antarctic data visualization\n\n![](cover_fig.png)\n\n## Disclaimer\n\n🚨 **This package is in early stages of design and implementation.** 🚨\n\nI welcome any feedback, ideas, or contributions! Please submit an [issue on Github](https://github.com/mdtanker/antarctic_plots/issues) for problems or feature ideas. \n\n## About\n\nThis python package provides some basic tools for creating maps and plots specific to Antarctica. It includes code to download common continent-wide datasets (i.e. Bedmap2, AntGG, ADMAP), and visualize them in a variety of ways, including cross sections and maps. The Jupyter notebook [examples/examples.ipynb](https://github.com/mdtanker/antarctic_plots/blob/main/examples/examples.ipynb) runs through some of the main functions and usages of this package.\n\nBy default the cross-sections include Bedmap2 surface, icebase, and bed as layers, and the data profiles include Free-air gravity and magnetics, but these can be changed to any data, as long as it's supplied as a grid/raster type of file.\n\nData are sampled along lines either defined by 2 sets of coordinates, or along the path of a shapefile. \n\nFeel free to use, share, modify, and contribute to this project. I've mostly made this for private usage so for now the documentation is sparse. \n",
    'author': 'Matt Tankersley',
    'author_email': 'matt.d.tankersley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
