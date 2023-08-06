# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybravia']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp']

setup_kwargs = {
    'name': 'pybravia',
    'version': '0.1.0',
    'description': 'Python async library for remote control of Sony Bravia TVs 2013 and newer.',
    'long_description': '# pybravia\n\n<img src="https://img.shields.io/pypi/v/pybravia" alt="PyPI Version"> <img src="https://img.shields.io/github/workflow/status/Drafteed/pybravia/CI" alt="GitHub Workflow Status"> <img src="https://img.shields.io/badge/code%20style-black-black" alt="Code style">\n\nPython 3 async library for remote control of Sony Bravia TVs 2013 and newer.\n\nFor more information on the API used in this library, refer to [BRAVIA Professional Display Knowledge Center](https://pro-bravia.sony.net/develop/index.html).\n',
    'author': 'Arem Draft',
    'author_email': 'artemon_93@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Drafteed/pybravia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
