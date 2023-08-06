# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyob',
 'pyob.exceptions',
 'pyob.main',
 'pyob.main.tools',
 'pyob.meta',
 'pyob.meta.classes',
 'pyob.set',
 'pyob.store',
 'pyob.tools',
 'pyob.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyob',
    'version': '1.0.2',
    'description': 'A high-level runtime object manager for Python 3 and above.',
    'long_description': None,
    'author': 'khunspoonzi',
    'author_email': 'khunspoonzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
