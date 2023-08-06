# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exencolorlogs']

package_data = \
{'': ['*']}

install_requires = \
['exencolor>=1.0']

setup_kwargs = {
    'name': 'exencolorlogs',
    'version': '1.0.2',
    'description': 'A module for nice looking colored logs.',
    'long_description': '# ExenColorLogs\n\nA module for nice looking colored logs. Does not have much customization, just a Logger class with special formatting.\n\n## Installation\n\nThe module is available for installation from PyPI via pip.\n```shell\n$ pip install exencolorlogs\n```\n\n## Basic Usage\n\n```python\nfrom exencolorlogs import Logger\n\nlog = Logger()\nlog.info("Greeting...")\nlog.ok("Hello!")\n```\n',
    'author': 'Exenifix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Exenifix/exencolorlogs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
