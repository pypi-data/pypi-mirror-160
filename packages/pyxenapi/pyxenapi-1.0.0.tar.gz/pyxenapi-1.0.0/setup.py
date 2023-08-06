# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxenapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyxenapi',
    'version': '1.0.0',
    'description': 'Python API Wrapper for XenForo Restful API',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
