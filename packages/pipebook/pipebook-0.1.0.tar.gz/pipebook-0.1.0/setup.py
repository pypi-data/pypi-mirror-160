# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipebook']

package_data = \
{'': ['*'], 'pipebook': ['resources/*']}

install_requires = \
['fridaay>=0.2.3,<0.3.0', 'toga==0.3.0.dev34']

setup_kwargs = {
    'name': 'pipebook',
    'version': '0.1.0',
    'description': 'Next-generation notebook for resilient, production-ready data pipelines',
    'long_description': None,
    'author': 'Ernest Prabhakar',
    'author_email': 'ernest.prabhakar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
