# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_pydantic', 'markdown_pydantic.models', 'markdown_pydantic.types']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.7,<4.0.0', 'PyYAML>=6.0,<7.0', 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['markdown-pydantic = markdown_pydantic.app:run']}

setup_kwargs = {
    'name': 'markdown-pydantic',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Piotr Katolik',
    'author_email': 'katolus@ventress.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
