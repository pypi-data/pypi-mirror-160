# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['capylang']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'capylang',
    'version': '0.10.3',
    'description': "Python's little programming language.",
    'long_description': None,
    'author': 'Kia Kazemi',
    'author_email': 'kia@anistick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
