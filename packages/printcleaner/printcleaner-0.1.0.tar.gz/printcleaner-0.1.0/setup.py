# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printcleaner']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.4.7,<0.5.0', 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'printcleaner',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lars Von Schaff',
    'author_email': 'larsvonschaff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
