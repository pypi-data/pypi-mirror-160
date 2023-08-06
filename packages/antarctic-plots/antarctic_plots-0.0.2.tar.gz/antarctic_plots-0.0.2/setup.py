# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antarctic_plots', 'antarctic_plots.tests']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.11.0,<0.12.0',
 'jupyter-book>=0.13.0,<0.14.0',
 'netCDF4>=1.6.0,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pooch>=1.6.0,<2.0.0',
 'pyproj>=3.3.1,<4.0.0',
 'rioxarray>=0.11.1,<0.12.0',
 'verde>=1.7.0,<2.0.0',
 'xarray>=2022.6.0,<2023.0.0']

setup_kwargs = {
    'name': 'antarctic-plots',
    'version': '0.0.2',
    'description': 'Functions to automate Antarctic data visualization',
    'long_description': None,
    'author': 'mdtanker',
    'author_email': 'matt.d.tankersley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
