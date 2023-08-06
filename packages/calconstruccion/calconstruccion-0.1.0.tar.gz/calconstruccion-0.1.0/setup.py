# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calconstruccion', 'calconstruccion.utils']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'calconstruccion',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefy0408',
    'author_email': 'caroarevaldivieso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
