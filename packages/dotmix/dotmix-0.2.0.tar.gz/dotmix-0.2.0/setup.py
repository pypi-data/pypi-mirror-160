# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotmix', 'dotmix.cli', 'dotmix.vendor']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0',
 'click>=8.0.1,<9.0.0',
 'colp>=0.0.2,<0.0.3',
 'pydantic>=1.8.2,<2.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=4.4.0,<5.0.0',
                      'sphinx-autoapi>=1.8.4,<2.0.0',
                      'sphinx-rtd-theme>=1.0.0,<2.0.0']}

entry_points = \
{'console_scripts': ['dotmix = dotmix.cli:cli']}

setup_kwargs = {
    'name': 'dotmix',
    'version': '0.2.0',
    'description': 'dotmix is a library and a cli that offers a template based solution to managing your dotfiles',
    'long_description': None,
    'author': 'Ian Mancini',
    'author_email': 'ianmethyst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
