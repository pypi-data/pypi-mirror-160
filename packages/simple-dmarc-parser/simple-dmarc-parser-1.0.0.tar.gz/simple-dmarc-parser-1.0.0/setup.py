# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_dmarc_parser']

package_data = \
{'': ['*']}

install_requires = \
['imap-tools>=0.56.0,<0.57.0', 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['simple-dmarc-parser = '
                     'simple_dmarc_parser.dmarc_parser:main']}

setup_kwargs = {
    'name': 'simple-dmarc-parser',
    'version': '1.0.0',
    'description': 'A Python script that processes DMARC reports from a mailbox and gives a basic summary.',
    'long_description': None,
    'author': 'FrostTheFox',
    'author_email': 'python@frostthefox.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
