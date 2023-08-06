# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dochooks',
 'dochooks.api_doc_checker',
 'dochooks.api_doc_checker.checkers',
 'dochooks.api_doc_checker.core',
 'dochooks.insert_whitespace_between_cn_and_en_char',
 'dochooks.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

extras_require = \
{':python_version < "3.11"': ['typing-extensions>=4.3.0,<5.0.0'],
 'rst-parser': ['docutils>=0.19,<0.20']}

entry_points = \
{'console_scripts': ['api-doc-checker = dochooks.api_doc_checker.check:main',
                     'check-whitespace-between-cn-and-en-char = '
                     'dochooks.insert_whitespace_between_cn_and_en_char.check:main',
                     'insert-whitespace-between-cn-and-en-char = '
                     'dochooks.insert_whitespace_between_cn_and_en_char.format:main']}

setup_kwargs = {
    'name': 'dochooks',
    'version': '0.3.0',
    'description': '',
    'long_description': 'None',
    'author': 'Nyakku Shigure',
    'author_email': 'sigure.qaq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
