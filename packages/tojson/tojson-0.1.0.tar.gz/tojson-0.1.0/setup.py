# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tojson']

package_data = \
{'': ['*']}

install_requires = \
['numpy>1.18.0', 'pandas>1.0.0']

entry_points = \
{'console_scripts': ['csv2json = tojson:csv2json.main',
                     'csvtojson = tojson:csv2json.main',
                     'tojson = tojson:csv2json.main']}

setup_kwargs = {
    'name': 'tojson',
    'version': '0.1.0',
    'description': 'A CLI tool to export CSV files to JSON format',
    'long_description': '# CSV2JSON\n\n🚀 A CLI tool to export CSV files to JSON format.\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.7-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n\n## Requirements\n- 🐍 [python>=3.7](https://www.python.org/downloads/)\n\n\n## ⬇️ Installation\n\n```sh\npip install tojson\n```\n\n\n## ⌨️ Usage\n\n```\n➜ csv2json --help  # You can also use the alias `tojson` or `csvtojson`\n\nusage: csv2json [-h] [-o {dict,list,series,split,records,index}] [-i INDENT]\n                [-c]\n                path [path ...]\n\npositional arguments:\n  path                  Path to a single file/directory or multiple\n                        files/directories\n\noptions:\n  -h, --help            show this help message and exit\n  -o {dict,list,series,split,records,index}, --orient {dict,list,series,split,records,index}\n                        The type of the values of the dictionary\n  -i INDENT, --indent INDENT\n                        JSON output indentation\n  -c, --compress        Compress the output\n```\n\n\n## 📕 Examples\n\n```sh\ncsv2json foo.csv\n```\n\n```sh\n# Orient as list \ncsv2json foo.csv -o list\n```\n\n```sh\n# Compressed output and use zero indentation (minified)\ncsv2json foo.csv -c -i 0\n```\n',
    'author': 'Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
