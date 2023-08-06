# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matriarch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'matriarch',
    'version': '0.0.1',
    'description': 'Matriarch',
    'long_description': '# Matriarch\n\nStay tuned!\n',
    'author': 'Quansight',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quansight',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
