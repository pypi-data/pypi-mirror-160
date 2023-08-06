# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextcord_ormar',
 'nextcord_ormar.nxalembic',
 'nextcord_ormar.nxalembic.template']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.8,<2.0', 'nextcord>=2.0,<3.0', 'ormar>=0.11,<0.12']

extras_require = \
{'docs': ['Sphinx>=5.1,<6.0',
          'releases>=1.6,<2.0',
          'sphinx-argparse>=0.3.1,<0.4.0',
          'six>=1.16.0,<2.0.0']}

entry_points = \
{'console_scripts': ['nxalembic = nextcord_ormar.nxalembic:main']}

setup_kwargs = {
    'name': 'nextcord-ormar',
    'version': '0.3.1',
    'description': 'Database integration for Nextcord with Tortoise-ORM',
    'long_description': None,
    'author': 'Peter DeVita',
    'author_email': 'mewtwo2643@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
