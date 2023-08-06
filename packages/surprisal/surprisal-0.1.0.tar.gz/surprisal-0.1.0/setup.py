# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surprisal']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'plotext>=5.0.2,<6.0.0',
 'torch>=1.12.0,<2.0.0',
 'transformers>=4.20.1,<5.0.0']

setup_kwargs = {
    'name': 'surprisal',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aalok-sathe',
    'author_email': 'asathe@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
