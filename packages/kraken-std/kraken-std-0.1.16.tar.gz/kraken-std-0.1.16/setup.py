# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['std',
 'std.cargo',
 'std.docker',
 'std.generic',
 'std.helm',
 'std.python',
 'std.python.buildsystem',
 'std.python.tasks']

package_data = \
{'': ['*'], 'std.cargo': ['data/certs/*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'kraken-core>=0.3.6,<0.4.0',
 'proxy.py>=2.4.3,<3.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'twine>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'kraken-std',
    'version': '0.1.16',
    'description': 'The Kraken standard library.',
    'long_description': '# kraken-std\n\n[![Python application](https://github.com/kraken-build/kraken-std/actions/workflows/python-package.yml/badge.svg)](https://github.com/kraken-build/kraken-std/actions/workflows/python-package.yml)\n[![PyPI version](https://badge.fury.io/py/kraken-std.svg)](https://badge.fury.io/py/kraken-std)\n\nThe Kraken standard library.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
