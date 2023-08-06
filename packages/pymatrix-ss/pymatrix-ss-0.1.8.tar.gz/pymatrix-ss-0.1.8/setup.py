# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymatrix']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pymatrix = pymatrix:screensaver']}

setup_kwargs = {
    'name': 'pymatrix-ss',
    'version': '0.1.8',
    'description': '',
    'long_description': '# pymatrix\n\n[![pypi](https://img.shields.io/pypi/v/pymatrix-ss?color=%2334D058)](https://pypi.org/project/pymatrix-ss/)\n\n## Screensaver with zsh-morpho\n\n![demo](./demo.svg)\n\n1. Install\n\n   ```shell\n   pip install pymatrix-ss\n   ```\n\n    [![Typing SVG](https://readme-typing-svg.herokuapp.com/?lines=pip+install+pymatrix-ss)](https://pypi.org/project/pymatrix-ss/)\n\n1. Open `~/.zshrc`\n   1. add `zsh-morpho` to `plugins`\n   1. config zsh-morpho\n\n      ```shell\n      zstyle ":morpho" screen-saver "pymatrix"\n      zstyle ":morpho" delay "290"             # 5 minutes  before screen saver starts\n      zstyle ":morpho" check-interval "60"     # check every 1 minute if to run screen saver\n      ```\n',
    'author': ' ',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m9810223/pymatrix-ss',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>3,<4',
}


setup(**setup_kwargs)
