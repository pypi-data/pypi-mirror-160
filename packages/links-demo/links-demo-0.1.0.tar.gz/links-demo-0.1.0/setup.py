# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'links-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Patrick Arminio',
    'author_email': 'patrick.arminio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
