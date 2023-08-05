# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['winfiletime']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'winfiletime',
    'version': '2.0',
    'description': 'Win32 Filetime / Datetime conversion functions',
    'long_description': '# filetime.py\n\nA Python module to convert datetime to/from a\n[Win32 FILETIME structure](https://msdn.microsoft.com/en-us/library/windows/desktop/ms724284).\n\n[Reference algorithm](https://support.microsoft.com/en-us/help/167296)\n\n\n## Usage\n\nInstall from PyPI: `pip install winfiletime`\n\nExample usage:\n\n```py\nimport datetime\nimport winfiletime\n\n# Convert a datetime to a filetime\nwinfiletime.from_datetime(datetime.datetime(2009, 7, 25, 23, 0))\n# 128930364000000000\n\n# Convert a filetime to a datetime\nwinfiletime.to_datetime(128930364000000000)\n# datetime.datetime(2009, 7, 25, 23, 0)\n```\n\n## License\n\nThis project is hereby released in the Public Domain.\nSee the `LICENSE` file for the full CC0 license text.\n',
    'author': 'Jerome Leclanche',
    'author_email': 'jerome@leclan.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jleclanche/winfiletime',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
