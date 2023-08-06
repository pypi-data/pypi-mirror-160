# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexis_uni_parser']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0', 'pandoc>=2.2,<3.0']

setup_kwargs = {
    'name': 'nexis-uni-parser',
    'version': '0.1.1',
    'description': 'Parse NexisUni rtf files into a jsonlines file.',
    'long_description': '# NexisUni Parser\n\nThis module can be used to convert Nexis Uni rich-text files to a tabular format.\n\n## Usage\n\nThere are three main functions that this package provides.\n\n### Convert an RTF file to plain text\n\nConverting an RTF file to a plain text file can be achieved more directly by using pandoc. That said, I have included a function that will convert an RTF file to a plain text file. Under the hood it just uses [pandoc](https://pypi.org/project/pandoc/).\n\n### Parse Nexis Uni Files\n\nThe result of parsing a nexisuni file is a gzipped JSON lines file. This can be read easily using pandas. I choose to convert to a compressed JSON lines file because the text data can get rather large. Writing it to Excel directly would add a dependency and would force all the data to be read into memory before writing the file. By streaming it directly into a JSON lines file, the memory consumption stays relatively low.\n\n```python\nfrom pathlib import Path\nfrom nexisuni_parser import parse\n\ninputfile = Path.home().joinpath("nexisuni-file.rtf")\n\noutput_filepath = parse(inputfile)\n\n# Reading the data into a pandas dataframe is easy from here.\n\nimport pandas as pd\n\nnexisuni_df = pd.read_json(str(output_filepath), compression="gzip", lines=True)\n\n```\n',
    'author': 'Garrett Shipley',
    'author_email': 'garrett.shipley7+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garth74/nexis-uni-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
