# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdispyutils',
 'cdispyutils.auth',
 'cdispyutils.config',
 'cdispyutils.hmac4',
 'cdispyutils.profiling']

package_data = \
{'': ['*'], 'cdispyutils.profiling': ['images/*']}

install_requires = \
['Flask', 'PyJWT', 'cdiserrors>=1.0.0,<2.0.0', 'cryptography>=3.2', 'requests']

setup_kwargs = {
    'name': 'cdispyutils',
    'version': '2.0.1',
    'description': 'This package includes several utility Python tools for the Gen3 stack.',
    'long_description': None,
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
