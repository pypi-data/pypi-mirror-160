# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywidevine']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'lxml>=4.9.1,<5.0.0',
 'protobuf==3.19.3',
 'pycryptodome>=3.15.0,<4.0.0',
 'pymp4>=1.2.0,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['pywidevine = pywidevine.main:main']}

setup_kwargs = {
    'name': 'pywidevine',
    'version': '1.0.0',
    'description': 'Widevine CDM (Content Decryption Module) implementation in Python.',
    'long_description': None,
    'author': 'rlaphoenix',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
