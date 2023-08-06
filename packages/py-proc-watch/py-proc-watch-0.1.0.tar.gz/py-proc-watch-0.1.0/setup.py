# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['py_proc_watch', 'py_proc_watch_test']
install_requires = \
['colorama>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['pywatch = py_proc_watch:_entry_point']}

setup_kwargs = {
    'name': 'py-proc-watch',
    'version': '0.1.0',
    'description': 'Pure Python procps "watch" replacement',
    'long_description': '# py-proc-watch\n\nLibrary and command line tool for watching process output. This is more or less a simpler version of `watch` from [procps](https://gitlab.com/procps-ng/procps).\n\nThe main differences come from defaults:\n\n* `py-proc-watch` always trims long lines so they fit on the screen\n* `py-proc-watch` respects color ANSI escape sequences (but strips the rest)\n* Python or C for the implementation\n\n## Design goals\n\n`py-proc-watch` library and tool should be:\n\n1. simple\n2. fast for very long output of executed command\n3. easily tested for correct behavior\n4. pure Python to maximize the amount of supported systems\n5. easy to use in other tools\n\n## Usage\n\n`pywatch` command line tool supports only a few command line options to keep it simple:\n\n```text\nusage: pywatch.py [-h] [-n INTERVAL] [-p] [-v] command [command ...]\n\npositional arguments:\n  command               command to watch, can be specified as a quoted string or as a list (use -- to separate pywatch and command options)\n\noptions:\n  -h, --help            show this help message and exit\n  -n INTERVAL, --interval INTERVAL\n                        seconds to wait between command runs, positive floats and zero are accepted\n  -p, --precise         try to run the command precisely at intervals\n  -v, --debug           show debug information\n```\n\n`py_proc_watch` can be used also as a Python module to provide "watch-like" functionality easily. The library is quite simple, so just read the source and tests.\n\n## Development\n\n`py-proc-watch` uses [Python Poetry](https://python-poetry.org/) to manage dependencies.\n\nUsed tools:\n\n* [`isort`](https://pypi.org/project/isort/) for keeping imports sane\n* [`black`](https://pypi.org/project/black/) for enforcing a consistent code style\n* [`flake8`](https://pypi.org/project/flake8/) with [`pyproject-flake8`](https://pypi.org/project/pyproject-flake8/) for linting with `pyproject.toml` support\n* [`mypy`](https://pypi.org/project/mypy/) for type checking\n* [`pytest`](https://pypi.org/project/pytest/) for running test\n\nThe _magic_ incantation:\n\n```shell\npoetry run isort . && poetry run black . && poetry run pflake8 . && poetry run mypy . && poetry run pytest\n```\n\nwill run all of the above tools for you.\n\n## Contributing and reporting issues\n\nPlease use GitHub Issues and Pull requests. If you\'re contributing code please see [Development](#development) section.\n\n## License\n\nMIT, see [LICENSE.md](./LICENSE.md) for full text. This is very permissive license, see following pages for more information:\n\n* [Open Source Initiative page about MIT license](https://opensource.org/licenses/MIT)\n* [tl;drLegal page about MIT license](https://tldrlegal.com/license/mit-license)\n',
    'author': 'Krzysztof Pawlik',
    'author_email': 'krzysiek.pawlik@people.pl',
    'maintainer': 'Krzysztof Pawlik',
    'maintainer_email': 'krzysiek.pawlik@people.pl',
    'url': 'https://github.com/nelchael/py-proc-watch',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
