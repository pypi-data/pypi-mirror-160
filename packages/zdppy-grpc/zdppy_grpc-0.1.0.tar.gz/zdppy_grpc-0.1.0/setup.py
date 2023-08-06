# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_grpc', 'zdppy_grpc.health', 'zdppy_grpc.health.v1']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-tools>=1.45.0,<2.0.0', 'grpcio>=1.45.0,<2.0.0']

setup_kwargs = {
    'name': 'zdppy-grpc',
    'version': '0.1.0',
    'description': '基于gRPC的Python微服务开发框架',
    'long_description': None,
    'author': 'zhangdapeng520',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
