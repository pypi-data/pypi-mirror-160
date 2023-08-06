# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpsieve']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xpsieve',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
