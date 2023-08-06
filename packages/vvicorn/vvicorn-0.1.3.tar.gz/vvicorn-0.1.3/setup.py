# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vvicorn']

package_data = \
{'': ['*']}

install_requires = \
['ulogcorn>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'vvicorn',
    'version': '0.1.3',
    'description': "Uvicorn's logging wrapped with ulogcorn",
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
