# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simyan', 'simyan.schemas']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'ratelimit>=2.2.1,<3.0.0', 'requests>=2.28.1,<3.0.0']

extras_require = \
{'docs': ['mkdocs>=1.3.1,<2.0.0',
          'mkdocstrings[python]>=0.19.0,<0.20.0',
          'mkdocs-include-markdown-plugin>=3.6.0,<4.0.0']}

setup_kwargs = {
    'name': 'simyan',
    'version': '0.10.0',
    'description': 'A Python wrapper for the Comicvine API.',
    'long_description': '# Simyan\n\n[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)\n\n[![Black](https://img.shields.io/badge/Black-Enabled-000000?style=flat-square)](https://github.com/psf/black)\n[![Flake8](https://img.shields.io/badge/Flake8-Enabled-informational?style=flat-square)](https://github.com/PyCQA/flake8)\n[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)\n\n[![Github - Contributors](https://img.shields.io/github/contributors/Metron-Project/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Metron-Project/Simyan/graphs/contributors)\n\n[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)\n[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Metron-Project/Simyan/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/code-analysis.yaml)\n[![Github Action - Testing](https://img.shields.io/github/workflow/status/Metron-Project/Simyan/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Metron-Project/Simyan/actions/workflows/testing.yaml)\n\nA [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.\n\n## Installation\n\n**Simyan** requires >= 3.7.\n\n### Installing/Upgrading from PyPI\n\nTo install the latest version from PyPI:\n\n```shell\n$ pip3 install -U --user simyan\n```\n\nor via poetry:\n\n```shell\n$ poetry install simyan\n```\n\n## Example Usage\n\n```python\nfrom simyan.comicvine import Comicvine\nfrom simyan.sqlite_cache import SQLiteCache\n\nsession = Comicvine(api_key="ComicVine API Key", cache=SQLiteCache())\n\n# Search for Publisher\nresults = session.publisher_list(params={"filter": "name:DC Comics"})\nfor publisher in results:\n    print(f"{publisher.publisher_id} | {publisher.name} - {publisher.site_url}")\n\n# Get details for a Volume\nresult = session.volume(volume_id=26266)\nprint(result.summary)\n```\n\n## Notes\n\nBig thanks to [Mokkari](https://github.com/Metron-Project/mokkari) for the inspiration and template for this project.\n\nWho or what is Simyan?\n\n> Simyan along with his partner Mokkari, are the diminutive proprietors of the Evil Factory, an evil version of Project Cadmus created by Darkseid and his elite.\n>\n> More details at [Simyan (New Earth)](<https://dc.fandom.com/wiki/Simyan_(New_Earth)>)\n',
    'author': 'Buried-In-Code',
    'author_email': 'BuriedInCode@tuta.io',
    'maintainer': 'Buried-In-Code',
    'maintainer_email': 'BuriedInCode@tuta.io',
    'url': 'https://github.com/Metron-Project/Simyan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
