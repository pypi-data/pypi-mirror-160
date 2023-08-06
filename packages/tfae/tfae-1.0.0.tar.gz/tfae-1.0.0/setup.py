# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfae',
 'tfae.bottlenecks',
 'tfae.models',
 'tfae.regularizers',
 'tfae.schedulers']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'tfae',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Artem Legotin',
    'author_email': 'hello@artemlegotin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
