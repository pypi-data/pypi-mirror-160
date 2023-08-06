# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexis_uni_parser']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0', 'pandoc>=2.2,<3.0']

setup_kwargs = {
    'name': 'nexis-uni-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Garrett Shipley',
    'author_email': 'garrett.shipley7+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
