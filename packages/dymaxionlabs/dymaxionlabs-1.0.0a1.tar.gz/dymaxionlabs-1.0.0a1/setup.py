# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dymaxionlabs']

package_data = \
{'': ['*']}

install_requires = \
['google-resumable-media==0.5.1',
 'requests>=2.28.0,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'dymaxionlabs',
    'version': '1.0.0a1',
    'description': 'Python client for Dymaxion Labs Platform API',
    'long_description': None,
    'author': 'Damián Silvani',
    'author_email': 'munshkr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
