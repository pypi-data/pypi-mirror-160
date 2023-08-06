# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interactive_system_magic']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.4.0,<9.0.0']

setup_kwargs = {
    'name': 'interactive-system-magic',
    'version': '0.1.0',
    'description': 'An IPython magic to run system commands interactively',
    'long_description': None,
    'author': 'Matt Williams',
    'author_email': 'matt@milliams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
