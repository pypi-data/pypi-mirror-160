# sogou-scraper-pw
<!--- repo_name  sogou_scraper_pyppeteer  sogou_scraper_pp sogou_scraper_pp --->
[![tests](https://github.com/ffreemt/sogou-scraper-playwright/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sogou_scraper_pw.svg)](https://badge.fury.io/py/sogou_scraper_pw)

Scrape sogou tr using playwright

## Installation
```bash
pip install -U sogou-scraper-pw
```

## Usage

```python
from pprint import pprint
from sogou_scraper_pw import sogou_tr

res = sogou_tr("test me\n test him")
pprint(res)
# '考验我\n测试他'

print(sogou_tr("test me", to_lang="de"))
# Mich auf die Probe stellen.
