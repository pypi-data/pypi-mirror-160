# Deep archive command for `git`

[![PyPI](https://img.shields.io/pypi/v/git-archive-deep.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/git-archive-deep.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/git-archive-deep)][pypi status]
[![License](https://img.shields.io/pypi/l/git-archive-deep)][license]

[![Read the documentation at https://git-archive-deep.readthedocs.io/](https://img.shields.io/readthedocs/git-archive-deep/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/cd3/git-archive-deep/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/cd3/git-archive-deep/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/git-archive-deep/
[read the docs]: https://git-archive-deep.readthedocs.io/
[tests]: https://github.com/cd3/git-archive-deep/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/cd3/git-archive-deep
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Archive a git repository with all sub-modules.

## Installation

You can install _Git Archive Deep_ via [pip] from [PyPI]:

```console
$ pip install git-archive-deep
```

## Usage

Let's say you have a repository in a directory `MyTool/` and you want to archive version 2.1, which is tagged `v2.1`.
```console
git archive-deep v2.1 ./MyTool
```
This will create a zip file named `MyTool-v2.1.zip` that contains the repository along with its sub-modules.

This tool is similar to [git-archive-all](https://github.com/Kentzo/git-archive-all), but it allows you to specify a
git ref instead of archiving the currently checked out commit. It is really just simple wrapper around Git that calls
`git archive <ref> .` in the repository directory, but then reads `.gitmodules` (if it exists), determines the SHA1 for each
sub-module using `git rev-parse` (calling `git rev-parse v2.1:path/to/submodule` will print the SHA1 for the commit that is checked out in submodule
located at `path/to/submodule` for version `v2.1`), and then just calls itself for each sub-module recursively, merging each archive into the main repo.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Git Archive Deep_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/cd3/git-archive-deep/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/cd3/git-archive-deep/blob/main/LICENSE
[contributor guide]: https://github.com/cd3/git-archive-deep/blob/main/CONTRIBUTING.md
[command-line reference]: https://git-archive-deep.readthedocs.io/en/latest/usage.html
