# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['re_helpers']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['re_binmerge = re_helpers.binmerge:main']}

setup_kwargs = {
    'name': 're-helpers',
    'version': '0.1.0',
    'description': 'Reverse engineering helpers',
    'long_description': '',
    'author': 'Thomas Luzat',
    'author_email': 'thomas@luzat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
