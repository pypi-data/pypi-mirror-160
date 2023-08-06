# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitignoregh']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.23,<4.0.0', 'click>=8.0.1,<9.0.0', 'rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['gitignoregh = gitignoregh.cli:main']}

setup_kwargs = {
    'name': 'gitignoregh',
    'version': '1.1.0',
    'description': 'gitignoregh is a command line tool that generates a .gitignore file for a project from the github gitignore templates repository',
    'long_description': '# gitignoregh\n\n<a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/-python-success?logo=python&logoColor=white"></a>\n<a href="https://github.com/sauljabin/gitignoregh"><img alt="GitHub" src="https://img.shields.io/badge/status-active-brightgreen"></a>\n<a href="https://github.com/sauljabin/gitignoregh/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/gitignoregh"></a>\n<a href="https://github.com/sauljabin/gitignoregh/actions"><img alt="GitHub Actions" src="https://img.shields.io/github/workflow/status/sauljabin/gitignoregh/CI?label=tests"></a>\n<a href="https://app.codecov.io/gh/sauljabin/gitignoregh"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/gitignoregh"></a>\n<a href="https://pypi.org/project/gitignoregh"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/gitignoregh"></a>\n<a href="https://pypi.org/project/gitignoregh"><img alt="Version" src="https://img.shields.io/pypi/v/gitignoregh"></a>\n<a href="https://libraries.io/pypi/gitignoregh"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/gitignoregh"></a>\n<a href="https://pypi.org/project/gitignoregh"><img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20osx-blueviolet"></a>\n\n`gitignoregh` is a command line tool that generates a `.gitignore` file for a project from the [github gitignore templates repository](https://github.com/github/gitignore).\n\n![https://raw.githubusercontent.com/sauljabin/gitignoregh/main/screenshots/options.png](https://raw.githubusercontent.com/sauljabin/gitignoregh/main/screenshots/options.png)\n\n## Installation\n\nInstall with pip:\n```sh\npip install gitignoregh\n```\n\nUpgrade with pip:\n```sh\npip install --upgrade gitignoregh\n```\n\n## Usage\n\nHelp:\n```sh\ngitignoregh -h\n```\n\nVersion:\n```sh\ngitignoregh --version\n```\n\nList all gitignore templates:\n```sh\ngitignoregh -l\n```\n\nSearch gitignore templates files:\n```sh\ngitignoregh -s\n```\n\nPrint a gitignore: \n```sh\ngitignoregh -p\n```\n\nReset github template repository:\n```sh\ngitignoregh --reset\n```\n\nGenerate `.gitignore` file (accepts multiple arguments):\n```sh\ngitignoregh java gradle\n```\n\n## Development\n\nInstalling poetry:\n```sh\npip install poetry\n```\n\nInstalling development dependencies:\n```sh\npoetry install\n```\n\nRunning unit tests:\n```sh\npoetry run python -m scripts.tests\n```\n\nApplying code styles:\n```sh\npoetry run python -m scripts.styles\n```\n\nRunning code analysis:\n```sh\npoetry run python -m scripts.analyze\n```\n\nRunning code coverage:\n```sh\npoetry run python -m scripts.tests-coverage\n```\n\nRunning cli using `poetry`:\n```sh\npoetry run gitignoregh\n```\n',
    'author': 'Saúl Piña',
    'author_email': 'sauljabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sauljabin/gitignoregh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
