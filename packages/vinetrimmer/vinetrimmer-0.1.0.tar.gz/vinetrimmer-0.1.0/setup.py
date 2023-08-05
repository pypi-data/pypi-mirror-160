# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vinetrimmer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vinetrimmer',
    'version': '0.1.0',
    'description': 'Reserved.',
    'long_description': None,
    'author': 'rlaphoenix',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
