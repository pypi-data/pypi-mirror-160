# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weevils_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'weevils-cli',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'weevils.io',
    'author_email': 'code@weevils.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
