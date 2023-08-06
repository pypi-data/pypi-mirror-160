# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['async_pixiv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-pixiv',
    'version': '0.0.1',
    'description': 'Async Pixiv API',
    'long_description': '# async-pixiv\nAsync Pixiv API\n',
    'author': 'Arko',
    'author_email': 'arko.space.cc@gmail.com',
    'maintainer': 'Karako',
    'maintainer_email': 'karakohear@gmail.com',
    'url': 'https://github.com/ArkoClub/async-pixiv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
