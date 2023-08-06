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
    'version': '0.1.0',
    'description': 'Instantiate a playwright chromium (sync as opposed to async) browser',
    'long_description': '# get-pwbrowser-sync\n<!--- get-pwbrowser  get_pwbrowser  get_pwbrowser get_pwbrowser --->\n[![tests](https://github.com/ffreemt/get-pwbrowser-sync/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/get_pwbrowser_sync.svg)](https://badge.fury.io/py/get_pwbrowser_sync)\n\nInstantiate a playwright firefox sync (as opposed to async) browser\n\n## Installation\n```bash\npip install get-pwbrowser-sync\n\n# or\n# pip install git+https://github.com/ffreemt/get-pwbrowser-sync.git\n# python -m playwright install chromium\n```\n<details>\n<summary>or via poetry</summary>\n<code style="white-space:wrap;">\npoetry add git+https://github.com/ffreemt/get-pwbrowser-sync.git &&\npython -m playwright install chromium\n</code></details>\n\n## Usage\n\n```python\nfrom get_pwbrowser_sync import get_pwbrowser_sync\n\nbrowser = get_pwbrowser_sync()\npage = browser.new_page()\npage.goto("http://www.baidu.com")\nprint(page.title())\n# \'百度一下，你就知道\'\n```\n\n## Use of `.env` and `os.environ`\nThe browser can be run in a headful manner (to actually see what\'s going on):\n```\nfrom get_pwbrowser_sync import get_pwbrowser_sync\nbrowser = get_pwbrowser_sync(headless=False)\n\n```\n\nSome related parameters `HEADFUL`, `DEBUG` and `PROXY` can be set in shell environ or in .env with prefix `PWBROWSER_`.\n\ne.g., `set PWBROWSER_HEADFUL=1` in Windows or `export PWBROWSER_HEADFUL=1` in Linux and freinds)\n\nor in `.env`\n```bash\n# .env\nPWBROWSER_HEADFUL=1\n```\n\nFor more details have a look at the source code.',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/get-pwbrowser-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
