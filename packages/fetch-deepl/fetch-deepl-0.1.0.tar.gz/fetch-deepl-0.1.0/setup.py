# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetch_deepl']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'logzero>=1.7.0,<2.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['fetch-deepl = fetch_deepl.__main__:app']}

setup_kwargs = {
    'name': 'fetch-deepl',
    'version': '0.1.0',
    'description': 'Fetch result from a deepl-fastapi API.',
    'long_description': '# fetch-deepl\n[![pytest](https://github.com/ffreemt/fetch-deepl/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/fetch-deepl/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fetch_deepl.svg)](https://badge.fury.io/py/fetch_deepl)\n\nfetch-deepl descr\n\n## Install it\n\n```shell\npip install fetch_deepl\n# pip install git+https://github.com/ffreemt/fetch-deepl\n# poetry add git+https://github.com/ffreemt/fetch-deepl\n# git clone https://github.com/ffreemt/fetch-deepl && cd fetch-deepl\n```\n\n## Use it\n```python\nfrom fetch_deepl import fetch_deepl\n\nprint(fetch_deepl("Tell me and I forget. Teach me and I remember. Involve me and I learn."))\n# 告诉我，我就忘了。教导我，我就记住。让我参与，我就学\n\nprint(fetch_deepl("书山有路勤为径"))\n# There is a path to the mountain of books and diligence is the path\n\nprint(fetch_deepl("There is a path to the mountain of books and diligence is the path", from_lang="en", to_lang="de"))\n# Es gibt einen Weg zum Berg der Bücher und Fleiß ist der Weg\n\nprint(fetch_deepl("书山有路勤为径", from_lang="zh", to_lang="de"))\n# Es gibt einen Weg durch die Berge des Lernens und des Fleißes\n```\nN.B. If you switch to a new pair of languages, the first translation may not be correct. This has to do with how `deepl-fastapi` (which this whole things is based on) functions.',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/fetch-deepl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
