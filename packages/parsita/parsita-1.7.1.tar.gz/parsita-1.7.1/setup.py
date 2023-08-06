# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['parsita']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parsita',
    'version': '1.7.1',
    'description': 'Parser combinator library for Python',
    'long_description': "# Parsita\n\n[![Build status][build-image]][build-link]\n[![Code coverage][coverage-image]][coverage-link]\n[![Latest PyPI version][pypi-image]][pypi-link]\n[![Supported Python versions][python-versions-image]][python-versions-link]\n\n> The executable grammar of parsers combinators made available in the executable pseudocode of Python.\n\nParsita is a parser combinator library written in Python. Parser combinators provide an easy way to define a grammar using code so that the grammar itself effectively parses the source. They are not the fastest at parsing, but they are the easiest to write.\n\nLike all good parser combinator libraries, Parsita abuses operators to provide a clean grammar-like syntax. The `__or__` method is defined so that `|` tests between two alternatives. The `__and__` method is defined so that `&` tests two parsers in sequence. Other operators are used as well.\n\nIn a technique that I think is new to Python, Parsita uses metaclass magic to allow for forward declarations of values. This is important for parser combinators because grammars are often recursive or mutually recursive, meaning that some components must be used in the definition of others before they themselves are defined.\n\nSee the [Documentation](https://parsita.drhagen.com) for the full user guide.\n\n## Installation\n\nThe recommended means of installation is with `pip` from PyPI.\n\n```shell\npip install parsita\n```\n\n## Hello world\n\nThe following is a very basic parser for extracting the name from a `Hello, {name}!` string.\n\n```python\nfrom parsita import *\n\nclass HelloWorldParsers(TextParsers, whitespace=r'[ ]*'):\n    hello_world = lit('Hello') >> ',' >> reg(r'[A-Z][a-z]*') << '!'\n\n# A successful parse produces the parsed value\nname = HelloWorldParsers.hello_world.parse('Hello, David!').or_die()\nassert name == 'David'\n\n# A parsing failure produces a useful error message\nname = HelloWorldParsers.hello_world.parse('Hello David!').or_die()\n# parsita.state.ParseError: Expected ',' but found 'David'\n# Line 1, character 7\n#\n# Hello David!\n#       ^\n```\n\n[build-image]: https://github.com/drhagen/parsita/workflows/python/badge.svg?branch=master&event=push\n[build-link]: https://github.com/drhagen/parsita/actions?query=branch%3Amaster+event%3Apush\n[coverage-image]: https://codecov.io/github/drhagen/parsita/coverage.svg?branch=master\n[coverage-link]: https://codecov.io/github/drhagen/parsita?branch=master\n[pypi-image]: https://img.shields.io/pypi/v/parsita.svg\n[pypi-link]: https://pypi.python.org/pypi/parsita\n[python-versions-image]: https://img.shields.io/pypi/pyversions/parsita.svg\n[python-versions-link]: https://pypi.python.org/pypi/parsita\n",
    'author': 'David Hagen',
    'author_email': 'david@drhagen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drhagen/parsita',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
