# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hatter']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=8.0.3,<9.0.0',
 'clearcut>=0.2.2.post0,<0.3.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'hatter',
    'version': '0.6.0b3',
    'description': 'Framework to easily create microservices backed by a RabbitMQ broker',
    'long_description': '# Hatter: Decorator-based framework for AMQP clients\n\n[![Build Status](https://cloud.drone.io/api/badges/tangibleintelligence/hatter/status.svg)](https://cloud.drone.io/tangibleintelligence/hatter)\n[![PyPI version](https://badge.fury.io/py/hatter.svg)](https://badge.fury.io/py/hatter)\n\n`hatter` is a framework to easily create microservices backed by a RabbitMQ broker.\n\nWhile functional, this is still in alpha phase. Documentation, tests, and some additional functionality is still to come.',
    'author': 'Austin Howard',
    'author_email': 'austin@tangibleintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tangibleintelligence/hatter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
