# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiges', 'aiges.backup', 'aiges.cmd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiges',
    'version': '0.1.1',
    'description': "A module for test aiges's python wrapper.py",
    'long_description': None,
    'author': 'maybaby',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
