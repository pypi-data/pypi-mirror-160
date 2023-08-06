# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hash_chunker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hash-chunker',
    'version': '0.1.2',
    'description': 'Generator that yields hash chunks for distributed data processing.',
    'long_description': '# Hash Chunker\n\nGenerator that yields hash chunks for distributed data processing.\n\n### TLDR\n\n```\npip install hash-chunker\n```\n\n```\nfrom hash_chunker import HashChunker \n\nchunks = list(HashChunker().get_chunks(chunk_size=1, all_items_count=2))\n\nassert chunks == [("0000000000", "8000000000"), ("8000000000", "ffffffffff")]\n```\n \n### Description\n\nImagine a situation when you need to process huge amount data rows in parallel.\nEach data row has a hash field and the task is to use it for chunking.\n\nPossible reasons for using hash field and not int id field:\n- No auto increment id field.\n- Id field has many blank lines (1,2,3, 100500, 100501, 1000000).\n- Chunking by id will break data that must be in one chunk to different chunks\n(in user behavioral analytics id can be autoincrement for all users actions and\nuser_session hash is linked to concrete user, so if we chunk by id one user session may\nnot be in one chunk).\n',
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
