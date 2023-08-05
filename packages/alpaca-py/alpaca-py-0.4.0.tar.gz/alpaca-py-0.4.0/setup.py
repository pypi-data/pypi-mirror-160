# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpaca',
 'alpaca.broker',
 'alpaca.broker.models',
 'alpaca.common',
 'alpaca.data',
 'alpaca.data.historical',
 'alpaca.data.live',
 'alpaca.data.models',
 'alpaca.trading']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.3,<2.0.0',
 'pandas==1.3.5',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'websockets>=10.2,<11.0']

setup_kwargs = {
    'name': 'alpaca-py',
    'version': '0.4.0',
    'description': 'The Official Python SDK for Alpaca APIs',
    'long_description': "# Alpaca-py\n\n[![Downloads](https://pepy.tech/badge/alpaca-py/month)](https://pepy.tech/project/alpaca-py)\n[![Python Versions](https://img.shields.io/pypi/pyversions/alpaca-py.svg?logo=python&logoColor=white)](https://pypi.org/project/alpaca-py)\n[![GitHub](https://img.shields.io/github/license/alpacahq/alpaca-py?color=blue)](https://github.com/alpacahq/alpaca-py/blob/master/LICENSE.md)\n[![PyPI](https://img.shields.io/pypi/v/alpaca-py?color=blue)](https://pypi.org/project/alpaca-py/)\n### About\n\nAlpaca-py provides an interface for interacting with the various REST and WebSocket endpoints Alpaca offers.\nYou can access both historical and live market data for equities and cryptocurrencies via the Market Data API. \nYou can place trades for both crypto and equities through a uniform interface. Alpaca-py also offers the ability\nto manage your Broker API account by creating accounts, managing funds, and more. \n\nLearn more about the API products [Alpaca]((https://alpaca.markets/)) offers.\n\n**Note: AlpacaPy is in the very early stages of alpha development and is not production ready. Currently AlpacaPy\ninterfaces with only the Market Data API, however the other APIs are coming soon.**\n\n### Installation\n\nAlpaca-py is supported on Python 3.8+.  You can install Alpaca-py using pip.\n\nRun the following command in your terminal.\n\n```shell\n  pip install alpaca-py\n```\n\n\n### Dev setup\n\nThis project is managed via poetry so setup should be just running `poetry install`.\n\nThis repo is using [`pre-commit`](https://pre-commit.com/) to setup some checks to happen at commit time to keep the\nrepo clean. To set these up after you've run `poetry install` just run `poetry run pre-commit install` to have\npre-commit setup these hooks\n\n\n\n",
    'author': 'Rahul Chowdhury',
    'author_email': 'rahul.chowdhury@alpaca.markets',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alpacahq/alpaca-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
