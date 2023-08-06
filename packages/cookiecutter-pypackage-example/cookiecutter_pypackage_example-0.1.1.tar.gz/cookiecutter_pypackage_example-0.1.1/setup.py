# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiecutter_pypackage_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cookiecutter-pypackage-example',
    'version': '0.1.1',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# cookiecutter-pypackage-example\n\n[![Release](https://img.shields.io/github/v/release/xdurana/cookiecutter-pypackage-example)](https://img.shields.io/github/v/release/xdurana/cookiecutter-pypackage-example)\n[![Build status](https://img.shields.io/github/workflow/status/xdurana/cookiecutter-pypackage-example/merge-to-main)](https://img.shields.io/github/workflow/status/xdurana/cookiecutter-pypackage-example/merge-to-main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/xdurana/cookiecutter-pypackage-example)](https://img.shields.io/github/commit-activity/m/xdurana/cookiecutter-pypackage-example)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://xdurana.github.io/cookiecutter-pypackage-example/)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![License](https://img.shields.io/github/license/xdurana/cookiecutter-pypackage-example)](https://img.shields.io/github/license/xdurana/cookiecutter-pypackage-example)\n\nThis is a template repository for Python projects that use Poetry for their dependency management.\n\n- **Github repository**: <https://github.com/xdurana/cookiecutter-pypackage-example/>\n- **Documentation** <https://xdurana.github.io/cookiecutter-pypackage-example/>\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting\n[this page](https://github.com/xdurana/cookiecutter-pypackage-example/settings/secrets/actions/new).\n- Create a [new release](https://github.com/xdurana/cookiecutter-pypackage-example/releases/new) on Github.\nCreate a new tag in the form ``*.*.*``.\n\nFor more details, see [here](https://xdurana.github.io/cookiecutter-pypackage/releasing.html).\n\n---\n\nRepository initiated with [xdurana/cookiecutter-pypackage](https://github.com/xdurana/cookiecutter-pypackage).\n',
    'author': 'Xavier Duran',
    'author_email': 'fxavier.duran@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xdurana/cookiecutter-pypackage-example',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
