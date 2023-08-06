# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['lager']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'lager',
    'version': '0.16.4',
    'description': 'EZ-PZ logging based on loguru',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n\n# Lager :beer:\n\n\n[![Wheel](https://img.shields.io/pypi/wheel/lager.svg)](https://img.shields.io/pypi/wheel/lager.svg)\n[![Version](https://img.shields.io/pypi/v/lager.svg)](https://img.shields.io/pypi/v/lager.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/lager.svg)](https://img.shields.io/pypi/pyversions/lager.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Install:** `pip install lager`\n\nLogging library based off of loguru (`pip install loguru`).\n\n**Why not just use loguru?**\n\n - Lager is a better pun\n - Lager is really a utility pack for loguru\n\nBTW: Loguru is an amazing lib. Check it out: https://github.com/Delgan/loguru\n\n## Usage:\n\n\n\n```python\nfrom lager import LOG, lager, LAGER, log, logger  # All the same object\nLOG.info(\'info\')\n```\n\n    2021-07-22 12:29:22.853 | INFO     | __main__:<module>:2 - info\n\n',
    'author': 'jesse rubin',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/lager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
