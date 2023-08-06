# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mlengineerbelvo', 'mlengineerbelvo.config', 'mlengineerbelvo.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.36,<2.0.0',
 'feast>=0.22.1,<0.23.0',
 'mlflow>=1.27.0,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'python-json-config>=1.2.3,<2.0.0',
 'scikit-learn>=1.1.1,<2.0.0',
 'xgboost>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'mlengineerbelvo',
    'version': '0.1.0',
    'description': 'ML engineer Test Case - Belvo',
    'long_description': None,
    'author': 'Miguel Arquez Abdala',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
