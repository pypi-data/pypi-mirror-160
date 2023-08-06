# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_import']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0', 'pip>=22.1.1,<23.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['poetry-import = poetry_import.main:main']}

setup_kwargs = {
    'name': 'poetry-import',
    'version': '0.1.0',
    'description': 'CLI utility that helps you migrate from Python pip requirements to Poetry pyproject.toml + poetry.lock.',
    'long_description': None,
    'author': 'BrandonLWhite',
    'author_email': 'brandonlwhite@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
