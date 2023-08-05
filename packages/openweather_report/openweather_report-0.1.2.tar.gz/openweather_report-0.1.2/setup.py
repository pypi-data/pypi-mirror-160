# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openweather_report']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.3,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'openweather-report',
    'version': '0.1.2',
    'description': 'Get weather data using OpenWeather API and save data to a database.',
    'long_description': '# OpenWeather Report\n\nGet weather using OpenWeather API and save to a database.\n',
    'author': 'Christopher Tyler',
    'author_email': 'christophertyler@engineer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cetyler/openweather_report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
