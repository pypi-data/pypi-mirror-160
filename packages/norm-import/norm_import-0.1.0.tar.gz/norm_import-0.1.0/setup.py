# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norm_import']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'norm-import',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ваше Имя',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
