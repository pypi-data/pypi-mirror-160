# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefect_tasks']

package_data = \
{'': ['*']}

install_requires = \
['datamonk-invest-tools>=0.1.1,<0.2.0',
 'datamonk-scriptorium>=0.5.0,<0.6.0',
 'datamonk-utils>=0.1.0,<0.2.0',
 'prefect>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'datamonk-prefect-tasks',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Vit Mrnavek',
    'author_email': 'vit.mrnavek@datamonk.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.10.0',
}


setup(**setup_kwargs)
