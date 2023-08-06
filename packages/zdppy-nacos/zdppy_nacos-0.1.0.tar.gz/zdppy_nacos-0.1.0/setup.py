# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_nacos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-nacos',
    'version': '0.1.0',
    'description': 'python使用nacos作为配置中心',
    'long_description': None,
    'author': 'zhangdapeng520',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
