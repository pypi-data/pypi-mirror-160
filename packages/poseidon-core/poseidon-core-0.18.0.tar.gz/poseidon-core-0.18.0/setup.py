# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poseidon_core',
 'poseidon_core.controllers',
 'poseidon_core.controllers.faucet',
 'poseidon_core.helpers',
 'poseidon_core.operations',
 'poseidon_core.operations.primitives',
 'poseidon_core.operations.volos']

package_data = \
{'': ['*'], 'poseidon_core': ['metadata/*']}

install_requires = \
['faucetconfrpc==0.22.38',
 'httpx==0.23.0',
 'netaddr==0.8.0',
 'pika==1.3.0',
 'prometheus_client==0.14.1',
 'pyyaml==6.0',
 'schedule==1.1.0',
 'transitions==0.8.11']

entry_points = \
{'console_scripts': ['poseidon-core = poseidon_core.__main__:main']}

setup_kwargs = {
    'name': 'poseidon-core',
    'version': '0.18.0',
    'description': 'Poseidon core package, an application that leverages software defined networks (SDN) to acquire and then feed network traffic to a number of analytic tools.',
    'long_description': None,
    'author': 'cglewis',
    'author_email': 'clewis@iqt.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
