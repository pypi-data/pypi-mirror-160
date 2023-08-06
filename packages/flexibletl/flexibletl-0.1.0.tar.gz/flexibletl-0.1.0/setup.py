# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flexibletl']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.6,<5.0.0',
 'kedro>=0.18.2,<0.19.0',
 'psycopg2-binary>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'flexibletl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'John Doe',
    'author_email': 'john@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
