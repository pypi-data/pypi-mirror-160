# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siili']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.34,<2.0.0',
 'colorlog>=6.6.0,<7.0.0',
 'environs>=9.5.0,<10.0.0',
 'mypy>=0.971,<0.972',
 'yaspin>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['siili = siili.cli:cli']}

setup_kwargs = {
    'name': 'siili',
    'version': '0.1.0',
    'description': 'Amazon S3 uploading for mortals',
    'long_description': None,
    'author': 'hiAndrewQuinn',
    'author_email': '53230903+hiAndrewQuinn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
