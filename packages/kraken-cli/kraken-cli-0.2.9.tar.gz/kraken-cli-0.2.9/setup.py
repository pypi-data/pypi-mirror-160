# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cli', 'cli.buildenv', 'cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['kraken-core>=0.3.0,<0.4.0',
 'nr.python.environment>=0.1.2,<0.2.0',
 'packaging>=20.0',
 'setuptools>=33.0.0',
 'slap.core.cli>=0.3.1,<0.4.0',
 'termcolor>=1.1.0,<2.0.0',
 'types-termcolor>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['kraken = kraken.cli.__main__:_entrypoint']}

setup_kwargs = {
    'name': 'kraken-cli',
    'version': '0.2.9',
    'description': '',
    'long_description': '# kraken-cli\n\n[![Python application](https://github.com/kraken-build/kraken-cli/actions/workflows/python-package.yml/badge.svg)](https://github.com/kraken-build/kraken-cli/actions/workflows/python-package.yml)\n[![PyPI version](https://badge.fury.io/py/kraken-cli.svg)](https://badge.fury.io/py/kraken-cli)\n\nThe command-line interface to the Kraken CLI.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
