# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dainik']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3.0.3', 'nbox>=0.9.14rc28,<0.10.0']

setup_kwargs = {
    'name': 'dainik',
    'version': '0.4',
    'description': 'Client library for working with nimblebox LMAO',
    'long_description': None,
    'author': 'yashbonde',
    'author_email': 'bonde.yash97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
