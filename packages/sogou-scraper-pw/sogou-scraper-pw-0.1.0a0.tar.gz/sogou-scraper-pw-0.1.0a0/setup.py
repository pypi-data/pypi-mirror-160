# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sogou_scraper_pw']

package_data = \
{'': ['*']}

install_requires = \
['about-time>=4.1.0,<5.0.0',
 'get-pwbrowser-sync>=0.1.0-alpha.3,<0.2.0',
 'logzero>=1.7.0,<2.0.0',
 'playwright[chromium]>=1.24.0,<2.0.0',
 'pyquery>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'sogou-scraper-pw',
    'version': '0.1.0a0',
    'description': '',
    'long_description': '# sogou-scraper-pw\n<!--- repo_name  sogou_scraper_pyppeteer  sogou_scraper_pp sogou_scraper_pp --->\n[![tests](https://github.com/ffreemt/sogou-scraper-playwright/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sogou_scraper_pw.svg)](https://badge.fury.io/py/sogou_scraper_pw)\n\nScrape sogou tr using playwright\n\n## Installation\n```bash\npip install -U sogou-scraper-pw\n```\n\n## Usage\n\n```python\nfrom pprint import pprint\nfrom sogou_scraper_pw import sogou_tr\n\nres = sogou_tr("test me\\n test him")\npprint(res)\n# \'考验我\\n测试他\'\n\nprint(sogou_tr("test me", to_lang="de"))\n# Mich auf die Probe stellen.\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/sogou-scraper-playwright',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
