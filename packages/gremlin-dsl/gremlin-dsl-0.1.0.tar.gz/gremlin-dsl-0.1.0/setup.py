# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gremlin_dsl']

package_data = \
{'': ['*']}

install_requires = \
['gremlinpython>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'gremlin-dsl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Elliot Hershberg',
    'author_email': 'eahershberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
