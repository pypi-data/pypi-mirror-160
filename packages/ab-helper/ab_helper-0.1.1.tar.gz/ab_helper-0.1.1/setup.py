# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factly',
 'factly.ab_helper',
 'factly.ab_helper.core',
 'factly.ab_helper.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'ab-helper',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Factly Labs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
