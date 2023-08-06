# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nexis_uni_parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['nexis-uni-parser = nexis_uni_parser.__main__:main']}

setup_kwargs = {
    'name': 'nexis-uni-parser',
    'version': '0.1.3',
    'description': 'Parse NexisUni rtf files into a jsonlines file.',
    'long_description': '# Nexis Uni Parser\n\n[![PyPI](https://img.shields.io/pypi/v/nexis-uni-parser.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/nexis-uni-parser.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/nexis-uni-parser)][python version]\n[![License](https://img.shields.io/pypi/l/nexis-uni-parser)][license]\n\n[![Read the documentation at https://nexis-uni-parser.readthedocs.io/](https://img.shields.io/readthedocs/nexis-uni-parser/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/garth74/nexis-uni-parser/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/garth74/nexis-uni-parser/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/nexis-uni-parser/\n[status]: https://pypi.org/project/nexis-uni-parser/\n[python version]: https://pypi.org/project/nexis-uni-parser\n[read the docs]: https://nexis-uni-parser.readthedocs.io/\n[tests]: https://github.com/garth74/nexis-uni-parser/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/garth74/nexis-uni-parser\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nThis package can be used to convert NexisUni richtext files to jsonlines format.\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Nexis Uni Parser_ via [pip] from [PyPI]:\n\n```console\npip install nexis-uni-parser\n```\n\n## Usage\n\nThere are two main functions that this package provides.\n\n### Convert an RTF file to plain text\n\nConverting an RTF file to a plain text file can be achieved directly by using pandoc. That said, I have included a function that will convert an RTF file to a plain text file since it could be useful. Under the hood, it just uses [pandoc](https://pypi.org/project/pandoc/).\n\n```python\nfrom pathlib import Path\nfrom nexis_uni_parser import convert_rtf_to_plain_text\n\ninputfile = Path.home().joinpath("nexisuni-file.rtf")\noutput_filepath = convert_rtf_to_plain_text(inputfile)\n\nprint(output_filepath)\n>>> /Users/name/nexisuni-file.txt\n\n```\n\n### Parse Nexis Uni Files\n\nThe `parse` function can be used to parse a single file or a directory. Both produce a gzipped JSON lines file. I choose to convert to a compressed JSON lines file because the text data can get large if all files are read into memory.\n\n```python\nfrom pathlib import Path\nfrom nexis_uni_parser import parse\n\ninputfile = Path.home().joinpath("nexisuni-file.rtf")\n\noutput_filepath = parse(inputfile)\n\n# Reading the data into a pandas dataframe is easy from here.\n\nimport pandas as pd\n\nnexisuni_df = pd.read_json(str(output_filepath), compression="gzip", lines=True)\n\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Nexis Uni Parser_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/garth74/nexis-uni-parser/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/garth74/nexis-uni-parser/blob/main/LICENSE\n[contributor guide]: https://github.com/garth74/nexis-uni-parser/blob/main/CONTRIBUTING.md\n[command-line reference]: https://nexis-uni-parser.readthedocs.io/en/latest/usage.html\n',
    'author': 'Garrett M. Shipley',
    'author_email': 'garrett.shipley7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garth74/nexis-uni-parser',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
