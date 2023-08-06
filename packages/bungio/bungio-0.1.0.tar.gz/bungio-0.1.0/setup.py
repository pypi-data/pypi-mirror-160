# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bungio',
 'bungio.api',
 'bungio.api.bungie',
 'bungio.api.overwrites',
 'bungio.http',
 'bungio.http.routes',
 'bungio.models',
 'bungio.models.basic',
 'bungio.models.bungie',
 'bungio.models.bungie.common',
 'bungio.models.bungie.config',
 'bungio.models.bungie.content',
 'bungio.models.bungie.destiny',
 'bungio.models.bungie.destiny.components',
 'bungio.models.bungie.destiny.definitions',
 'bungio.models.bungie.destiny.entities',
 'bungio.models.bungie.destiny.historicalstats',
 'bungio.models.bungie.destiny.reporting',
 'bungio.models.bungie.destiny.requests',
 'bungio.models.bungie.social',
 'bungio.models.bungie.tags',
 'bungio.models.bungie.tags.models',
 'bungio.models.bungie.user',
 'bungio.models.mixins',
 'bungio.models.overwrites',
 'bungio.models.overwrites.destiny',
 'bungio.models.overwrites.destiny.historicalstats']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[aiosqlite]>=1.4.36,<2.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0']

extras_require = \
{'all': ['orjson>=3.6.8,<4.0.0',
         'aiodns>=3.0.0,<4.0.0',
         'cchardet>=2.1.7,<3.0.0',
         'Brotli>=1.0.9,<2.0.0',
         'aiohttp-client-cache>=0.7.0,<0.8.0',
         'mkdocstrings[python]>=0.18.1,<0.19.0',
         'mkdocs-material>=8.2.15,<9.0.0',
         'mkdocs-awesome-pages-plugin>=2.7.0,<3.0.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0',
         'pytest>=7.1.2,<8.0.0',
         'pytest-asyncio>=0.18.3,<0.19.0'],
 'cache': ['aiohttp-client-cache>=0.7.0,<0.8.0'],
 'docs': ['mkdocstrings[python]>=0.18.1,<0.19.0',
          'mkdocs-material>=8.2.15,<9.0.0',
          'mkdocs-awesome-pages-plugin>=2.7.0,<3.0.0',
          'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'speedups': ['orjson>=3.6.8,<4.0.0',
              'aiodns>=3.0.0,<4.0.0',
              'cchardet>=2.1.7,<3.0.0',
              'Brotli>=1.0.9,<2.0.0'],
 'test': ['pytest>=7.1.2,<8.0.0', 'pytest-asyncio>=0.18.3,<0.19.0']}

setup_kwargs = {
    'name': 'bungio',
    'version': '0.1.0',
    'description': 'A destiny 2 / bungie api wrapper',
    'long_description': '[![](https://img.shields.io/pypi/v/bungio?label=Version&logo=pypi)](https://pypi.org/project/bungio/)\n[![](https://img.shields.io/pypi/dm/bungio?label=Downloads&logo=pypi)](https://pypi.org/project/bungio/)\n[![](https://img.shields.io/readthedocs/bungio?label=Docs&logo=readthedocs)](https://bungio.readthedocs.io/en/latest/)\n![](https://img.shields.io/badge/Python-3.10+-1081c1?logo=python)\n[![](https://img.shields.io/github/workflow/status/Kigstn/BungIO/Black%20Formatting/master?label=Black%20Formatting&logo=github)](https://github.com/Kigstn/BungIO/actions/workflows/black.yml)\n[![](https://img.shields.io/github/workflow/status/Kigstn/BungIO/Flake8%20Styling/master?label=Flake%20Styling&logo=github)](https://github.com/Kigstn/BungIO/actions/workflows/flake.yml)\n\n\n<h1 align="center">\n    <p>\n        <img src="https://raw.githubusercontent.com/Kigstn/BungIO/master/docs/src/images/favicon.png" alt="BungIO Logo">\n    </p>\n    BungIO\n</h1>\n\n---\n\nBungIO is a modern and pythonic wrapper for Bungies Destiny 2 API.\n\n- [X] Python 3.10+\n- [X] Asynchronous\n- [X] 100% typed and raw api coverage\n- [X] Ratelimit compliant\n- [X] Manifest support\n- [X] OAuth2 support\n- [X] Easily used in combination with other libraries like FastApi\n\nClick [here](https://bungio.readthedocs.io/en/latest/installation) to get started or visit\nthe [guides](https://bungio.readthedocs.io/en/latest/Guides/basic)\nor [api reference](https://bungio.readthedocs.io/en/latest/API%20Reference/client/).\n\n\n## Basic Example\n\n```py\nimport asyncio\nimport os\n\nfrom bungio import Client\nfrom bungio.models import BungieMembershipType, DestinyActivityModeType, DestinyUser\n\n\n# create the client obj with our bungie authentication\nclient = Client(\n    bungie_client_id=os.getenv("bungie_client_id"),\n    bungie_client_secret=os.getenv("bungie_client_secret"),\n    bungie_token=os.getenv("bungie_token"),\n)\n\nasync def main():\n    # create a user obj using a known bungie id\n    user = DestinyUser(membership_id=4611686018467765462, membership_type=BungieMembershipType.TIGER_STEAM)\n\n    # iterate thought the raids that user has played\n    async for activity in user.yield_activity_history(mode=DestinyActivityModeType.RAID):\n\n        # print the date of the activity\n        print(activity.period)\n\n# bungio is by nature asynchronous, it can only be run in an asynchronous context\nasyncio.run(main())\n```\n',
    'author': 'Daniel J',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kigstn/BungIO',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
