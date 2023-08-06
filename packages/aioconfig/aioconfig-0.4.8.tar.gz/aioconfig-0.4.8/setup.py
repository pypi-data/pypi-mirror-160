# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioconfig']

package_data = \
{'': ['*']}

install_requires = \
['dataset>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'aioconfig',
    'version': '0.4.8',
    'description': '',
    'long_description': "# aioconfig\n\n`aioconfig` **efficiently** and **thread-safely** stores configurations in the\nbackground (**asynchronously**).\n\n## Installation\n\n```sh\npip install aioconfig\n```\n\n## Usage\n\nThe interface of `aioconfig` is dramatically easy to use.\nFor example, both `set(key, value)` and `await set(key, value)` store a pair of\nkey/value, which the former one is a fire-and-forget asynchronous function call\nwhile the latter one blocks until the data written onto the disk.\n\n### Init\n\n```py\nimport aioconfig\nstorage = aioconfig.get_storage(await aioconfig.attach('example.db'))\nsection = await aioconfig.get('default')\n```\n\n### Delete\n\n```py\nsection.delete(key='foo')\n```\n\n#### Blocking delete (wait until it's done)\n\n```py\nawait section.delete(key='foo')\n```\n\n### Get\n\n```py\nvalue1 = await section.get(key='foo', default='bar')\nvalue2 = await section.get(key='baz', default=12.3)\n```\n\n### Get all\n\n```py\nvalue = await section.get_all()\n```\n\n### Set (fire-and-forget)\n\n```py\nsection.set(key='foo', value='bar')\nsection.set(key='baz', value=12.3)\n```\n\n#### Blocking set (wait until it's done)\n\n```py\nawait section.set(key='foo', value='bar')\nawait section.set(key='baz', value=12.3)\n```\n\n### Batch set (fire-and-forget) (TBD)\n\n```py\nwith storage.transation():\n    storage.set(\n        key='foo', value='bar',\n        section='default_section')\n    storage.set(\n        key='baz', value=12.3,\n        section='default_section')\n```\n\n#### Blocking batch set (wait until it's done) (TBD)\n\n```py\nasync with storage.transation():\n    storage.set(\n        key='foo', value='bar',\n        section='default_section')\n    storage.set(\n        key='baz', value=12.3,\n        section='default_section')\n```\n",
    'author': 'Johann Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/changyuheng/aioconfig.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
