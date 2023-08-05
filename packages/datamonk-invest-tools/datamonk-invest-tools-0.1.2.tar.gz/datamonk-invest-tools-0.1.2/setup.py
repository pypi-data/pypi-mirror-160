# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invest_tools']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.10,<2.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'datamonk-invest-tools',
    'version': '0.1.2',
    'description': 'package for my personal investment activities',
    'long_description': None,
    'author': 'Vit Mrnavek',
    'author_email': 'vit.mrnavek@datamonk.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
