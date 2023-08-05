# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scriptorium',
 'scriptorium.apps',
 'scriptorium.storage',
 'scriptorium.transformations']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.7,<2.0.0',
 'google-api-python-client>=2.0.2,<3.0.0',
 'google-auth-oauthlib>=0.4.3,<0.5.0',
 'google-auth>=2.0.0,<3.0.0',
 'google-cloud-bigquery-storage>=2.3.0,<3.0.0',
 'google-cloud-bigquery>=2.13.1,<3.0.0',
 'google-cloud-storage>=1.37.0,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pandasql>=0.7.3,<1.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'pygsheets>=2.0.5,<3.0.0',
 'pymssql>=2.2.0,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'setuptools>=54.2.0,<55.0.0',
 'slack-sdk>=3.18.0,<4.0.0']

setup_kwargs = {
    'name': 'datamonk-scriptorium',
    'version': '0.5.3',
    'description': '',
    'long_description': None,
    'author': 'Vit Mrnavek',
    'author_email': 'vit.mrnavek@datamonk.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
