# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorm', 'pytorm.repository']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.37,<2.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'multimethod>=1.8,<2.0']

setup_kwargs = {
    'name': 'pytorm',
    'version': '0.0.4',
    'description': 'Implementation of repository pattern over SQLAlchemy',
    'long_description': '# PytORM\n\n[![Release](https://img.shields.io/github/release/flaiers/pytorm.svg)](https://github.com/flaiers/pytorm/releases/latest)\n[![Licence](https://img.shields.io/github/license/flaiers/pytorm)](https://github.com/flaiers/pytorm/blob/main/LICENSE)\n\n\n## Introduction\n\nImplementation of repository pattern over SQLAlchemy\n\n## Installation\n\n```shell\npoetry add pytorm\n```\n\n```shell\npip install pytorm\n```\n',
    'author': 'Maxim Bigin',
    'author_email': 'i@flaiers.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flaiers/pytorm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
