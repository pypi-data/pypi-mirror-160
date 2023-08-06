# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_pwbrowser_sync']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.6.3,<2.0.0',
 'playwright[chromium]>=1.24.0,<2.0.0',
 'pydantic[dotenv]>=1.8.1,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'typing-extensions==3.10.0.0']

setup_kwargs = {
    'name': 'get-pwbrowser-sync',
    'version': '0.1.0a1',
    'description': 'Instantiate a playwright chromium (sync as opposed to async) browser',
    'long_description': None,
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
