# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabler_icons', 'tabler_icons.templatetags']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tabler-icons',
    'version': '0.2.0',
    'description': 'SVG tabler icons for your apps.',
    'long_description': '# Tabler Icons\n\nSVG tabler icons for your apps.\n\n![PyPI](https://img.shields.io/pypi/v/tabler_icons)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/tabler_icons/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/tabler_icons)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/tabler_icons)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tabler_icons)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/tabler_icons)\n![Lines of code](https://img.shields.io/tokei/lines/github/alex-oleshkevich/tabler_icons)\n\n## Installation\n\nInstall `tabler_icons` using PIP or poetry:\n\n```bash\npip install tabler_icons\n# or\npoetry add tabler_icons\n```\n\n## Features\n\n-   TODO\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/tabler_icons',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
