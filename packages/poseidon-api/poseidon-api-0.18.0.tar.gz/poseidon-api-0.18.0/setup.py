# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poseidon_api']

package_data = \
{'': ['*']}

install_requires = \
['bjoern==3.2.1',
 'falcon-cors==1.1.7',
 'falcon==3.1.0',
 'httpx==0.23.0',
 'natural==0.2.0',
 'poseidon-core==0.17.21']

entry_points = \
{'console_scripts': ['poseidon-api = poseidon_api.api:main']}

setup_kwargs = {
    'name': 'poseidon-api',
    'version': '0.18.0',
    'description': 'RESTful API for querying Poseidon',
    'long_description': None,
    'author': 'cglewis',
    'author_email': 'clewis@iqt.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
