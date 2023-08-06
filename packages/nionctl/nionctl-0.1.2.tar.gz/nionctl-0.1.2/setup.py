# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nionctl']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['nionctl = nionctl.main:main_app']}

setup_kwargs = {
    'name': 'nionctl',
    'version': '0.1.2',
    'description': '',
    'long_description': '# nionctl\n\nAn abbreviation of common linux utilities into a single cli',
    'author': '8Dion8',
    'author_email': 'shvartserinfo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
