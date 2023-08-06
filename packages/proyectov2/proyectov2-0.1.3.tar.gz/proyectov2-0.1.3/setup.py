# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proyectov2', 'proyectov2.acciones']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['webserver = proyectov2.main:main']}

setup_kwargs = {
    'name': 'proyectov2',
    'version': '0.1.3',
    'description': '',
    'long_description': '## Avance de proyecto de control remoto de dispositivo.',
    'author': 'Paul Orellana',
    'author_email': 'paorellana6@utpl.edu.ec',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
