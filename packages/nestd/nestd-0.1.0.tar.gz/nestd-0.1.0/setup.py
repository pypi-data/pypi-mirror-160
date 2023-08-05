# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nestd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nestd',
    'version': '0.1.0',
    'description': 'A package to extract your nested functions!',
    'long_description': None,
    'author': 'Sanskar Jethi',
    'author_email': 'sansyrox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
