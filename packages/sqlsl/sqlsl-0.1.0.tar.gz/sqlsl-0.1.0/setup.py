# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlsl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlsl',
    'version': '0.1.0',
    'description': 'SQL simple loader',
    'long_description': None,
    'author': 'pegov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pegov/sqlsl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
