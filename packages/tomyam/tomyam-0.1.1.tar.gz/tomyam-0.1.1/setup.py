# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomyam', 'tomyam.assetmanager']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.39,<2.0.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'tomyam',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'monarchjuno',
    'author_email': 'monarchjuno@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
