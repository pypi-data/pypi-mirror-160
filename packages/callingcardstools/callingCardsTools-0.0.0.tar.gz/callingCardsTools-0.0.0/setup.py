# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['callingcardstools',
 'callingcardstools.bin',
 'callingcardstools.blockify',
 'callingcardstools.macs_style']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.30,<0.30.0',
 'biopython>=1.79,<2.0',
 'bx-python>=0.8.13,<0.9.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pybedtools>=0.9.0,<0.10.0',
 'pysam>=0.19.1,<0.20.0',
 'scipy>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['hello_world = callingcardstools:hello_world',
                     'macs_peak_caller = '
                     'callingcardstools.bin:macs_peak_caller.main']}

setup_kwargs = {
    'name': 'callingcardstools',
    'version': '0.0.0',
    'description': 'A collection of objects and functions to work with calling cards sequencing tools',
    'long_description': None,
    'author': 'chase mateusiak',
    'author_email': 'chase.mateusiak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
