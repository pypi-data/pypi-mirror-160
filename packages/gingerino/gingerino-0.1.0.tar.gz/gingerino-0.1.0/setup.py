# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gingerino']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gingerino',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marco Burro',
    'author_email': 'marcoburro98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
