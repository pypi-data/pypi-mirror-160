# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaurorax',
 'pyaurorax._internal',
 'pyaurorax.api',
 'pyaurorax.api.classes',
 'pyaurorax.availability',
 'pyaurorax.availability.classes',
 'pyaurorax.cli',
 'pyaurorax.cli.availability',
 'pyaurorax.cli.conjunctions',
 'pyaurorax.cli.data_products',
 'pyaurorax.cli.ephemeris',
 'pyaurorax.cli.sources',
 'pyaurorax.cli.util',
 'pyaurorax.conjunctions',
 'pyaurorax.conjunctions.classes',
 'pyaurorax.conjunctions.swarmaurora',
 'pyaurorax.data_products',
 'pyaurorax.data_products.classes',
 'pyaurorax.ephemeris',
 'pyaurorax.ephemeris.classes',
 'pyaurorax.metadata',
 'pyaurorax.requests',
 'pyaurorax.sources',
 'pyaurorax.sources.classes',
 'pyaurorax.util']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'humanize>=3.2.0,<4.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'texttable>=1.6.4,<2.0.0']

extras_require = \
{'aacgmv2': ['aacgmv2>=2.6.2,<3.0.0']}

entry_points = \
{'console_scripts': ['aurorax-cli = pyaurorax.cli.cli:cli']}

setup_kwargs = {
    'name': 'pyaurorax',
    'version': '0.10.0',
    'description': 'Python library for interacting with the AuroraX API',
    'long_description': '<a href="https://aurorax.space/"><img alt="AuroraX" src="logo.svg" height="60"></a>\n\n[![GitHub tests](https://github.com/aurorax-space/pyaurorax/actions/workflows/test_standard.yml/badge.svg)](https://github.com/aurorax-space/pyaurorax/actions/workflows/test_standard.yml)\n[![PyPI version](https://img.shields.io/pypi/v/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/aurorax-space/pyaurorax/blob/main/LICENSE)\n[![PyPI Python versions](https://img.shields.io/pypi/pyversions/pyaurorax.svg)](https://pypi.python.org/pypi/pyaurorax/)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6098075.svg)](https://doi.org/10.5281/zenodo.6098075)\n\nPyAuroraX is a Python library for interacting with [AuroraX](https://aurorax.space), a project working to be the world\'s first and foremost data platform for auroral science. The primary objective of AuroraX is to enable mining and exploration of existing and future auroral data, enabling key science and enhancing the benefits of the world\'s investment in auroral instrumentation. This will be accomplished with the development of key systems/standards for uniform metadata generation and search, image content analysis, interfaces to leading international tools, and a community involvement that includes more than 80% of the world\'s data providers.\n\nPyAuroraX officially supports Python 3.6, 3.7, 3.8, and 3.9 (Python 3.10 not currently supported).\n\nSome links to help:\n- [AuroraX main website](https://aurorax.space)\n- [PyAuroraX documentation](https://docs.aurorax.space/code/overview)\n- [PyAuroraX API Reference](https://docs.aurorax.space/code/pyaurorax_api_reference/pyaurorax)\n\n## Installation\n\nPyAuroraX is available on PyPI so pip can be used to install it:\n\n```console\n$ pip install pyaurorax\n```\n\nTo get full functionality, you can install PyAuroraX with the aacgmv2 dependency. Note that without this, the calculate_btrace methods in the util module will show warning messages. All other functionality will work without this dependency.\n\n```console\n$ pip install pyaurorax[aacgmv2]\n```\n\nFuthermore, if you want the most bleeding edge version of PyAuroraX, you can install it directly from the Github repository:\n\n```console\n$ git clone https://github.com/aurorax-space/pyaurorax.git\n$ cd pyaurorax\n$ pip install .\n[ or with the aacgmv2 extra ]\n$ pip install .[aacgmv2]\n```\n\n## Usage\n\nThere are two things you can use as part of the PyAuroraX library: the main library, and the command line tool.\n\n### Library import\n\nYou can import the library using the following statement:\n\n```python\n>>> import pyaurorax\n```\n\n### CLI program\n\nThe program `aurorax-cli` is included in the PyAuroraX package as a command line tool. Try it out using:\n\n```\n$ aurorax-cli --help\n```\n\n## Development\n\nSome common things you can do:\n- `make update` Update the Python dependency libraries\n- `tools/bump_version.py` Bump the version number\n- `make test-pytest-unauthorized-access` Only run the authorization tests\n- `make test-pytest-read` Only run the read-based tests\n- `make test-pytest-create-update-delete` Only run the write-based tests\n- `make docs` Generate pdoc documentation\n\n### Setup\n\nClone the repository and install primary and development dependencies using Poetry.\n\n```console\n$ git clone git@github.com:aurorax-space/pyaurorax.git\n$ cd pyaurorax\n$ make install\n```\n\n### Documentation\n\nDocumentation for the PyAuroraX project is managed by a separate repository [here](https://github.com/aurorax-space/docs). However, you are still able to generate the documentation for this repo for testing/development purposes. To generate the docs, run the following:\n\n```console\n$ make docs\n```\n\n### Testing\n\nPyAuroraX includes several test evaluations bundled into two groups: linting and functionality tests. The linting includes looking through the codebase using tools such as Flake8, PyLint, Pycodestyle, Bandit, and MyPy. The functionality tests use PyTest to test modules in the library.\n\nWhen running the functionality tests using PyTest, you must have the environment variable `AURORAX_APIKEY_STAGING` set to your API key on the staging API system. Alternatively, you can specifiy your API key using the command line (see example at the bottom of this section).\n\nThere exist several makefile targets to help run these tests quicker/easier. Below are the available commands:\n\n- `make test-linting` Run all linting tests\n- `make test-pytest` Run all automated functional tests\n- `make test-flake8` Run Flake8 styling tests\n- `make test-pylint` Run PyLint styling tests\n- `make test-pycodestyle` Run pycodestyle styling tests\n- `make test-bandit` Run Bandit security test\n- `make test-mypy` Run mypy type checking test\n- `make test-coverage` View test coverage report (must be done after `make test-pytest` or other coverage command)\n\nThe PyTest functionality tests include several categories of tests. You can run each category separately if you want using the "markers" feature of PyTest. All markers are found in the pytest.ini file at the root of the repository.\n\n- `poetry run pytest --markers` List all markers\n- `poetry run pytest -v -m accounts` Perform only the tests for the "accounts" marker\n- `poetry run pytest -v -m availability` Perform only the tests for the "availability" marker\n- `poetry run pytest -v -m conjunctions` Perform only the tests for the "conjunctions" marker\n- `poetry run pytest -v -m ephemeris` Perform only the tests for the "ephemeris" marker\n- `poetry run pytest -v -m exceptions` Perform only the tests for the "exceptions" marker\n- `poetry run pytest -v -m location` Perform only the tests for the "location" marker\n- `poetry run pytest -v -m metadata` Perform only the tests for the "metadata" marker\n- `poetry run pytest -v -m requests` Perform only the tests for the "request" marker\n- `poetry run pytest -v -m sources` Perform only the tests for the "sources" marker\n- `poetry run pytest -v -m util` Perform only the tests for the "util" marker\n\nBelow are some more commands for advanced usages of PyTest.\n\n- `poetry run pytest -v` Run all tests in verbose mode\n- `poetry run pytest --collect-only` List all available tests\n- `poetry run pytest --markers` List all markers (includes builtin, plugin and per-project ones)\n- `cat pytest.ini` List custom markers\n- `poetry run pytest tests/test_suite/ephemeris/test_ephemeris.py::test_get_request_url -v` Run a single specific test\n\nYou can also run Pytest against a different API. By default, it runs agains the staging API, but you can alternatively tell it to run against the production API, or a local instance.\n\n- `poetry run pytest -v --env=production` Run all tests against production API, using the AURORAX_APIKEY_PRODUCTION environment variable\n- `poetry run pytest --env=local --host=http://localhost:3000` Run all tests against a local instance of the API, using the AURORAX_APIKEY_LOCAL environment variable\n- `poetry run pytest -v --api-key=SOME_API_KEY` Run all tests with the specified API key (will run against the staging API since that\'s the default)\n- `poetry run pytest --help` View usage for pytest, including the usage for custom options (see the \'custom options\' section of the output)\n\nBelow are some more commands for evaluating the PyTest coverage.\n\n- `poetry run coverage report` View test coverage report\n- `poetry run coverage html` Generate an HTML page of the coverage report\n- `poetry run coverage report --show-missing` View the test coverage report and include the lines deemed to be not covered by tests\n\nNote that the coverage report only gets updated when using the Makefile pytest targets, or when running coverage manually like `coverage run -m pytest -v`. More information about usage of the `coverage` command can be found [here](https://coverage.readthedocs.io).\n',
    'author': 'Maryam Sohrabi',
    'author_email': 'sohrabm@ucalgary.ca',
    'maintainer': 'Maryam Sohrabi',
    'maintainer_email': 'sohrabm@ucalgary.ca',
    'url': 'https://github.com/aurorax-space/pyaurorax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
