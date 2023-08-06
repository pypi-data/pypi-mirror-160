# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valio',
 'valio.descriptor',
 'valio.error',
 'valio.field',
 'valio.logger',
 'valio.regexer',
 'valio.regexer.relib',
 'valio.regexer.tests',
 'valio.schema',
 'valio.tests',
 'valio.tests.descriptor',
 'valio.tests.validator',
 'valio.validator']

package_data = \
{'': ['*']}

install_requires = \
['phonenumbers>=8.12.50,<9.0.0', 'typingx>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'valio',
    'version': '0.1.0b5',
    'description': 'Pluggable validation library that supports dataclasses, async validation, async tasks, validation extension, regex validation, dynamic documentation and much more. ',
    'long_description': None,
    'author': 'bitplorer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
