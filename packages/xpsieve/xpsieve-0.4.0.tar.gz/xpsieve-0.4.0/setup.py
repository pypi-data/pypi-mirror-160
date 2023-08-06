# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpsieve']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xpsieve',
    'version': '0.4.0',
    'description': 'Additions to pandas for experiments handling (e.g. pd.read_wandb)',
    'long_description': None,
    'author': 'Damien Sileo',
    'author_email': 'damien.sileo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
