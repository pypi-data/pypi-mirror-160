# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ports_v2_core',
 'ports_v2_core.rpc',
 'ports_v2_core.rpc.clients',
 'ports_v2_core.rpc.errors',
 'ports_v2_core.schemas']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-jsonrpc>=2.2.2,<3.0.0',
 'jsonrpcclient>=4.0.2,<5.0.0',
 'pydantic[email]>=1.9.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'ports-v2-core',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
