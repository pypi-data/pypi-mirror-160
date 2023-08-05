# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils']

package_data = \
{'': ['*'], 'utils': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'friktion-research-utils',
    'version': '0.0.22',
    'description': 'Friktion research toolkit',
    'long_description': '',
    'author': 'thiccythot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://app.friktion.fi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
