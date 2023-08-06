# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['services', 'services.commands', 'services.db', 'services.security']

package_data = \
{'': ['*']}

install_requires = \
['sanic[ext]>=22.6.0,<23.0.0']

entry_points = \
{'console_scripts': ['srv = services.cli:cli']}

setup_kwargs = {
    'name': 'ai-services',
    'version': '0.1.0',
    'description': 'A simple web framework based on Sanic',
    'long_description': None,
    'author': 'nuxion',
    'author_email': 'nuxion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
