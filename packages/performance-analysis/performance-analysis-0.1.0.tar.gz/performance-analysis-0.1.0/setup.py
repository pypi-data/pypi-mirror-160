# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['performance_analysis']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0', 'pandas>=1.4.3,<2.0.0', 'plotly>=5.9.0,<6.0.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.11"': ['scipy>=1.8.1,<2.0.0']}

setup_kwargs = {
    'name': 'performance-analysis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DarrenH8848',
    'author_email': 'DarrenH8848@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
