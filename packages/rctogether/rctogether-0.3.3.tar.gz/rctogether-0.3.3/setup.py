# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rctogether']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'rctogether',
    'version': '0.3.3',
    'description': '',
    'long_description': None,
    'author': 'Adam Kelly',
    'author_email': 'adam@cthulahoops.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
