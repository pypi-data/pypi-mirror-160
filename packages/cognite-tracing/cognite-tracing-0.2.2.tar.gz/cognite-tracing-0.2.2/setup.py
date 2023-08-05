# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.tracing']

package_data = \
{'': ['*']}

install_requires = \
['elastic-apm[opentracing]>=6.6.1,<7.0.0',
 'lightstep>=4.4.7,<5.0.0',
 'opentracing>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'cognite-tracing',
    'version': '0.2.2',
    'description': 'Library for tracing using Lightstep',
    'long_description': None,
    'author': 'Vegard Stikbakke',
    'author_email': 'vegard.stikbakke@gmail.com',
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
