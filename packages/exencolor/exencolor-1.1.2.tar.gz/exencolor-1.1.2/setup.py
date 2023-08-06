# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exencolor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exencolor',
    'version': '1.1.2',
    'description': 'A modern module for colored output.',
    'long_description': '# ExenColor\nA modern module for colored output.\n\n## Installation\nThe module is available for installation from PyPI via pip:\n```shell\n$ pip install exencolor\n```\n\n## Examples\n\n### Foreground\n\n```python\nfrom exencolor import colored, Color\n\nprint(colored("Hello World!", foreground=Color.GREEN))\n```\n![output](https://github.com/Exenifix/exencolor/blob/master/.github/img/foreground.png?raw=true)\n\n### Background\n\n```python\nfrom exencolor import colored, Color\n\nprint(colored("Hello World!", background=Color.BLUE))\n```\n![output](https://github.com/Exenifix/exencolor/blob/master/.github/img/background.png?raw=true)\n\n### Decorations\n\n```python\nfrom exencolor import colored, Decoration\n\nprint(colored("Hello World!", decoration=Decoration.UNDERLINE))\n```\n![output](https://github.com/Exenifix/exencolor/blob/master/.github/img/deco1.png?raw=true)\n\n```python\nfrom exencolor import colored, Decoration\n\nprint(colored("Hello World!", decorations=[Decoration.UNDERLINE, Decoration.BOLD]))\n```\n![output](https://github.com/Exenifix/exencolor/blob/master/.github/img/deco2.png?raw=true)\n\n### Combined\n\n```python\nfrom exencolor import colored, Decoration, Color\n\nprint(colored("Hello World!", foreground=Color.BRIGHT_CYAN, background=Color.BRIGHT_YELLOW, decoration=Decoration.UNDERLINE))\n```\n![output](https://github.com/Exenifix/exencolor/blob/master/.github/img/combined.png?raw=true)\n',
    'author': 'Exenifix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Exenifix/exencolor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
