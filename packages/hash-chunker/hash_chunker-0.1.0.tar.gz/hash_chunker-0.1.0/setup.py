# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hash_chunker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hash-chunker',
    'version': '0.1.0',
    'description': 'Helper that generates hash chunks for distributed data processing.',
    'long_description': '# Hash Chunker\n',
    'author': 'Volodymyr Kochetkov',
    'author_email': 'whysages@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whysage/hash_chunker',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
