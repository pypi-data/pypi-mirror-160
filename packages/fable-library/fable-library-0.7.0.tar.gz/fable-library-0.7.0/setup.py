# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fable_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fable-library',
    'version': '0.7.0',
    'description': 'Fable library for Python',
    'long_description': '# Fable Library for Python\n\nThis module is used as the [Fable](https://fable.io/) library for\nPython.\n\nThe code should be type annotated using [type\nhints](https://docs.python.org/3/library/typing.html) and statically\ntype checked using\n[pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)\nat `strict` setting.\n\nThe code should be formatted using the\n[black](https://black.readthedocs.io) formatter with default settings.\n',
    'author': 'Dag Brattli',
    'author_email': 'dag@brattli.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fable.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
