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
    'version': '0.1.1',
    'description': 'Reverse engineering helpers',
    'long_description': 're-helpers\n==========\n\nInternally used helpers for reverse engineering. So far, only `re_binmerge` is included.\n',
    'author': 'Thomas Luzat',
    'author_email': 'thomas@luzat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luzat/re-helpers',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
