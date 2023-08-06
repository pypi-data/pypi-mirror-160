# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbnu', 'tbnu.aesthetics']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'art>=5.6,<6.0']

entry_points = \
{'console_scripts': ['tbnu = tbnu:main']}

setup_kwargs = {
    'name': 'tbnu',
    'version': '1.0.0',
    'description': 'TBNU is a super simple and easy to use CLI notes application',
    'long_description': None,
    'author': 'Abdullah Mohammed',
    'author_email': 'aamohammed4556@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
