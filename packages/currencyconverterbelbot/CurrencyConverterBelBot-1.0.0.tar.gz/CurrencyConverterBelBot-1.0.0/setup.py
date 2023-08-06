# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['currencyconverterbelbot']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.21,<3.0',
 'black>=22.6.0,<23.0.0',
 'bs4>=0.0.1,<0.0.2',
 'lxml>=4.9.1,<5.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'currencyconverterbelbot',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'andrei',
    'author_email': 'dorofeichik9723@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
