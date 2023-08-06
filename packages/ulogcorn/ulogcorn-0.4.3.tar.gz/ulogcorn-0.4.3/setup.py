# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ulogcorn']

package_data = \
{'': ['*']}

install_requires = \
['gunicorn>=20.1.0,<21.0.0',
 'loguru>=0.6.0,<0.7.0',
 'uvicorn[standard]>=0.18.1,<0.19.0']

setup_kwargs = {
    'name': 'ulogcorn',
    'version': '0.4.3',
    'description': 'Unify logging for a gunicorn and uvicorn application with loguru',
    'long_description': None,
    'author': 'Joy',
    'author_email': 'icocoabeans@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
