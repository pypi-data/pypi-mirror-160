# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dgad', 'dgad.grpc', 'dgad.label_encoders', 'dgad.models']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'grpcio>=1.47.0,<2.0.0',
 'keras-tcn>=3.4.4,<4.0.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'tensorflow>=2.9.1,<3.0.0',
 'tldextract>=3.3.1,<4.0.0']

entry_points = \
{'console_scripts': ['dgad = dgad.cli:cli']}

setup_kwargs = {
    'name': 'dgad',
    'version': '4.0.0',
    'description': 'Classifies DGA domains',
    'long_description': None,
    'author': 'Federico Falconieri',
    'author_email': 'federico.falconieri@tno.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
