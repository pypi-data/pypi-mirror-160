# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conf2env']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'conf2env',
    'version': '0.0.1b2',
    'description': '',
    'long_description': None,
    'author': 'jmarkin',
    'author_email': 'me@jmarkin.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
