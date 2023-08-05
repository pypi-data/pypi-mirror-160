# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baseten', 'baseten.client_commands', 'baseten.common']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0',
 'colorama>=0.4.3',
 'coolname>=1.1.0',
 'jinja2>=2.10.3',
 'joblib>=0.12.5',
 'pyyaml>=5.1',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.22',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.62.1,<5.0.0',
 'truss>=0.0.28,<0.0.29']

entry_points = \
{'console_scripts': ['baseten = baseten.cli:cli_group']}

setup_kwargs = {
    'name': 'baseten',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Amir Haghighat',
    'author_email': 'amir@baseten.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
