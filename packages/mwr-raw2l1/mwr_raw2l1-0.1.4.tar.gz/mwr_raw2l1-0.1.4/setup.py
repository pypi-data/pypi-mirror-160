# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mwr_raw2l1',
 'mwr_raw2l1.measurement',
 'mwr_raw2l1.readers',
 'mwr_raw2l1.utils']

package_data = \
{'': ['*'],
 'mwr_raw2l1': ['config/*',
                'data/*',
                'data/attex/0-20000-0-99999/*',
                'data/attex/orig/*',
                'data/output/*',
                'data/radiometrics/0-20000-0-10393/*',
                'data/radiometrics/orig/*',
                'data/rpg/0-20000-0-06610/*',
                'data/rpg/orig/*',
                'logs/*']}

install_requires = \
['PyYAML>=6,<7',
 'ephem>=4.1,<5.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy>=1.21,<2.0',
 'scipy>=1.7.3,<2.0.0',
 'xarray>=0.20.2,<0.21.0']

extras_require = \
{'colorlog': ['colorlog>=6.6,<7.0']}

entry_points = \
{'console_scripts': ['mwr_raw2l1 = mwr_raw2l1.__main__:main']}

setup_kwargs = {
    'name': 'mwr-raw2l1',
    'version': '0.1.4',
    'description': 'Readers for the most prominent types of operational ground-based K- and V-band microwave radiometers and a writer for NetCDF files according to E-PROFILE/ACTRIS standards.',
    'long_description': None,
    'author': 'Rolf Rüfenacht',
    'author_email': 'rruefenacht@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
