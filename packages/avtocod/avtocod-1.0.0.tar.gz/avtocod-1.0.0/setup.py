# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avtocod',
 'avtocod.methods',
 'avtocod.session',
 'avtocod.session.middlewares',
 'avtocod.types',
 'avtocod.types.profile',
 'avtocod.types.report',
 'avtocod.types.report.report_entities',
 'avtocod.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<1.10.0']

setup_kwargs = {
    'name': 'avtocod',
    'version': '1.0.0',
    'description': 'Avtocod - неофициальный, элегантный, асинхронный враппер автокода',
    'long_description': '***This version still in development***\n',
    'author': 'Fom123',
    'author_email': 'gamemode1.459@gmail.com',
    'maintainer': 'Fom123',
    'maintainer_email': 'gamemode1.459@gmail.com',
    'url': 'https://github.com/Fom123/avtocod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
