# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gingerino']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gingerino',
    'version': '0.1.2',
    'description': 'Parse strings using Jinja-style templates',
    'long_description': '# Gingerino\n\n[![PyPI Version](https://img.shields.io/pypi/v/gingerino)](https://pypi.org/project/gingerino/)\n\nThis is a proof of concept\n\n## Usage\n\n```python\nfrom typing import Literal\n\nfrom gingerino import Gingerino\n\n\nclass UserInfo(Gingerino):\n    name: str\n    age: int\n    unit: Literal["years", "months"]\n\n\ntemplate = "{{ name }} is {{ age }} {{ unit }} old"\nuser = UserInfo(template)\n\nuser.parse("Marco is 24 years old")\n\nprint(user.name, user.age, user.unit)\n# Marco 24 years\n```\n',
    'author': 'Marco Burro',
    'author_email': 'marcoburro98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/buurro/gingerino',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
