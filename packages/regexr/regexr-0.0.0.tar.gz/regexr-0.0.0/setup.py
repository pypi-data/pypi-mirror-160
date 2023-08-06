# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regexr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'regexr',
    'version': '0.0.0',
    'description': 'Regular expressions for humans',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
