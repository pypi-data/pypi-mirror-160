# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finflow', 'finflow.src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'finflow',
    'version': '0.1.0',
    'description': 'Modular pipelines to create and backtest investment strategies',
    'long_description': None,
    'author': 'João Jacques',
    'author_email': 'joaopedro_jh@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
