# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qloader']

package_data = \
{'': ['*']}

install_requires = \
['imagehash', 'pillow', 'requests', 'selenium']

setup_kwargs = {
    'name': 'qloader',
    'version': '8.1.5',
    'description': 'Gather results from some search engine',
    'long_description': None,
    'author': 'tasker',
    'author_email': 'tasker@ialcloud.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
