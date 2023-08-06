# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_correios']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'api-correios',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bruno Souza',
    'author_email': 'bruno.souza@zaxapp.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
