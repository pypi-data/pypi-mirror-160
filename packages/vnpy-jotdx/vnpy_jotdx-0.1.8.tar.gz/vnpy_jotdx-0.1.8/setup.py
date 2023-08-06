# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vnpy_jotdx']

package_data = \
{'': ['*']}

install_requires = \
['joconst>=0.1.14,<0.2.0', 'jotdx>=0.1.16,<0.2.0']

setup_kwargs = {
    'name': 'vnpy-jotdx',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'FangyangJz',
    'author_email': 'fangyang.jing@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
