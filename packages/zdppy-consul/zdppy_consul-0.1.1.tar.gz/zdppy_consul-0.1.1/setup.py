# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_consul']

package_data = \
{'': ['*']}

install_requires = \
['zdppy-requests>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'zdppy-consul',
    'version': '0.1.1',
    'description': 'Python使用consul作为注册中心',
    'long_description': None,
    'author': 'zhangdapeng520',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
