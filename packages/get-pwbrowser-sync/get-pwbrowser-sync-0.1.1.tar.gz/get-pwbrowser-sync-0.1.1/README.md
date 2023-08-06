# get-pwbrowser-sync
<!--- get-pwbrowser  get_pwbrowser  get_pwbrowser get_pwbrowser --->
[![tests](https://github.com/ffreemt/get-pwbrowser-sync/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/get_pwbrowser_sync.svg)](https://badge.fury.io/py/get_pwbrowser_sync)

Instantiate a playwright firefox sync (as opposed to async) browser

## Installation
```bash
pip install get-pwbrowser-sync

# or
# pip install git+https://github.com/ffreemt/get-pwbrowser-sync.git
# python -m playwright install chromium
```
<details>
<summary>or via poetry</summary>
<code style="white-space:wrap;">
poetry add git+https://github.com/ffreemt/get-pwbrowser-sync.git &&
python -m playwright install chromium
</code></details>

## Usage

```python
from get_pwbrowser_sync import get_pwbrowser_sync

browser = get_pwbrowser_sync()
page = browser.new_page()
page.goto("http://www.baidu.com")
print(page.title())
# '百度一下，你就知道'
```

## Use of `.env` and `os.environ`
The browser can be run in a headful manner (to actually see what's going on):
```
from get_pwbrowser_sync import get_pwbrowser_sync
browser = get_pwbrowser_sync(headless=False)

```

Some related parameters `HEADFUL`, `DEBUG` and `PROXY` can be set in shell environ or in .env with prefix `PWBROWSER_`.

e.g., `set PWBROWSER_HEADFUL=1` in Windows or `export PWBROWSER_HEADFUL=1` in Linux and freinds)

or in `.env`
```bash
# .env
PWBROWSER_HEADFUL=1
```

For more details have a look at the source code.