# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['firebirdsql_run']

package_data = \
{'': ['*']}

install_requires = \
['firebirdsql>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'firebirdsql-run',
    'version': '0.0.1a3',
    'description': 'Firebirdsql wrapper inspired by subprocess.run',
    'long_description': '# firebirdsql-run\n\n> [Firebirdsql](https://github.com/nakagami/pyfirebirdsql/) wrapper inspired by [subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run).\n\n[![PyPI version](https://img.shields.io/pypi/v/firebirdsql-run)](https://pypi.org/project/firebirdsql-run)\n[![CI/CD](https://github.com/DeadNews/firebirdsql-run/actions/workflows/python-app.yml/badge.svg)](https://github.com/DeadNews/firebirdsql-run/actions/workflows/python-app.yml)\n[![CodeQL](https://github.com/DeadNews/firebirdsql-run/actions/workflows/python-codeql.yml/badge.svg)](https://github.com/DeadNews/firebirdsql-run/actions/workflows/python-codeql.yml)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeadNews/firebirdsql-run/main.svg)](https://results.pre-commit.ci/latest/github/DeadNews/firebirdsql-run/main)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DeadNews_firebirdsql-run&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DeadNews_firebirdsql-run)\n\n## Installation\n\n```sh\npip install firebirdsql-run\n```\n',
    'author': 'DeadNews',
    'author_email': 'uhjnnn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeadNews/firebirdsql-run',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
