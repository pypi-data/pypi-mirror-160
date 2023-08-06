# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataclass_mapper']

package_data = \
{'': ['*']}

extras_require = \
{'pydantic': ['pydantic>=1.9.0,<2.0.0']}

setup_kwargs = {
    'name': 'dataclass-mapper',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Jakob Kogler',
    'author_email': 'jakob.kogler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
