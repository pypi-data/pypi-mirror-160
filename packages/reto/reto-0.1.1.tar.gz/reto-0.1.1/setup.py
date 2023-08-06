# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reto']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'mdweek>=1.2.4,<2.0.0',
 'mypy>=0.950,<0.951',
 'networkx>=2.8,<3.0',
 'pytest>=7.1.2,<8.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'reto',
    'version': '0.1.1',
    'description': 'A python package for programming in declarative style.',
    'long_description': None,
    'author': 'Yasunori Horikoshi',
    'author_email': 'hotoku@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
