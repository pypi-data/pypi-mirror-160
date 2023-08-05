# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atomkraft', 'atomkraft.chain', 'atomkraft.cli']

package_data = \
{'': ['*']}

install_requires = \
['bip-utils>=2.3.0,<3.0.0',
 'copier>=6.1.0,<7.0.0',
 'hdwallet>=2.1.1,<3.0.0',
 'jsonrpcclient>=4.0.2,<5.0.0',
 'modelator>=0.4.2,<0.5.0',
 'numpy>=1.22.4,<2.0.0',
 'pytest>=7.1.2,<8.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.6.1,<0.7.0',
 'websockets>=10.3,<11.0']

entry_points = \
{'console_scripts': ['atomkraft = atomkraft.cli:app'],
 'pytest11': ['atomkraft-chain = atomkraft.chain.pytest']}

setup_kwargs = {
    'name': 'atomkraft',
    'version': '0.0.1',
    'description': 'Testing for Cosmos Blockchains',
    'long_description': '# atomkraft\n\nTesting for Cosmos Blockchains\n\n### Using `pip` (inside a system or virtual env)\n\n```\npip install git+https://github.com/informalsystems/atomkraft@dev\natomkraft --help\n```\n\n### Using `poetry` (inside a project)\n\n```\npoetry add git+https://github.com/informalsystems/atomkraft#dev\npoerty run atomkraft\n```\n',
    'author': 'Andrey Kuprianov',
    'author_email': 'andrey@informal.systems',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/informalsystems/atomkraft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
