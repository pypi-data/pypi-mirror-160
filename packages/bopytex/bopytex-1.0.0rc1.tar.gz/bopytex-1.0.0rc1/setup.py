# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bopytex', 'bopytex.jinja2_env', 'bopytex.planner', 'bopytex.worker']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'bopytex',
    'version': '1.0.0rc1',
    'description': 'Command line tool for compiling latex with python command embedded',
    'long_description': None,
    'author': 'Bertrand Benjamin',
    'author_email': 'benjamin.bertrand@opytex.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
