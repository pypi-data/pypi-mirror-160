# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_archive_deep']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['git-archive-deep = git_archive_deep.__main__:main']}

setup_kwargs = {
    'name': 'git-archive-deep',
    'version': '0.1.1',
    'description': 'Git Archive Deep',
    'long_description': "# Deep archive command for `git`\n\n[![PyPI](https://img.shields.io/pypi/v/git-archive-deep.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/git-archive-deep.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/git-archive-deep)][pypi status]\n[![License](https://img.shields.io/pypi/l/git-archive-deep)][license]\n\n[![Read the documentation at https://git-archive-deep.readthedocs.io/](https://img.shields.io/readthedocs/git-archive-deep/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/cd3/git-archive-deep/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/cd3/git-archive-deep/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/git-archive-deep/\n[read the docs]: https://git-archive-deep.readthedocs.io/\n[tests]: https://github.com/cd3/git-archive-deep/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/cd3/git-archive-deep\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Archive a git repository with all sub-modules.\n\n## Installation\n\nYou can install _Git Archive Deep_ via [pip] from [PyPI]:\n\n```console\n$ pip install git-archive-deep\n```\n\n## Usage\n\nLet's say you have a repository in a directory `MyTool/` and you want to archive version 2.1, which is tagged `v2.1`.\n```console\ngit archive-deep v2.1 ./MyTool\n```\nThis will create a zip file named `MyTool-v2.1.zip` that contains the repository along with its sub-modules.\n\nThis tool is similar to [git-archive-all](https://github.com/Kentzo/git-archive-all), but it allows you to specify a\ngit ref instead of archiving the currently checked out commit. It is really just simple wrapper around Git that calls\n`git archive <ref> .` in the repository directory, but then reads `.gitmodules` (if it exists), determines the SHA1 for each\nsub-module using `git rev-parse` (calling `git rev-parse v2.1:path/to/submodule` will print the SHA1 for the commit that is checked out in submodule\nlocated at `path/to/submodule` for version `v2.1`), and then just calls itself for each sub-module recursively, merging each archive into the main repo.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Git Archive Deep_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/cd3/git-archive-deep/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/cd3/git-archive-deep/blob/main/LICENSE\n[contributor guide]: https://github.com/cd3/git-archive-deep/blob/main/CONTRIBUTING.md\n[command-line reference]: https://git-archive-deep.readthedocs.io/en/latest/usage.html\n",
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cd3/git-archive-deep',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
