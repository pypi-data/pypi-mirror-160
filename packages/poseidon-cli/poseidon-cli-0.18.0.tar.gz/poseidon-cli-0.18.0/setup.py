# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poseidon_cli']

package_data = \
{'': ['*']}

install_requires = \
['cmd2==2.4.2', 'natural==0.2.0', 'poseidon-core==0.17.21', 'texttable==1.6.4']

entry_points = \
{'console_scripts': ['poseidon-cli = poseidon_cli.__main__:main']}

setup_kwargs = {
    'name': 'poseidon-cli',
    'version': '0.18.0',
    'description': 'Commandline tool for querying Poseidon via Prometheus',
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
