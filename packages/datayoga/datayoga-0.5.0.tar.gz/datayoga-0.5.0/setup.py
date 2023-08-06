# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datayoga',
 'datayoga.blocks',
 'datayoga.blocks.add_field',
 'datayoga.blocks.map',
 'datayoga.blocks.remove_field',
 'datayoga.blocks.rename_field']

package_data = \
{'': ['*'], 'datayoga': ['schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'jmespath>=1.0.0,<2.0.0', 'jsonschema>=4.4.0,<5.0.0']

extras_require = \
{'test': ['mock>=4.0.3,<5.0.0',
          'pytest>=7.1.2,<8.0.0',
          'pytest-describe>=2.0.1,<3.0.0',
          'pytest-mock>=3.7.0,<4.0.0',
          'pytest-timeout>=2.1.0,<3.0.0',
          'requests-mock>=1.9.3,<2.0.0']}

setup_kwargs = {
    'name': 'datayoga',
    'version': '0.5.0',
    'description': 'DataYoga for Python',
    'long_description': '# TBD\n',
    'author': 'DataYoga',
    'author_email': 'admin@datayoga.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
