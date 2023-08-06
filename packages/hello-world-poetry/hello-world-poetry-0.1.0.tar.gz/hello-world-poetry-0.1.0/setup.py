# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hello_world_poetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hello-world-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Claudia Quintana Wong',
    'author_email': 'cquintana@imantia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
