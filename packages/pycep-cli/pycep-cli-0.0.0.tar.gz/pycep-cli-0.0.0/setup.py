# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'pycep'}

packages = \
['pycep']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['rich>=12.5.1,<13.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pycep = pycep-cli:cli']}

setup_kwargs = {
    'name': 'pycep-cli',
    'version': '0.0.0',
    'description': 'Deploy Azure Resources with Python + Bicep',
    'long_description': '# pycep-cli\n\nThis will be a python cli tool to deploy azure resources based on bicep files.\n',
    'author': 'mfeyx',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
