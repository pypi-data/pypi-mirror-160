# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_http_sd']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.3,<3.0.0',
 'prometheus-client>=0.14.1,<0.15.0',
 'waitress>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['prometheus-http-sd = prometheus_http_sd.app:main']}

setup_kwargs = {
    'name': 'prometheus-http-sd',
    'version': '0.2.1',
    'description': 'Prometheus HTTP SD framework.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
