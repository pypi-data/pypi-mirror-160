# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py2gsuite', 'py2gsuite.api', 'py2gsuite.utils']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0',
 'google-api-python-client>=2.52.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'py2gsuite',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'ktro2828',
    'author_email': 'kotaro.uetake@tier4.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
