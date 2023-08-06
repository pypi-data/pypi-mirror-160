# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deadnews_python_template']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deadnews-python-template',
    'version': '0.0.1a2',
    'description': 'Python Project Template',
    'long_description': '# deadnews-python-template\n\n> Python Project Template\n\n[![PyPI version](https://img.shields.io/pypi/v/deadnews-python-template)](https://pypi.org/project/deadnews-python-template)\n[![CI/CD](https://github.com/DeadNews/deadnews-python-template/actions/workflows/python-app.yml/badge.svg)](https://github.com/DeadNews/deadnews-python-template/actions/workflows/python-app.yml)\n[![pre-commit.ci](https://results.pre-commit.ci/badge/github/DeadNews/deadnews-python-template/main.svg)](https://results.pre-commit.ci/latest/github/DeadNews/deadnews-python-template/main)\n[![codecov](https://codecov.io/gh/DeadNews/deadnews-python-template/branch/main/graph/badge.svg?token=OCZDZIYPMC)](https://codecov.io/gh/DeadNews/deadnews-python-template)\n\n## Installation\n\n```sh\npip install deadnews-python-template\n```\n',
    'author': 'DeadNews',
    'author_email': 'uhjnnn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeadNews/deadnews-python-template',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
